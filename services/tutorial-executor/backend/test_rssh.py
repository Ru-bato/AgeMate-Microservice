from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.connect("ws://server_ip:9223")  # 连接到本地用户 Chrome
    page = browser.new_page()
    page.goto("https://example.com")
    print(page.title())
