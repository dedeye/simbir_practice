import aiohttp

from api.settings import config

URL_BASE = config.get_goods_url_base()


async def adv_list(params):
    url = URL_BASE + "advert/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return {
                "status": resp.status,
                "body": await resp.read(),
                "hdrs": resp.headers,
            }


async def adv_filtered(params):
    url = URL_BASE + "advert/filter/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return {
                "status": resp.status,
                "body": await resp.read(),
                "hdrs": resp.headers,
            }


async def tag_list(params):
    url = URL_BASE + "advert/all_tags/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as resp:
            return {
                "status": resp.status,
                "body": await resp.read(),
                "hdrs": resp.headers,
            }


async def adv_create(params):
    url = URL_BASE + "advert/"
    async with aiohttp.ClientSession() as session:
        async with session.post(url, json=params) as resp:
            return {
                "status": resp.status,
                "body": await resp.read(),
                "hdrs": resp.headers,
            }


async def adv_by_id(method, id, data=None):
    url = URL_BASE + "advert/" + id + "/"
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, json=data) as resp:
            return {
                "status": resp.status,
                "body": await resp.read(),
                "hdrs": resp.headers,
            }


async def adv_get_ad_author(id):
    url = URL_BASE + "advert/" + id + "/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                ad = await resp.json()
                return ad["author"]
            else:
                return None


async def adv_add_image(id, img, author):
    url = URL_BASE + "advert/" + id + "/img/"
    data = aiohttp.FormData()
    data.add_field(name="author", value=author)

    data.add_field(name="file", value=img.file, filename=img.filename)

    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as resp:
            return {
                "status": resp.status,
                "body": await resp.read(),
                "hdrs": resp.headers,
            }


async def img_by_id(method, id, data=None):
    url = URL_BASE + "img/" + id + "/"
    async with aiohttp.ClientSession() as session:
        async with session.request(method, url, json=data) as resp:
            return {
                "status": resp.status,
                "body": await resp.read(),
                "hdrs": resp.headers,
            }


async def img_get_author(id):
    url = URL_BASE + "img/" + id + "/"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status == 200:
                img = await resp.json()
                return img["author"]
            else:
                return None
