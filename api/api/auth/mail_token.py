import secrets

import aioredis

from api.settings import config

token_ttl = config.auth_mail_token_ttl


class MailToken:
    app = None
    redis = None

    async def setup(self, app):
        self.redis = await aioredis.create_redis_pool(config.get_api_redis_url())
        self.app = app

    async def cleanup(self, app):
        app["mail_token"].redis.close()
        await app["mail_token"].redis.wait_closed()

    def create_token(self):
        return secrets.token_hex(32)

    async def store_token(self, email, token):
        await self.redis.set(email, token)
        await self.redis.expire(email, token_ttl)

    async def remove_token(self, email):
        await self.redis.delete(email)

    async def token_is_valid(self, email, token):
        stored_token = await self.redis.get(email, encoding="utf-8")
        print(stored_token)
        print(token)
        if stored_token != token:
            print("neq")

        return stored_token == token


def init_mail_token(app):
    app["mail_token"] = MailToken()
    app.on_startup.append(app["mail_token"].setup)
    app.on_cleanup.append(app["mail_token"].cleanup)
