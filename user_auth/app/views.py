from aiohttp import web

import user_auth.app.jwt_pair as jwt_pair
import user_auth.app.users as users


async def register(request):
    """
    ---
    description: This end-point allow to register new user.
    tags:
    - Auth
    produces:
    - text/plain
    consumes:
      - "application/json"
    parameters:
      - in: header
        name: "Authorization"
        required: false
        schema:
          type: "string"
        description: "User's JWT. type 'Bearer' before JWT"


      - in: "body"
        name: "body"
        required: true
        schema:
          type: object
          properties:
            "username":
                "type": "string"    
                "description": "User's username"
                "default": "John"
            "password":
                "type": "string"    
                "description": "User's password"
                "default": "password"
    """
    if request.method == "POST":
        if "jwt-token" in request:
            raise web.HTTPBadRequest(reason="Already Authorized")

        try:
            data = await request.json()
        except Exception:
            return web.json_response(data={"error": "invalid json data"}, status=400)

        if "username" not in data:
            return web.json_response(data={"error": "username required"}, status=400)
        if "password" not in data:
            return web.json_response(data={"error": "password required"}, status=400)

        try:
            await users.register(
                db=request.app["db"],
                username=data["username"],
                password=data["password"],
                role="user",
            )
        except users.UserExistsException:
            raise web.HTTPBadRequest(reason="Username taken")

        return web.json_response(data={"result": "success"}, status=200)


async def login(request):
    """
    ---
    description: This end-point allow to log in .
    tags:
    - Auth
    produces:
    - application/json
    consumes:
      - application/json
    parameters:
      - in: header
        name: "Authorization"
        required: false
        schema:
          type: "string"
        description: "User's JWT. type 'Bearer' before JWT"


      - in: "body"
        name: "body"
        required: true
        schema:
          type: object
          properties:
            "username":
                "type": "string"    
                "description": "User's username"
                "default": "John"
            "password":
                "type": "string"    
                "description": "User's password"
                "default": "password"
    """
    if request.method == "POST":
        if "jwt-token" in request:
            raise web.HTTPBadRequest(reason="Already Authorized")

        try:
            data = await request.json()
        except Exception:
            return web.json_response(data={"error": "invalid json data"}, status=400)

        if "username" not in data:
            return web.json_response(data={"error": "username required"}, status=400)
        if "password" not in data:
            return web.json_response(data={"error": "password required"}, status=400)

        try:
            user_data = await users.login(
                db=request.app["db"],
                username=data["username"],
                password=data["password"],
            )
        except (users.UserExistsException, users.WrongPasswordException):
            return web.HTTPBadRequest(reason="wrong login or password")

        pair = await jwt_pair.create(
            request=request, user=data["username"], role=user_data.role
        )

        return web.json_response(data=pair, status=200)


async def validate(request):
    """
    ---
    description: This end-point avalidates the token and returns it payload.
    tags:
        - Auth
    produces:
        - application/json
    consumes:
      - application/json
    parameters:
      - in: header
        name: "Authorization"
        required: false
        schema:
          type: "string"
        description: "User's JWT. type 'Bearer' before JWT"
    """
    if request.method == "GET":
        if "jwt-token" not in request:
            raise web.HTTPForbidden(reason="No authorization header")

        token = request["jwt-token"]
        return web.json_response(data=token, status=200)


async def refresh(request):
    """
    ---
    description: This end-point revokes old jwt-pair and generates new
    tags:
        - Auth
    produces:
        - application/json
    parameters:
      - in: header
        name: "Authorization"
        required: false
        schema:
          type: "string"
        description: "User's JWT. type 'Bearer' before JWT"

        
      - in: "body"
        name: "body"
        required: true
        schema:
          type: object
          properties:
            "jwt_token":
                "type": "string"    
                "description": "User's jwt"

            "refresh_token":
                "type": "string"    
                "description": "User's refresh token"

    """
    if request.method == "POST":
        try:
            data = await request.json()
        except Exception:
            return web.Response(text="nok", status=400)

        if "refresh_token" not in data:
            data = {"error": "refresh token required"}
            return web.json_response(data=data, status=400)

        if "jwt_token" not in data:
            data = {"error": "jwt token required"}
            return web.json_response(data=data, status=400)

        try:
            result = await jwt_pair.refresh(
                request=request,
                jwt_token=data["jwt_token"],
                refresh_token=data["refresh_token"],
            )
        except jwt_pair.JwtPairNotFound:
            web.HTTPBadRequest(
                reason="JWT Pair not found, refresh token may be expired"
            )

        return web.json_response(data=result, status=200)


async def logout(request):
    """
    ---
    description: This end-point logs user out ad invalidates jwt-pair.
    tags:
        - Auth
    produces:
        - application/json
    consumes:
      - application/json
    parameters:
      - in: header
        name: "Authorization"
        required: false
        schema:
          type: "string"
        description: "User's JWT. type 'Bearer' before JWT"

    """
    if request.method == "GET":
        if "jwt-token" not in request:
            raise web.HTTPForbidden(reason="No authorization header")

        await jwt_pair.revoke(request)
        return web.json_response(data={"result": "success"}, status=200)
