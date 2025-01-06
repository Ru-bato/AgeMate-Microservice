from fastapi import WebSocket
import logging
import asyncio
import json

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"客户端已连接: {websocket.client}")

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)
        logger.info(f"客户端已断开: {websocket.client}")

    async def broadcast(self, action_data):
        dead_connections = []
        for connection in self.active_connections:
            try:
                await connection.send_json(action_data)
            except:
                dead_connections.append(connection)
        
        # 清理失效连接        
        for conn in dead_connections:
            self.active_connections.remove(conn)

class WebSocketManager:
    def __init__(self):
        self.websocket = None
        self.response_future = None
        
    async def send_message(self, message):
        if self.websocket:
            await self.websocket.send(message)
            
    async def wait_for_response(self, timeout=30):
        """等待来自扩展的响应"""
        if not self.websocket:
            raise Exception("WebSocket connection not available")
            
        try:
            response = await asyncio.wait_for(
                self.websocket.recv(),
                timeout=timeout
            )
            return json.loads(response)
        except asyncio.TimeoutError:
            raise Exception("Timeout waiting for extension response")

# 创建全局实例
websocket_manager = ConnectionManager()