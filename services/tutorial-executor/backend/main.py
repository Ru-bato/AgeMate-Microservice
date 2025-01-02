import asyncio
import os
import logging
from fastapi import FastAPI, BackgroundTasks, Request, status, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import sys
from seeact import main as seeact_main
import uvicorn
from rabbitmq.consumer import RabbitMQConsumer
from pydantic import BaseModel
from dataclasses import dataclass
import toml
from websocket_manager import websocket_manager
import platform
import subprocess
import psutil
from typing import Optional
from playwright.async_api import async_playwright
import requests
import miniupnpc
import socket
from contextlib import asynccontextmanager

# 初始化 FastAPI 应用
app = FastAPI()

# 确保可以找到本地的 seeact.py 文件
sys.path.append(os.path.join(os.path.dirname(__file__), "path_to_seeact_directory"))

BASE_URL = "/tutorial-executor"
background_tasks = BackgroundTasks()

# CORS Middleware
origins = [
    "http://localhost",
    "http://localhost:5173",  # Assuming a frontend dev server at this address
    # Add more origins as needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 日志配置
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler()
formatter = logging.Formatter('[%(levelname)s] %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# WebSocket 端点
@app.websocket("/tutorial-executor/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket_manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            logger.info(f"收到消息来自 {websocket.client}: {data}")
            if data["type"] == "execute_action":
                await perform_action(data["data"])
            elif data["type"] == "skip_action":
                await skip_current_step()
            elif data["type"] == "auto_execute":
                enable_auto_execute()
    except WebSocketDisconnect:
        websocket_manager.disconnect(websocket)
    except Exception as e:
        logger.error(f"WebSocket 异常: {e}")
        websocket_manager.disconnect(websocket)

# API 端点

class ExecuteRequest(BaseModel):
    query: str
    url: str
    clientIP: str

class ChromeLauncher:
    @staticmethod
    def find_chrome_executable() -> Optional[str]:
        """智能查找 Chrome 可执行文件的路径"""
        system = platform.system()
        
        if system == "Windows":
            import winreg
            try:
                # 从注册表查找 Chrome 安装路径
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                    r"SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe") as key:
                    return winreg.QueryValue(key, None)
            except WindowsError:
                # 常见安装路径
                paths = [
                    os.path.expandvars(r"%ProgramFiles%\Google\Chrome\Application\chrome.exe"),
                    os.path.expandvars(r"%ProgramFiles(x86)%\Google\Chrome\Application\chrome.exe"),
                    os.path.expandvars(r"%LocalAppData%\Google\Chrome\Application\chrome.exe"),
                ]
                return next((path for path in paths if os.path.exists(path)), None)
                
        elif system == "Darwin":  # macOS
            paths = [
                "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                "~/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            ]
            return next((os.path.expanduser(path) for path in paths if os.path.exists(os.path.expanduser(path))), None)
            
        elif system == "Linux":
            # 在 Linux 上查找 Chrome
            try:
                # 使用 which 命令查找
                chrome_path = subprocess.check_output(["which", "google-chrome"], 
                                                    universal_newlines=True).strip()
                return chrome_path
            except subprocess.CalledProcessError:
                # 常见安装路径
                paths = [
                    "/usr/bin/google-chrome",
                    "/usr/bin/google-chrome-stable",
                    "/usr/bin/chromium",
                ]
                return next((path for path in paths if os.path.exists(path)), None)
        
        return None

    @staticmethod
    def is_chrome_running_with_debug_port() -> bool:
        """检查是否已有 Chrome 实例在运行并开启了调试端口"""
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if proc.info['name'] and 'chrome' in proc.info['name'].lower():
                    cmdline = proc.info.get('cmdline', [])
                    if any('--remote-debugging-port=9222' in arg for arg in cmdline):
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        return False

    @staticmethod
    async def ensure_debug_chrome() -> bool:
        """确保有一个带调试端口的 Chrome 实例在运行"""
        if ChromeLauncher.is_chrome_running_with_debug_port():
            logger.info("已检测到带调试端口的 Chrome 正在运行")
            return True

        chrome_path = ChromeLauncher.find_chrome_executable()
        if not chrome_path:
            logger.error("未找到 Chrome 可执行文件")
            return False

        try:
            # 创建用户数据目录
            user_data_dir = os.path.join(os.path.expanduser("~"), ".seeact", "chrome-debug-profile")
            os.makedirs(user_data_dir, exist_ok=True)

            # 启动 Chrome
            subprocess.Popen([
                chrome_path,
                f"--user-data-dir={user_data_dir}",
                "--remote-debugging-port=9222",
                "--no-first-run",
                "--no-default-browser-check",
                "about:blank"  # 打开空白页面
            ])
            
            # 等待 Chrome 启动
            for _ in range(5):
                if ChromeLauncher.is_chrome_running_with_debug_port():
                    logger.info("成功启动带调试端口的 Chrome")
                    return True
                await asyncio.sleep(1)
            
            logger.error("Chrome 启动超时")
            return False
            
        except Exception as e:
            logger.error(f"启动 Chrome 失败: {e}")
            return False

class PortForwardManager:
    def __init__(self):
        self.local_ip = None
        self.local_port = None
        self.external_port = None
        self.os_type = platform.system()

    def get_local_ip(self):
        """获取本机局域网IP"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            self.local_ip = s.getsockname()[0]
            s.close()
            logger.info(f"本机局域网IP: {self.local_ip}")
            return True
        except Exception as e:
            logger.error(f"获取本机IP失败: {e}")
            return False

    async def setup_port_forwarding(self, local_port=9222, external_port=9222):
        """设置端口转发"""
        try:
            if not self.get_local_ip():
                return False

            self.local_port = local_port
            self.external_port = external_port

            if self.os_type == 'Linux':
                # Linux 使用 iptables
                commands = [
                    [
                        'sudo', 'iptables', '-t', 'nat', '-A', 'PREROUTING', 
                        '-p', 'tcp', '--dport', str(external_port), 
                        '-j', 'DNAT', '--to-destination', f"{self.local_ip}:{local_port}"
                    ],
                    [
                        'sudo', 'iptables', '-A', 'FORWARD', '-p', 'tcp', 
                        '-d', self.local_ip, '--dport', str(local_port), 
                        '-j', 'ACCEPT'
                    ]
                ]
                for cmd in commands:
                    try:
                        subprocess.run(cmd, check=True, capture_output=True)
                    except subprocess.CalledProcessError as e:
                        logger.error(f"执行命令失败: {e.stderr.decode()}")
                        return False

            elif self.os_type == 'Windows':
                # Windows 使用 netsh
                command = [
                    'netsh', 'interface', 'portproxy', 
                    'add', 'v4tov4', 
                    f'listenport={external_port}',
                    'listenaddress=0.0.0.0',
                    f'connectport={local_port}',
                    f'connectaddress={self.local_ip}'
                ]
                try:
                    subprocess.run(command, check=True, capture_output=True)
                except subprocess.CalledProcessError as e:
                    logger.error(f"执行命令失败: {e.stderr.decode()}")
                    return False

            else:
                logger.error(f"不支持的操作系统: {self.os_type}")
                return False

            # 验证端口转发
            try:
                await asyncio.sleep(1)  # 等待端口转发生效
                response = requests.get(f'http://{self.local_ip}:{self.external_port}/json/version', timeout=2)
                if response.status_code == 200:
                    logger.info("端口转发验证成功")
                    return True
            except Exception as e:
                logger.warning(f"端口转发验证失败: {e}")
                # 继续尝试，因为有些环境可能无法直接验证

            logger.info(f"端口转发设置完成: {self.local_ip}:{self.local_port} -> 0.0.0.0:{self.external_port}")
            return True

        except Exception as e:
            logger.error(f"设置端口转发失败: {e}")
            return False

    async def remove_port_forwarding(self):
        """移除端口转发"""
        try:
            if not self.local_ip or not self.local_port or not self.external_port:
                return

            if self.os_type == 'Linux':
                commands = [
                    [
                        'sudo', 'iptables', '-t', 'nat', '-D', 'PREROUTING', 
                        '-p', 'tcp', '--dport', str(self.external_port), 
                        '-j', 'DNAT', '--to-destination', f"{self.local_ip}:{self.local_port}"
                    ],
                    [
                        'sudo', 'iptables', '-D', 'FORWARD', '-p', 'tcp', 
                        '-d', self.local_ip, '--dport', str(self.local_port), 
                        '-j', 'ACCEPT'
                    ]
                ]
                for cmd in commands:
                    try:
                        subprocess.run(cmd, check=True, capture_output=True)
                    except subprocess.CalledProcessError as e:
                        logger.error(f"移除端口转发失败: {e.stderr.decode()}")

            elif self.os_type == 'Windows':
                command = [
                    'netsh', 'interface', 'portproxy',
                    'delete', 'v4tov4',
                    f'listenport={self.external_port}',
                    'listenaddress=0.0.0.0'
                ]
                try:
                    subprocess.run(command, check=True, capture_output=True)
                except subprocess.CalledProcessError as e:
                    logger.error(f"移除端口转发失败: {e.stderr.decode()}")

            logger.info("端口转发已移除")

        except Exception as e:
            logger.error(f"移除端口转发时发生错误: {e}")

@app.post("/tutorial-executor/execute")
async def execute(request: ExecuteRequest, background_tasks: BackgroundTasks):
    """接收前端请求，启动 SeeAct 操作"""
    logger.info("收到前端启动请求")
    logger.info(f"请求参数: query={request.query}, url={request.url}, ip={request.clientIP}")
    
    try:
        # 构建连接URL
        ws_url = f"ws://{request.clientIP}:9222"
        logger.info(f"尝试连接到用户Chrome: {ws_url}")
        
        # 尝试连接到用户浏览器
        async with async_playwright() as p:
            try:
                browser = await p.chromium.connect_over_cdp(ws_url)
                context = browser.contexts[0]
                pages = context.pages
                page = pages[0] if pages else await context.new_page()
                
                # 启动 SeeAct
                background_tasks.add_task(run_seeact, request.query, request.url, request.clientIP)
                return {"status": "success", "message": "SeeAct 已启动"}
                
            except Exception as e:
                logger.error(f"连接到用户浏览器失败: {str(e)}")
                raise HTTPException(
                    status_code=500,
                    detail="无法连接到用户浏览器，请确保Chrome调试模式已启动且端口可访问"
                )
    except Exception as e:
        logger.error(f"执行过程中发生错误: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )
    
@app.get("/tutorial-executor/start-seeact")
async def start_seeact_endpoint():
    """启动 SeeAct 任务"""
    config_path = os.path.join(os.path.dirname(__file__), "config", "demo_mode.toml")
    with open(config_path, 'r') as toml_config_file:
        config = toml.load(toml_config_file)
    
    base_dir = os.path.dirname(__file__)
    task = config["basic"]["default_task"]
    url = config["basic"]["default_website"]
    
    # 等待 Chrome 扩展建立连接
    retry_count = 0
    while retry_count < 5:
        try:
            async with async_playwright() as p:
                # 尝试连接到用户浏览器
                browser = await p.chromium.connect_over_cdp("ws://localhost:9222")
                await browser.close()
                break
        except Exception:
            await asyncio.sleep(1)
            retry_count += 1
    
    # 启动 seeact
    asyncio.create_task(seeact_main(config, base_dir, task, url))
    
    return {
        "status": "success",
        "redirect_url": url,
        "task": task
    }

@app.get("/tutorial-executor")
async def check_alive():
    return {"message": "I'm alive"}

# 健康检查端点
@app.get("/health")
def health_check():
    return {"status": "ok"}

# 异常处理器
@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    logger.error(f"意外错误: {exc}")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"message": str(exc)},
    )

# 执行相关函数

@dataclass
class ExecutionConfig:
    auto_execute: bool = False

config_execution = ExecutionConfig()
taken_actions = []
task_queue = []

def enable_auto_execute():
    config_execution.auto_execute = True
    logger.info("已启用自动执行模式")

async def perform_action(data):
    if config_execution.auto_execute:
        logger.info("自动执行模式下执行操作")
        await execute_specific_action(data)
    else:
        logger.info("等待用户指示以执行操作")
        # 可以在此添加等待用户指示的逻辑

async def skip_current_step():
    action = "当前操作已被跳过"
    taken_actions.append(action)
    logger.info(action)
    if task_queue:
        task_queue.pop(0)
    # 可以在此添加继续下一个任务的逻辑

async def execute_specific_action(data):
    try:
        component_id = data.get("componentId")
        action = data.get("action")
        # 在这里实现具体的操作逻辑，例如通过 Playwright 操作页面元素
        logger.info(f"执行操作: {action} 在组件: {component_id}")
        # 示例：与 Playwright 会话交互
        # await session_control.active_page.click(f'[data-id="{component_id}"]')
    except Exception as e:
        logger.error(f"执行操作时出错: {e}")

async def run_seeact(query: str, url: str, clientIP: str):
    """
    在后台异步运行 seeact.py 的 main 函数
    """
    logger.info("开始运行 SeeAct 主任务。")
    
    # 配置文件路径
    config_path = os.path.join(os.path.dirname(__file__), "config", "demo_mode.toml")
    
    # 加载配置
    config = None
    try:
        import toml
        with open(config_path, 'r') as toml_config_file:
            config = toml.load(toml_config_file)
            logger.info(f"已加载配置文件 - {config_path}")
    except FileNotFoundError:
        logger.error(f"错误：文件 '{config_path}' 未找到。")
        return
    except toml.TomlDecodeError:
        logger.error(f"错误：文件 '{config_path}' 不是有效的 TOML 文件。")
        return

    # 调用 seeact 的 main 函数
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        logger.info(f"基目录: {base_dir}")
        await seeact_main(config, base_dir, query, url, clientIP)
    except Exception as e:
        logger.error(f"SeeAct 主任务执行时出错: {str(e)}")
        logger.exception("详细错误信息:")

@app.on_event("startup")
async def startup_event():
    """服务启动时初始化 WebSocket 管理器"""
    global websocket_manager

@app.on_event("shutdown")
async def shutdown_event():
    """服务关闭时清理连接"""
    for connection in websocket_manager.active_connections:
        await connection.close()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8003)
