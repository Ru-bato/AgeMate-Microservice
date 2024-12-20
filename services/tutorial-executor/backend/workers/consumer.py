import asyncio
import aio_pika
import toml
from seeact import main  # 导入原有核心逻辑函数
from utils.redis_client import get_redis_client
from main import get_config, base_dir

async def consume_tasks(redis_client, config, base_dir):
    """Consume tasks from RabbitMQ and process them."""
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        queue = await channel.declare_queue('task_queue')

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    task_data = toml.loads(message.body.decode())
                    task_id = task_data["id"]
                    task_input = task_data["task"]
                    website_input = task_data["website"]

                    try:
                        # Call the existing main function here
                        await main(config, base_dir, task=task_input, website=website_input)

                        # Update task status in Redis after processing
                        redis_client.set(task_id, "completed")
                    except Exception as e:
                        # Log any errors that occur during processing
                        logger.error(f"Error processing task {task_id}: {str(e)}")
                        redis_client.set(task_id, "failed")

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    redis_client = get_redis_client()  # 初始化Redis客户端
    config = get_config()  # 加载配置
    loop.run_until_complete(consume_tasks(redis_client, config, base_dir))