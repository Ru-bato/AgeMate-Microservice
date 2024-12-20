import os
import toml
import asyncio
from fastapi import FastAPI, Depends
from config.settings import settings

app = FastAPI()

# 加载配置文件的函数
def load_config(config_path: str):
    base_dir = os.path.dirname(os.path.abspath(__file__))
    try:
        with open(os.path.join(base_dir, config_path), 'r') as toml_config_file:
            config = toml.load(toml_config_file)
            print(f"Configuration File Loaded - {os.path.join(base_dir, config_path)}")
            return config
    except FileNotFoundError:
        print(f"Error: File '{config_path}' not found.")
        raise
    except toml.TomlDecodeError:
        print(f"Error: File '{config_path}' is not a valid TOML file.")
        raise

# 在 FastAPI 启动时加载配置并初始化 SeeAct
@app.on_event("startup")
async def startup_event():
    config = load_config(settings.config_path)
    # 初始化 SeeAct
    manager = SeeActManager(model=config["model"])
    await manager.initialize()  # 假设你有一个初始化方法

    # 启动 SeeAct 相关任务或调度
    await manager.execute_task("example_task", "example_website")

@app.on_event("shutdown")
async def shutdown_event():
    # 在应用关闭时清理资源
    pass
