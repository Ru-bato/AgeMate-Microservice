from fastapi import WebSocket
import logging

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

# 创建全局实例
websocket_manager = ConnectionManager()