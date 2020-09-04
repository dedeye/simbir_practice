from email.message import EmailMessage

import aiosmtplib

from . import config
from .models import Template


async def sendmail(to, template, params):

    template = await Template.get_by_name(template)

    if not template:
        # write error to log here?
        return

    message = EmailMessage()
    message["From"] = config.MAIL_ADDRESS
    message["To"] = to

    try:
        message["Subject"] = template.subject.format(**params)
        message.set_content(template.text.format(**params))
    except Exception:
        # write error to log here?
        return

    await aiosmtplib.send(message, hostname="smtp", port=25)
