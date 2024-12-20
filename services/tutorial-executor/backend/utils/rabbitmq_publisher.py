import aio_pika
import toml

async def publish_to_rabbitmq(task_data):
    """Publish task data to RabbitMQ."""
    connection = await aio_pika.connect_robust("amqp://guest:guest@localhost/")
    async with connection:
        channel = await connection.channel()
        exchange = await channel.declare_exchange('tasks', aio_pika.ExchangeType.DIRECT)
        message_body = task_data.encode()  # Convert the data to bytes
        message = aio_pika.Message(body=message_body)
        await exchange.publish(message, routing_key='task_queue')