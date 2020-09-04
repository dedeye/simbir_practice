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
    if "jwt-token" in request:
        raise web.HTTPBadRequest(reason="Already Authorized")

    try:
        data = await request.json()
    except Exception:
        raise web.HTTPBadRequest(reason="invalid json")

    if "username" not in data:
        raise web.HTTPBadRequest(reason="username required")
    if "password" not in data:
        raise web.HTTPBadRequest(reason="password required")

    await users.register(
        db=request.app["db"],
        username=data["username"],
        password=data["password"],
        role="user",
    )

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

    if "jwt-token" in request:
        raise web.HTTPBadRequest(reason="Already Authorized")

    try:
        data = await request.json()
    except Exception:
        raise web.HTTPBadRequest(reason="invalid json")

    if "username" not in data:
        raise web.HTTPBadRequest(reason="username required")
    if "password" not in data:
        raise web.HTTPBadRequest(reason="password required")

    user_data = await users.login(
        db=request.app["db"], username=data["username"], password=data["password"]
    )

    pair = await jwt_pair.create(
        request=request, user=str(user_data.id), role=user_data.role
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

    try:
        data = await request.json()
    except Exception:
        raise web.HTTPBadRequest(reason="invalid json")

    if "refresh_token" not in data:
        data = {"error": "refresh token required"}
        return web.json_response(data=data, status=400)

    if "jwt_token" not in data:
        data = {"error": "jwt token required"}
        return web.json_response(data=data, status=400)

    result = await jwt_pair.refresh(
        request=request,
        jwt_token=data["jwt_token"],
        refresh_token=data["refresh_token"],
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

    if "jwt-token" not in request:
        raise web.HTTPForbidden(reason="No authorization header")

    await jwt_pair.revoke(request)
    return web.json_response(data={"result": "success"}, status=200)


async def login_taken(request):
    """
    ---
    description: This end-point return True if login is in use
    tags:
      - Auth
    produces:
      - application/json
    consumes:
      - "application/json"
    parameters:
      - name: "username"
        in: "path"
        required: true
        type: "string"
    """
    taken = await users.login_taken(request.app["db"], request.match_info["username"])
    return web.json_response(data={"taken": taken}, status=200)


async def get_login(request):
    """
    ---
    description: This end-point return login for user id
    tags:
      - Auth
    produces:
      - application/json
    consumes:
      - "application/json"
    parameters:
      - name: "id"
        in: "path"
        required: true
        type: "int"
    """
    uuid = request.match_info["id"]
    user = await users.get_username_by_id(request.app["db"], uuid)
    return web.json_response(data={"login": user.username}, status=200)
