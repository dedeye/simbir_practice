from argon2 import PasswordHasher, exceptions

from user_auth.app.db import create_user, get_user

ph = PasswordHasher()


class UserExistsException(Exception):
    pass


class UserNotFoundException(Exception):
    pass


class WrongPasswordException(Exception):
    pass


async def login(db, username, password):
    async with db.acquire() as conn:
        user_data = await get_user(conn, username=username)
        if not user_data:
            raise UserExistsException()

        try:
            ph.verify(user_data.password, password)

        except exceptions.VerifyMismatchError:
            raise WrongPasswordException()

        return user_data


async def register(db, username, password, role):
    async with db.acquire() as conn:
        user_data = await get_user(conn, username=username)
        if user_data:
            raise UserExistsException()

        passhash = ph.hash(password)

        await create_user(conn=conn, username=username, passhash=passhash, role=role)
