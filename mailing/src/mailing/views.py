from pydantic import BaseModel, EmailStr

from fastapi import APIRouter, HTTPException

from .models import Template

router = APIRouter()


@router.get("/template/{id}/")
async def get_template(id: str):
    template = await Template.get_or_404(id)
    return template.to_dict()


@router.get("/template/by_name/{name}")
async def get_template_by_name(name: str):
    template = await Template.get_by_name(name)
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
    created = await Template.create(
        name=template.name, text=template.text, subject=template.subject
    )
    return created.to_dict()


@router.delete("/template/{id}")
async def delete_template(id: str):
    template = await Template.get_or_404(id)
    await template.delete()
    return dict(id=id)


@router.get("/templates/")
async def get_all_templates():
    templates = await Template.query.gino.all()
    return [temp.to_dict() for temp in templates]


def init_app(app):
    app.include_router(router, prefix="/api/v1")
