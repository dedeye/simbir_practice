import asyncio
import json

import aio_pika

from .mail import sendmail

connection = None


class MailQueue:
    def __init__(self):
        self.connection = None

    def run(self):
        loop = asyncio.get_event_loop()
        asyncio.create_task(self.reciever(loop))

    async def connect(self):
        self.connection = await aio_pika.connect_robust("amqp://guest:guest@rabbit/")

    async def reciever(self, loop):
        if not self.connection:
            await self.connect()

        queue_name = "mail_queue"
        channel = await self.connection.channel()
        queue = await channel.declare_queue(queue_name, auto_delete=True)

        async with queue.iterator() as queue_iter:

            async for message in queue_iter:
                async with message.process():
                    data = json.loads(message.body)
                    await sendmail(data["to"], data["template"], data["params"])

    async def publish(self, to, template, params):
        routing_key = "mail_queue"

        message_body = json.dumps({"to": to, "template": template, "params": params})

        channel = await self.connection.channel()  # type: aio_pika.Channel

        await channel.default_exchange.publish(
            aio_pika.Message(body=message_body.encode()), routing_key=routing_key,
        )


mail_queue = MailQueue()


def rabbit_init():
    mail_queue.run()
