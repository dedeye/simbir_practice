import asyncio
import json

import aio_pika

from .mail import sendmail

connection = None


class MailQueue:
    def __init__(self, queue_name):
        self.__connection = None
        self.queue_name = queue_name

    def run(self):
        # loop = asyncio.get_event_loop()
        asyncio.create_task(self.reciever())

    # retuns current connection, creates one if needed
    async def get_connection(self):
        if not self.__connection:
            self.__connection = await aio_pika.connect_robust(
                "amqp://guest:guest@rabbit/"
            )
        return self.__connection

    async def process_message(self, message: aio_pika.IncomingMessage):
        async with message.process():
            data = json.loads(message.body)
            await sendmail(data["to"], data["template"], data["params"])

    async def reciever(self):
        connection = await self.get_connection()

        channel = await connection.channel()
        queue = await channel.declare_queue(self.queue_name, auto_delete=True)

        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                await self.process_message(message)


mail_queue = MailQueue("mail_queue")


def rabbit_init():
    mail_queue.run()
