from functools import wraps

from api.auth.client import validate


def use_auth(required=False):
    def decorator(f):
        @wraps(f)
        async def wrapper(request, *args, **kwds):

            hdrs = request.headers
            userdata = await validate(hdrs, required)
            if userdata:
                kwds.update(userdata)

            return await f(request, *args, **kwds)

        return wrapper

    return decorator
