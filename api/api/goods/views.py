import json

from aiohttp import web

import api.auth.client as auth_client
from api.auth.decorator import use_auth
from api.goods import client

routes = web.RouteTableDef()


@routes.get("/goods/adv/all_tags/")
async def get_tags(request):
    result = await client.tag_list(request.query)
    return web.Response(
        status=result["status"], body=result["body"], headers=result["hdrs"]
    )


@routes.get("/goods/adv/")
@use_auth(required=False)
async def get_filtered(request, **kwargs):
    query = request.query.copy()

    if "author" in query and query["author"] == "me":
        if "user" not in kwargs:
            raise web.HTTPBadRequest(
                reason="author=me can only be used while authorized"
            )
        query["author"] = kwargs["user"]

    result = await client.adv_filtered(query)
    return web.Response(
        status=result["status"], body=result["body"], headers=result["hdrs"]
    )


@routes.post("/goods/adv/")
@use_auth(required=True)
async def post_adv(request, **kwargs):
    try:
        params = await request.json()
    except Exception:
        raise web.HTTPBadRequest(reason="invalid json")

    params["author"] = kwargs["user"]
    result = await client.adv_create(params)
    return web.Response(
        status=result["status"], body=result["body"], headers=result["hdrs"]
    )


async def adv_crud_by_id(request, method, kwargs):
    id = request.match_info["id"]

    if method != "GET":
        user = kwargs["user"]
        author = await client.adv_get_ad_author(id)
        if user != author:
            raise web.HTTPUnauthorized

    data = None
    if request.body_exists:
        try:
            data = await request.json()
        except Exception:
            raise web.HTTPBadRequest(reason="invalid json")

    if method == "PUT":
        data["author"] = kwargs["user"]

    return await client.adv_by_id(method, id, data=data)


@routes.get("/goods/adv/{id}/")
async def get_by_id(request, **kwargs):
    result = await adv_crud_by_id(request, "GET", kwargs)

    # next code seems pretty bad =(
    # check if we need to send mail views notification
    views = json.loads(result["body"])["views"]

    if (views % 10) == 0:
        id = json.loads(result["body"])["author"]
        email = await auth_client.login_by_id(id)
        # send mail
        mailing = request.app["mailing"]
        await mailing.send(email, "views_notify", {"views": views})

    return web.Response(
        status=result["status"], body=result["body"], headers=result["hdrs"]
    )


@routes.delete("/goods/adv/{id}/")
@use_auth(required=True)
async def del_by_id(request, **kwargs):
    result = await adv_crud_by_id(request, "DELETE", kwargs)
    return web.Response(
        status=result["status"], body=result["body"], headers=result["hdrs"]
    )


@routes.put("/goods/adv/{id}/")
@use_auth(required=True)
async def put_by_id(request, **kwargs):
    result = await adv_crud_by_id(request, "PUT", kwargs)
    return web.Response(
        status=result["status"], body=result["body"], headers=result["hdrs"]
    )


@routes.patch("/goods/adv/{id}/")
@use_auth(required=True)
async def patch_by_id(request, **kwargs):
    result = await adv_crud_by_id(request, "PATCH", kwargs)
    return web.Response(
        status=result["status"], body=result["body"], headers=result["hdrs"]
    )


@routes.post("/goods/adv/{id}/img/")
@use_auth(required=True)
async def post_img(request, **kwargs):
    id = request.match_info["id"]

    user = kwargs["user"]
    author = await client.adv_get_ad_author(id)
    if user != author:
        raise web.HTTPUnauthorized

    data_rcvd = await request.post()

    result = await client.adv_add_image(id, img=data_rcvd["file"], author=user)

    return web.Response(
        status=result["status"], body=result["body"], headers=result["hdrs"]
    )


@routes.get("/goods/img/{id}/")
async def get_img(request):
    id = request.match_info["id"]

    result = await client.img_by_id("GET", id)
    return web.Response(
        status=result["status"], body=result["body"], headers=result["hdrs"]
    )


@routes.delete("/goods/img/{id}/")
@use_auth(required=True)
async def delete_img(request, **kwargs):
    id = request.match_info["id"]

    user = kwargs["user"]
    author = await client.img_get_author(id)
    if user != author:
        raise web.HTTPUnauthorized

    result = await client.img_by_id("DELETE", id)
    return web.Response(
        status=result["status"], body=result["body"], headers=result["hdrs"]
    )
