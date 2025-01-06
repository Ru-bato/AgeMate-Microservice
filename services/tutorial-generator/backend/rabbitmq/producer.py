import aio_pika
import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class RabbitMQProducer:
    def __init__(self, rabbitmq_url: str):
        self.rabbitmq_url = rabbitmq_url
        self._connection = None
        self._channel = None
        self.exchange_name = "tutorial_exchange"  # 添加交换机
        self.queue_name = "tutorial_executor_queue"
        self.routing_key = "tutorial.seeact"  # 使用点号分隔的路由键

    async def connect(self):
        if not self._connection:
            self._connection = await aio_pika.connect_robust(self.rabbitmq_url)
            self._channel = await self._connection.channel()
            
            # 声明交换机
            self._exchange = await self._channel.declare_exchange(
                self.exchange_name,
                aio_pika.ExchangeType.TOPIC,  # 使用 TOPIC 类型交换机
                durable=True
            )

            # 声明队列
            queue = await self._channel.declare_queue(
                self.queue_name,
                durable=True,
                arguments={
                    'x-message-ttl': 86400000,  # 消息 TTL：24小时
                    'x-dead-letter-exchange': f"{self.exchange_name}.dlx",  # 死信交换机
                    'x-dead-letter-routing-key': f"{self.routing_key}.dead"  # 死信路由键
                }
            )

            # 绑定队列到交换机
            await queue.bind(
                self._exchange,
                routing_key=self.routing_key
            )

            logger.info("Connected to RabbitMQ and setup completed")

    async def send_message(self, action: str, data: Dict[str, Any] = None):
        try:
            await self.connect()
            
            message = {
                'action': action,
                'data': data or {}
            }

            # 发送消息
            await self._exchange.publish(
                aio_pika.Message(
                    body=json.dumps(message).encode(),
                    delivery_mode=aio_pika.DeliveryMode.PERSISTENT,
                    content_type='application/json',
                    headers={'message_type': action}  # 添加消息类型头
                ),
                routing_key=self.routing_key
            )
            
            logger.info(f"Sent message: {message}")
            
        except Exception as e:
            logger.error(f"Error sending message: {e}")
            raise

    async def close(self):
        if self._connection:
            await self._connection.close()
            self._connection = None
            self._channel = None
            logger.info("Closed RabbitMQ connection")