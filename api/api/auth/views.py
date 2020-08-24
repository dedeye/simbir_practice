from aiohttp import web
from pydantic import BaseModel, EmailStr, ValidationError

from api.auth import client


class LoginModel(BaseModel):
    login: EmailStr
    password: str


class RequestRegisterTokenModel(BaseModel):
    email: EmailStr


class RegisterModel(BaseModel):
    login: EmailStr
    token: str
    password: str


class RefreshJWTModel(BaseModel):
    jwt: str
    refresh: str


routes = web.RouteTableDef()


@routes.post("/auth/login/")
async def login(request):
    try:
        data = LoginModel.parse_raw(await request.text())
    except ValidationError:
        raise web.HTTPBadRequest

    result = await client.login(data.login, data.password)

    return web.Response(
        status=result["status"], body=result["body"], headers=result["hdrs"]
    )


@routes.post("/auth/register/")
async def register(request):
    try:
        data = RegisterModel.parse_raw(await request.text())
    except ValidationError:
        raise web.HTTPBadRequest

    # check token
    mail_token = request.app["mail_token"]
    valid = await mail_token.token_is_valid(data.login, data.token)
    if not valid:
        raise web.HTTPBadRequest(reason="invalid token")

    result = await client.register(login=data.login, password=data.password)
    return web.Response(
        status=result["status"], body=result["body"], headers=result["hdrs"]
    )


@routes.post("/auth/request_register_token/")
async def request_register_token(request):

    try:
        data = RequestRegisterTokenModel.parse_raw(await request.text())
    except ValidationError:
        raise web.HTTPBadRequest

    # check login free
    login_taken = await client.login_taken(data.email)

    # send token only if login is free
    if not login_taken:
        # generate token
        mail_token = request.app["mail_token"]
        token = mail_token.create_token()
        await mail_token.store_token(data.email, token)

        # send mail
        mailing = request.app["mailing"]
        await mailing.send(data.email, "mail_token", {"token": token})

    return web.Response(text="ok ", status=200)


@routes.post("/auth/refresh/")
async def refresh(request):
    try:
        data = RefreshJWTModel.parse_raw(await request.text())
    except ValidationError:
        raise web.HTTPBadRequest

    result = await client.refresh(data.jwt, data.refresh)

    return web.Response(
        status=result["status"], body=result["body"], headers=result["hdrs"]
    )


@routes.post("/auth/logout/")
async def logout(request):
    if "Authorization" not in request.headers:
        raise web.HTTPUnauthorized

    result = await client.logout(request.headers["Authorization"])
    return web.Response(
        status=result["status"], body=result["body"], headers=result["hdrs"]
    )
