import os

DATABASE = {
    "NAME": os.environ.get("SQL_DATABASE"),
    "USER": os.environ.get("SQL_USER"),
    "PASSWORD": os.environ.get("SQL_PASSWORD"),
    "HOST": os.environ.get("SQL_HOST"),
    "PORT": os.environ.get("SQL_PORT"),
}

DATABASE_URL = "postgres://{}:{}@{}:{}/{}".format(
    DATABASE["USER"],
    DATABASE["PASSWORD"],
    DATABASE["HOST"],
    DATABASE["PORT"],
    DATABASE["NAME"],
)


JWT = {
    "SECRET": os.environ.get("JWT_SECRET"),
    "ALGORITHM": os.environ.get("JWT_ALGORITM", "HS256"),
    "TTL": int(os.environ.get("JWT_TTL", 20 * 60)),
    "REFRESH_TOKEN_TTL": int(os.environ.get("REFRESH_TOKEN_TTL", 20 * 60 * 60)),
}
