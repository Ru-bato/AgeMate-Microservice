# from playwright.sync_api import sync_playwright

# with sync_playwright() as p:
#     browser = p.chromium.connect("wss://62b8-111-187-15-75.ngrok-free.app/json/version")  # 连接到本地用户 Chrome
#     page = browser.new_page()
#     page.goto("https://example.com")
#     print(page.title())

# import requests

# response = requests.get("http://localhost:9222/json/version")
# data = response.json()
# ws_url = data["webSocketDebuggerUrl"]
# print(ws_url)

# from playwright.sync_api import sync_playwright

# with sync_playwright() as p:
#     ws_url = "wss://62b8-111-187-15-75.ngrok-free.app/devtools/browser/<id>"  # 获取的正确的 WebSocket URL
#     browser = p.chromium.connect(ws_url)
#     page = browser.new_page()
#     page.goto("https://example.com")
#     print(page.title())


from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    # 连接到本地计算机的 Chrome 实例
    # browser = p.chromium.connect_over_cdp('http://127.0.0.1:9222')
    browser = p.chromium.connect_over_cdp('http://192.168.65.254:9222')
    page = browser.new_page()
    page.goto('https://example.com')
    print(page.title())
    browser.close()

# # Import the sync_playwright function from the sync_api module of Playwright.
# from playwright.sync_api import sync_playwright

# # Start a new session with Playwright using the sync_playwright function.
# with sync_playwright() as playwright:
#     # Connect to an existing instance of Chrome using the connect_over_cdp method.
#     browser = playwright.chromium.connect_over_cdp("http://127.0.0.1:9222")

#     # Retrieve the first context of the browser.
#     default_context = browser.contexts[0]

#     # Retrieve the first page in the context.
#     page = default_context.pages[0]

#     # Print the title of the page.
#     print(page.title())

#     # Print the URL of the page.
#     print(page.url)
