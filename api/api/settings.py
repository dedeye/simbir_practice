from pydantic import BaseSettings
from pydantic.fields import Field

__all__ = ["config"]


class Config(BaseSettings):
    auth_hostname: str = Field(..., env="AUTH_HOSTNAME", required=True)
    auth_port: int = Field(..., env="AUTH_PORT", requierd=True)
    auth_prefix: str = Field(..., env="AUTH_PREFIX", required=True)

    auth_mail_token_ttl: int = Field(
        name="auth_mail_token_ttl", default=20 * 60 * 60, env="AUTH_MAIL_TOKEN_TTL"
    )

    def get_auth_url_base(self):
        return "http://{}:{}/{}".format(
            self.auth_hostname, self.auth_port, self.auth_prefix
        )

    goods_hostname: str = Field(..., env="GOODS_HOSTNAME", required=True)
    goods_port: int = Field(..., env="GOODS_PORT", requierd=True)
    goods_prefix: str = Field(..., env="GOODS_PREFIX", required=True)

    def get_goods_url_base(self):
        return "http://{}:{}/{}".format(
            self.goods_hostname, self.goods_port, self.goods_prefix
        )

    mail_hostname: str = Field(..., env="MAIL_HOSTNAME", required=True)
    mail_port: int = Field(..., env="MAIL_PORT", requierd=True)
    mail_prefix: str = Field(..., env="MAIL_PREFIX", required=True)

    def get_mail_url_base(self):
        return "http://{}:{}/{}".format(
            self.mail_hostname, self.mail_port, self.mail_prefix
        )

    mail_rabbit_user: str = Field(
        name="mail_rabbit_user", default="guest", env="MAIL_RABBIT_USER"
    )
    mail_rabbit_pass: str = Field(
        name="mail_rabbit_pass", default="guest", env="MAIL_RABBIT_PASS"
    )

    def get_mail_rabbit_url(self):
        return "amqp://{}:{}@rabbit/".format(
            self.mail_rabbit_user, self.mail_rabbit_pass
        )

    monitor_rabbit_user: str = Field(
        name="monitor_rabbit_user", default="guest", env="MONITOR_RABBIT_USER"
    )
    monitor_rabbit_pass: str = Field(
        name="monitor_rabbit_pass", default="guest", env="MONITOR_RABBIT_PASS"
    )
    monitor_task: str = Field(
        name="monitor_task", default="monitoring.tasks.store_event", env="MONITOR_TASK"
    )

    def get_monitor_rabbit_url(self):
        return "amqp://{}:{}@rabbit/".format(
            self.monitor_rabbit_user, self.monitor_rabbit_pass
        )

    api_redis_host: str = Field(
        name="api_redis_host", default="redis-api", env="API_REDIS_HOST"
    )

    def get_api_redis_url(self):
        return "redis://{}".format(self.api_redis_host)


config = Config()
