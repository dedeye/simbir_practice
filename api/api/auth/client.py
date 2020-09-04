import aiohttp

from api.settings import config

URL_BASE = config.get_auth_url_base()


async def login(login, password):
    data = {"username": login, "password": password}
    url = URL_BASE + "login/"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            return {
                "status": resp.status,
                "body": await resp.read(),
                "hdrs": resp.headers,
            }


async def register(login, password):
    data = {"username": login, "password": password}
    url = URL_BASE + "register/"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            return {
                "status": resp.status,
                "body": await resp.read(),
                "hdrs": resp.headers,
            }


async def login_taken(login):
    url = URL_BASE + "login_taken/" + login + "/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            result = await resp.json()
            return result["taken"]


async def validate(hdrs, required):
    url = URL_BASE + "validate/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=hdrs) as resp:
            if resp.status == 200:
                return await resp.json()
            elif required:
                raise aiohttp.web.HTTPUnauthorized


async def refresh(jwt, refresh):
    data = {"jwt_token": jwt, "refresh_token": refresh}
    url = URL_BASE + "refresh/"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=data) as resp:
            return {
                "status": resp.status,
                "body": await resp.read(),
                "hdrs": resp.headers,
            }


async def logout(auth):
    url = URL_BASE + "logout/"
    headers = {"Authorization": auth}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, headers=headers) as resp:
            return {
                "status": resp.status,
                "body": await resp.read(),
                "hdrs": resp.headers,
            }


async def login_by_id(id):
    url = URL_BASE + "login_by_id/" + id + "/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            result = await resp.json()
            return result["login"]
