import os

from pydantic import BaseSettings
from pydantic.fields import Field

__all__ = ["config"]


class Config(BaseSettings):
    db_name: str = Field(..., env="SQL_DATABASE", required=True)
    db_user: str = Field(..., env="SQL_USER", required=True)
    db_pass: str = Field(..., env="SQL_PASSWORD", required=True)
    db_host: str = Field(..., env="SQL_HOST", required=True)
    db_port: int = Field(..., env="SQL_PORT", required=True)

    def get_db_url(self):
        return "postgres://{}:{}@{}:{}/{}".format(
            self.db_user, self.db_pass, self.db_host, self.db_port, self.db_name
        )

    jwt_secret: str = Field(..., env="JWT_SECRET", required=True)
    jwt_algo: str = Field(name="jwt_algo", default="HS256", env="JWT_ALGORITHM")
    jwt_ttl: int = Field(name="jwt_ttl", default=20 * 60, env="JWT_TTL")
    jwt_refresh_ttl: int = Field(
        name="refresh_ttl", default=20 * 60 * 60, env="REFRESH_TOKEN_TTL"
    )


config = Config()