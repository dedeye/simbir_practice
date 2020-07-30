import uuid

from sqlalchemy import Column, MetaData, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base

metadata = MetaData(schema="users")

Base = declarative_base(metadata=metadata)


class User(Base):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    username = Column(String(200), unique=True, nullable=False)
    password = Column(String(100), nullable=False)
    role = Column(String(20), nullable=False)

    @classmethod
    async def create_user(self, conn, username, passhash, role):
        stmt = self.__table__.insert().values(
            id=uuid.uuid4(), username=username, password=passhash, role=role,
        )
        await conn.execute(stmt)

    @classmethod
    async def get_user(self, conn, username):
        table = self.__table__
        stmt = table.select().where(table.c.username == username)
        result = await conn.execute(stmt)
        return await result.fetchone()
