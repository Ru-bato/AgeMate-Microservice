# import asyncio
# import websockets
# import requests
# async def test_websocket():
#     response = requests.get('https://api.ipify.org?format=json')
#     ip = response.json().get('ip')
#     uri = f"ws://127.0.0.1:9222"  # 确保使用正确的 URI
#     # uri = f"ws://{ip}:9222/devtools/browser/751d6d48-a389-4a07-a5ba-f88c97a1969e"
#     # uri = "wss://echo.websocket.org"
#     uri = "ws://localhost:5173"

#     try:
#         # 使用 'async with' 正确的方式连接 WebSocket
#         async with websockets.connect(uri) as websocket:
#             print("成功连接到 WebSocket 服务器")
#             # 发送测试消息
#             await websocket.send("测试消息")
#             print("发送消息: 测试消息")
#             # 等待响应
#             response = await websocket.recv()
#             print(f"收到响应: {response}")
#     except Exception as e:
#         print(f"连接失败: {e}")

# # 使用 asyncio.run() 来启动异步任务
# asyncio.run(test_websocket())
# from playwright.sync_api import sync_playwright

# with sync_playwright() as p:
#     browser = p.chromium.connect_over_cdp("ws://localhost:9222")
#     context = browser.new_context()
#     page = context.new_page()
#     page.goto("https://example.com")
#     print(page.title())
#     browser.close()

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect_over_cdp("http://localhost:9222")
    page = browser.contexts[0].pages[0]
    page.goto('https://code.visualstudio.com/download')
    with page.expect_download() as download_info:
        page.get_by_label("Windows CLI 64-bit x64").click()
    download = download_info.value
    print(download.path())
    print(download.suggested_filename)
    browser.close()
