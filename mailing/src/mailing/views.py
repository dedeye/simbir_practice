from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr

from .models import Template
from .rabbit import mail_queue

router = APIRouter()


@router.get("/template/{id}/")
async def get_template(id: str):
    template = await Template.get_or_404(id)
    return template.to_dict()


@router.get("/template/by_name/{name}")
async def get_template_by_name(name: str):
    template = await Template.query.where(Template.name == name).gino.first()
    if not template:
        raise HTTPException(status_code=404, detail="Item not found")
    return template.to_dict()


class TemplateModel(BaseModel):
    name: str
    subject: str
    text: str


class MailModel(BaseModel):
    temp_name: str
    address: EmailStr
    params: dict


@router.post("/template/")
async def add_template(template: TemplateModel):
    rv = await Template.create(
        name=template.name, text=template.text, subject=template.subject
    )
    return rv.to_dict()


@router.delete("/template/{id}")
async def delete_template(id: str):
    template = await Template.get_or_404(id)
    await template.delete()
    return dict(id=id)


@router.get("/templates/")
async def get_all_templates():
    templates = await Template.query.gino.all()
    return [temp.to_dict() for temp in templates]


@router.post("/send_mail/")
async def send_mail(mail: MailModel):
    await mail_queue.publish(mail.address, mail.temp_name, mail.params)


def init_app(app):
    app.include_router(router, prefix="/api/v1")
