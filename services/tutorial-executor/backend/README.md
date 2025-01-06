seeact-fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py                     # FastAPI应用入口
│   ├── config/                     # 配置文件夹
│   │   ├── __init__.py
│   │   ├── settings.py             # 应用配置设置
│   │   └── logging.py              # 日志配置
│   ├── models/                     # 数据模型文件夹
│   │   ├── __init__.py
│   │   ├── database.py             # MongoDB异步连接和操作
│   │   ├── schemas.py              # Pydantic数据验证模型
│   │   └── crud.py                 # CRUD操作
│   ├── routes/                     # API路由文件夹
│   │   ├── __init__.py
│   │   ├── web_actions.py          # Web交互动作路由
│   │   ├── inference.py            # 推理相关路由
│   │   └── other_routes.py         # 其他路由
│   ├── services/                   # 业务逻辑服务文件夹
│   │   ├── __init__.py
│   │   ├── browser_service.py      # 浏览器服务
│   │   ├── inference_service.py    # 推理服务
│   │   └── screenshot_service.py   # 截图服务
│   ├── utils/                      # 工具函数文件夹
│   │   ├── __init__.py
│   │   ├── dom_utils.py            # DOM处理工具
│   │   ├── image_utils.py          # 图像处理工具
│   │   ├── format_prompt_utils.py  # 提示格式化工具
│   │   └── evaluation_utils.py     # 评估工具
│   ├── workers/                    # 后台任务文件夹
│   │   ├── __init__.py
│   │   └── tasks.py                # Celery等后台任务
│   └── static/                      # 静态文件如截图等
│       └── screenshots/
├── tests/                          # 测试文件夹
│   ├── __init__.py
│   ├── test_main.py
│   ├── test_services.py
│   └── conftest.py
├── Dockerfile                      # Docker镜像构建文件
├── docker-compose.yml              # Docker容器编排文件
├── requirements.txt                # Python依赖包
└── README.md                       # 项目说明文档


现在先给我完整的main.py的内容，如果由于对话长度限制，一次不能输出完整内容，可以在多轮回答中给出。

请继续

你是否已经给出了main.py的完整内容？如果是，请回答是，如果还没有，请补全剩余内容