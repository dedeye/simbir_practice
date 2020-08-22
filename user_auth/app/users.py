from argon2 import PasswordHasher, exceptions

from user_auth.app.exceptions import (
    UserExistsException,
    UserNotFoundException,
    WrongPasswordException,
)
from user_auth.app.models import User

ph = PasswordHasher()


async def login(db, username, password):
    async with db.acquire() as conn:
        user_data = await User.get_user(conn, username=username)
        if not user_data:
            raise UserNotFoundException()

        try:
            ph.verify(user_data.password, password)

        except exceptions.VerifyMismatchError:
            raise WrongPasswordException()

        return user_data


async def register(db, username, password, role):
    async with db.acquire() as conn:
        user_data = await User.get_user(conn, username=username)
        if user_data:
            raise UserExistsException()

        passhash = ph.hash(password)

        await User.create_user(
            conn=conn, username=username, passhash=passhash, role=role
        )


async def login_taken(db, username):
    async with db.acquire() as conn:
        user = await User.get_user(conn, username=username)
        return not not user


async def get_username_by_id(db, uuid):
    async with db.acquire() as conn:
        return await User.get_user_by_id(conn, uuid=uuid)
