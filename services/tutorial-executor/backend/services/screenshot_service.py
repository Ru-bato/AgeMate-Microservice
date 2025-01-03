# -*- coding: utf-8 -*-
"""
Screenshot Service

This module handles the logic for capturing screenshots of web pages.
It interacts with web automation tools and other services to prepare data,
execute screenshot capture, and process results.
"""

import asyncio
from fastapi import HTTPException, status
from models.schemas import ScreenshotRequest, ScreenshotResponse
from config.logging import logger
from pyppeteer import launch
import os
from datetime import datetime
from models.database import get_db

class ScreenshotService:
    def __init__(self):
        self.browser = None

    async def initialize(self):
        """
        Initializes the browser instance for screenshot capture.
        """
        try:
            self.browser = await launch(headless=True)
            logger.info("Browser initialized for screenshot service.")
        except Exception as e:
            logger.error(f"Error initializing browser: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def shutdown(self):
        """
        Closes the browser instance gracefully.
        """
        if self.browser:
            await self.browser.close()
            logger.info("Browser closed.")

    async def capture_screenshot(self, request: ScreenshotRequest) -> ScreenshotResponse:
        """
        Captures a screenshot based on the provided request.

        Args:
            request (ScreenshotRequest): The input data required for screenshot capture.

        Returns:
            ScreenshotResponse: The result of the screenshot capture.
        """
        try:
            # Log the start of the screenshot capture
            logger.info(f"Starting screenshot capture for request: {request}")

            # Prepare data for screenshot capture
            prepared_data = await self._prepare_data(request)

            # Execute the actual screenshot capture process
            screenshot_result = await self._execute_capture(prepared_data)

            # Process and format the screenshot result
            formatted_result = await self._process_result(screenshot_result)

            # Save screenshot log
            await self.save_screenshot_log(request, formatted_result)

            # Log the completion of the screenshot capture
            logger.info(f"Screenshot capture completed. Result: {formatted_result}")

            return formatted_result

        except Exception as e:
            logger.error(f"Error during screenshot capture: {str(e)}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

    async def _execute_capture(self, data):
        """
        Executes the screenshot capture using the prepared data.

        Args:
            data (dict): Prepared data ready for screenshot capture.

        Returns:
            dict: Raw screenshot capture results.
        """
        try:
            page = await self.browser.newPage()
            await page.goto(data['url'], {'waitUntil': 'networkidle2'})
            
            # Optionally set viewport size if specified in request
            if 'viewport' in data and data['viewport']:
                await page.setViewport(data['viewport'])

            # Optionally add custom JavaScript or CSS before capturing the screenshot
            if 'scripts' in data:
                for script in data['scripts']:
                    await page.evaluate(script)

            # Capture the screenshot
            screenshot_path = os.path.join('/tmp', f"screenshot_{data['timestamp']}.png")
            await page.screenshot({'path': screenshot_path, 'fullPage': True})

            # Close the page
            await page.close()

            return {"screenshot_path": screenshot_path}
        except Exception as e:
            logger.error(f"Error executing screenshot capture: {str(e)}")
            raise

    async def _process_result(self, raw_result):
        """
        Processes and formats the raw screenshot capture results.

        Args:
            raw_result (dict): Raw screenshot capture results.

        Returns:
            ScreenshotResponse: Formatted screenshot response.
        """
        try:
            # Implement any post-processing logic here
            processed_result = ScreenshotResponse(screenshot_url=raw_result["screenshot_path"])
            logger.info(f"Processed screenshot result: {processed_result}")

            return processed_result
        except Exception as e:
            logger.error(f"Error processing result: {str(e)}")
            raise

    async def _prepare_data(self, request: ScreenshotRequest):
        """
        Prepares the data necessary for running the screenshot capture.

        Args:
            request (ScreenshotRequest): The input data required for screenshot capture.

        Returns:
            dict: Prepared data ready for screenshot capture.
        """
        try:
            # Prepare the input data for the screenshot capture
            prepared_data = {
                "url": request.url,
                "viewport": request.viewport,
                "scripts": request.scripts,
                "timestamp": datetime.utcnow().timestamp()  # To ensure unique filenames
            }

            return prepared_data
        except Exception as e:
            logger.error(f"Error preparing data: {str(e)}")
            raise

    async def save_screenshot_log(self, request: ScreenshotRequest, response: ScreenshotResponse):
        """
        Saves the screenshot request and response as a log entry in the database.

        Args:
            request (ScreenshotRequest): The original screenshot request.
            response (ScreenshotResponse): The screenshot response.
        """
        try:
            db = await get_db()
            log_entry = {
                "url": request.url,
                "viewport": request.viewport,
                "scripts": request.scripts,
                "screenshot_url": response.screenshot_url,
                "timestamp": datetime.utcnow()
            }
            await db.screenshot_logs.insert_one(log_entry)
            logger.info("Screenshot log saved.")
        except Exception as e:
            logger.error(f"Error saving screenshot log: {str(e)}")
            raise