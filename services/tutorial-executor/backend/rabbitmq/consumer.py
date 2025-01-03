import aio_pika
import logging
import json

logger = logging.getLogger(__name__)

class RabbitMQConsumer:
    def __init__(self, rabbitmq_url: str, background_tasks, run_seeact):
        self.rabbitmq_url = rabbitmq_url
        self.background_tasks = background_tasks
        self.run_seeact = run_seeact

    async def start(self):
        # 连接到 RabbitMQ
        connection = await aio_pika.connect_robust(self.rabbitmq_url)
        channel = await connection.channel()

        # 声明队列
        queue = await channel.declare_queue(
            "tutorial_executor_queue",
            durable=True
        )

        async def process_message(message: aio_pika.IncomingMessage):
            async with message.process():
                try:
                    data = json.loads(message.body.decode())
                    logger.info(f"Received message: {data}")
                    
                    # 检查消息类型
                    if data.get('action') == 'start_seeact':
                        logger.info("Starting SeeAct task...")
                        self.background_tasks.add_task(self.run_seeact)
                    else:
                        logger.info(f"Ignored message with action: {data.get('action')}")
                        
                except Exception as e:
                    logger.error(f"Error processing message: {e}")

        # 开始消费消息
        await queue.consume(process_message)
        
        return connection