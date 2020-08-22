import json
from typing import Optional

import aio_pika
import aiohttp
from pydantic import BaseModel

from api.settings import config

mail_rabbit_str = config.get_mail_rabbit_url()

BASE_URL = config.get_mail_url_base()


class MailTemplate(BaseModel):
    name: str
    subject: str
    text: str
    id: Optional[str]


class Mailing:
    templates = {
        "mail_token": MailTemplate(
            name="mail_token",
            subject="Here is your registration token",
            text="Your registration token is:\n"
            "{token}\n"
            "may be some day here will be a magic link, but dont bother waiting",
        ),
        "views_notify": MailTemplate(
            name="views_notify",
            subject="Your ad is getting more popular!",
            text="Your ad has just reacher {views} views!\nPretty cool, isnt it?",
        ),
    }

    def __init__(self, queue_name):
        self.conn = None
        self.queue_name = queue_name

    async def setup(self, app):
        self.conn = await aio_pika.connect_robust(mail_rabbit_str)
        await self.template_update_all()

    async def template_get(self, template_name):
        async with aiohttp.ClientSession() as session:
            url = BASE_URL + "template/" + "by_name/" + template_name
            async with session.get(url) as resp:
                if resp.status != 200:
                    return None

                data = await resp.text()
                return MailTemplate.parse_raw(data)

    async def template_delete(self, id):
        async with aiohttp.ClientSession() as session:
            url = BASE_URL + "template/" + id
            async with session.delete(url) as resp:
                if resp.status != 200:
                    raise Exception

    async def template_add(self, template):
        async with aiohttp.ClientSession() as session:
            url = BASE_URL + "template/"
            async with session.post(url, data=template.json()) as resp:
                if resp.status != 200:
                    raise Exception

    async def template_update(self, template):
        stored = await self.template_get(template.name)
        if (
            not stored
            or stored.subject != template.subject
            or stored.text != template.text
        ):
            if stored:
                await self.template_delete(stored.id)

            await self.template_add(template)

    async def template_update_all(self):
        for key in self.templates:
            await self.template_update(self.templates[key])

    async def send(self, to, template_name, params):
        channel = await self.conn.channel()

        message_body = json.dumps(
            {"to": to, "template": template_name, "params": params}
        )
        await channel.default_exchange.publish(
            aio_pika.Message(body=message_body.encode()), routing_key=self.queue_name,
        )


def mailing_init(app):
    app["mailing"] = Mailing("mail_queue")
    app.on_startup.append(app["mailing"].setup)
