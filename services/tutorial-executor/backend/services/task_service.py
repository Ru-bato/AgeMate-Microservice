from fastapi import BackgroundTasks, HTTPException
from .browser_service import browser_service
from playwright.async_api import Page, ElementHandle, TimeoutError
import asyncio
from models.task import Task, create_task, get_task, update_task
from loguru import logger
from uuid import UUID


class TaskService:
    """
    TaskService 类负责处理所有与任务执行相关的业务逻辑。
    包括初始化任务、执行浏览器交互、保存结果等。
    """

    @staticmethod
    async def perform_task(task_details: dict):
        """
        根据提供的任务详情执行一系列预定义的操作。
        
        :param task_details: 包含任务信息的字典，如URL和要执行的动作列表。
        :return: 返回一个包含任务状态和其他相关信息的字典。
        """

        # 创建新的任务记录
        new_task = Task(
                task_id=task_details['task_id'],
                url=task_details['url']
            )
        await create_task(new_task)

        # 初始化浏览器页面
        page = await browser_service.context.new_page()

        try:
            url = task_details.get('url')
            if not url:
                raise ValueError("URL is required")

            # 导航到指定的URL
            await page.goto(url, wait_until="load", timeout=60000)
            logger.info(f"Navigated to {url}")

            # 执行用户定义的动作序列
            if 'actions' in task_details:
                for action in task_details['actions']:
                    action_type = action.get('type')
                    selector = action.get('selector')
                    value = action.get('value', None)

                    try:
                        element: ElementHandle = await page.wait_for_selector(selector, timeout=5000)
                    except TimeoutError:
                        error_message = f"Element not found for selector {selector}"
                        logger.error(error_message)
                        async with SessionLocal() as db:
                            task = await db.get(Task, new_task.id)
                            task.status = 'failed'
                            task.error_message = error_message
                            await db.commit()
                        return {"status": "failed", "error": error_message}

                    if action_type == 'click':
                        try:
                            await element.click(timeout=5000)
                            logger.info(f"Clicked on element {selector}")
                        except Exception as e:
                            logger.error(f"Failed to click on element {selector}: {str(e)}")
                            raise
                    elif action_type == 'type':
                        try:
                            await element.fill(value, timeout=5000)
                            logger.info(f"Typed '{value}' into element {selector}")
                        except Exception as e:
                            logger.error(f"Failed to type into element {selector}: {str(e)}")
                            raise
                    elif action_type == 'select':
                        try:
                            await element.select_option(value=value, timeout=5000)
                            logger.info(f"Selected option '{value}' from element {selector}")
                        except Exception as e:
                            logger.error(f"Failed to select option from element {selector}: {str(e)}")
                            raise
                    else:
                        error_message = f"Unsupported action type {action_type}"
                        logger.error(error_message)
                        async with SessionLocal() as db:
                            task = await db.get(Task, new_task.id)
                            task.status = 'failed'
                            task.error_message = error_message
                            await db.commit()
                        return {"status": "failed", "error": error_message}
                    
                    await page.wait_for_timeout(500)  # Wait briefly between actions

            # 保存截图
            screenshot_path = f"screenshots/{task_details['task_id']}.png"
            await page.screenshot(path=screenshot_path, full_page=True)
            logger.info(f"Screenshot saved at {screenshot_path}")

            await update_task(str(new_task.id), {
                "status": "completed",
                "screenshot_path": screenshot_path
            })

        except Exception as e:
            error_message = f"An error occurred during task execution: {str(e)}"
            logger.error(error_message)
            await update_task(str(new_task.id), {
                "status": "failed",
                "error_message": error_message
            })
            raise HTTPException(status_code=500, detail=error_message)
        finally:
            await page.close()

        return {"status": "completed", "screenshot": screenshot_path}