from aiohttp import web


class JwtPairNotFound(web.HTTPBadRequest):
    reason = "Jwt pair not found: jwt may be revoked or refresh token timed out"


class UserExistsException(web.HTTPBadRequest):
    reason = "User already exists"


class UserNotFoundException(web.HTTPBadRequest):
    reason = "User not found"


class WrongPasswordException(web.HTTPBadRequest):
    reason = "Wrong password"
