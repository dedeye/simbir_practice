import secrets
from datetime import datetime, timedelta
from math import ceil

import aioredis
import jwt
from aiohttp_jwt import JWTMiddleware

JWT_SECRET = "secret"
JWT_ALGORITHM = "HS256"
JWT_TTL = 20 * 60
RFR_TTL = 20 * 60 * 60


class JwtPairNotFound(Exception):
    pass


async def init_storage(app):
    redis = await aioredis.create_redis_pool("redis://redis")
    app["redis"] = redis


async def close_storage(app):
    app["redis"].close()
    await app["redis"].wait_closed()


async def create(request, user, role):

    jwt_exp = ceil((datetime.utcnow() + timedelta(seconds=JWT_TTL)).timestamp())
    refresh_exp = ceil((datetime.utcnow() + timedelta(seconds=RFR_TTL)).timestamp())

    jwt_payload = {
        "user": user,
        "role": role,
        "exp": jwt_exp,
    }

    jwt_token = jwt.encode(jwt_payload, JWT_SECRET, JWT_ALGORITHM)
    refresh_token = secrets.token_hex(32)

    redis = request.app["redis"]
    await redis.set(jwt_token, refresh_token)
    await redis.expireat(jwt_token, refresh_exp)

    return {
        "jwt": {"token": jwt_token.decode(), "expire": jwt_exp},
        "refresh": {"token": refresh_token, "expire": refresh_exp},
    }


async def revoke(request, jwt=None):
    if not jwt:
        jwt = request["jwt-encoded"]

    redis = request.app["redis"]
    await redis.delete(jwt)


async def is_revoked(request, decoded):
    redis = request.app["redis"]
    # middleware does not provide encoded token, so get it from header
    _, token = request.headers.get("Authorization").strip().split(" ")
    exists = await redis.exists(token)
    return exists == 0


async def refresh(request, jwt_token, refresh_token):
    redis = request.app["redis"]

    refresh_stored = await redis.get(jwt_token, encoding="utf-8")
    if refresh_token != refresh_stored:
        raise JwtPairNotFound()

    await revoke(request, jwt_token)

    data = jwt.decode(jwt_token, JWT_SECRET, verify=False, algorithms=[JWT_ALGORITHM])

    return await create(request, data["user"], data["role"])


def middleware(whitelist):
    return JWTMiddleware(
        JWT_SECRET,
        request_property="jwt-token",
        credentials_required=False,
        algorithms="HS256",
        whitelist=whitelist,
        store_token="jwt-encoded",
        is_revoked=is_revoked,
    )
