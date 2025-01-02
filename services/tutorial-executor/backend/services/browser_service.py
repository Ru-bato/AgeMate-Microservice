from playwright.async_api import async_playwright, BrowserContext
from fastapi import HTTPException
from loguru import logger
import asyncio

class BrowserService:
    """BrowserService handles all browser interactions."""

    class BrowserContextManager:
        def __init__(self):
            self.playwright = None
            self.browser = None
            self.context: BrowserContext = None

        async def __aenter__(self):
            self.playwright = await async_playwright().start()
            self.browser = await self.playwright.chromium.launch(headless=True)
            self.context = await self.browser.new_context()
            return self.context

        async def __aexit__(self, exc_type, exc_val, exc_tb):
            if self.context:
                await self.context.close()
            if self.browser:
                await self.browser.close()
            if self.playwright:
                await self.playwright.stop()

    @staticmethod
    async def get_new_page() -> BrowserContext:
        """Returns a new page within the browser context."""
        async with BrowserService.BrowserContextManager() as context:
            page = await context.new_page()
            return page

    @staticmethod
    async def navigate_to_url(page: BrowserContext, url: str):
        """Navigates to the specified URL and waits until the page is loaded."""
        try:
            await page.goto(url, wait_until="load", timeout=60000)
            logger.info(f"Navigated to {url}")
        except Exception as e:
            error_message = f"Failed to navigate to {url}: {str(e)}"
            logger.error(error_message)
            raise HTTPException(status_code=500, detail=error_message)

    @staticmethod
    async def take_screenshot(page: BrowserContext, path: str):
        """Takes a screenshot of the current page and saves it to the specified path."""
        try:
            await page.screenshot(path=path, full_page=True)
            logger.info(f"Screenshot saved at {path}")
        except Exception as e:
            error_message = f"Failed to save screenshot: {str(e)}"
            logger.error(error_message)
            raise HTTPException(status_code=500, detail=error_message)

    @staticmethod
    async def click_element(page: BrowserContext, selector: str, timeout: int = 5000):
        """Clicks on an element identified by the given selector."""
        try:
            element = await page.wait_for_selector(selector, timeout=timeout)
            await element.click(timeout=timeout)
            logger.info(f"Clicked on element {selector}")
        except Exception as e:
            error_message = f"Failed to click on element {selector}: {str(e)}"
            logger.error(error_message)
            raise HTTPException(status_code=500, detail=error_message)

    @staticmethod
    async def type_into_element(page: BrowserContext, selector: str, value: str, timeout: int = 5000):
        """Types text into an input field identified by the given selector."""
        try:
            element = await page.wait_for_selector(selector, timeout=timeout)
            await element.fill(value, timeout=timeout)
            logger.info(f"Typed '{value}' into element {selector}")
        except Exception as e:
            error_message = f"Failed to type into element {selector}: {str(e)}"
            logger.error(error_message)
            raise HTTPException(status_code=500, detail=error_message)

    @staticmethod
    async def select_option(page: BrowserContext, selector: str, value: str, timeout: int = 5000):
        """Selects an option from a dropdown menu identified by the given selector."""
        try:
            element = await page.wait_for_selector(selector, timeout=timeout)
            await element.select_option(value=value, timeout=timeout)
            logger.info(f"Selected option '{value}' from element {selector}")
        except Exception as e:
            error_message = f"Failed to select option from element {selector}: {str(e)}"
            logger.error(error_message)
            raise HTTPException(status_code=500, detail=error_message)