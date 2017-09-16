from slim.utils import async_run
import config

# asyncpg 配置

import asyncpg

asyncpg_conn = None


def asyncpg_init(db_uri):
    async def create_conn(db_uri):
        global asyncpg_conn
        asyncpg_conn = await asyncpg.connect(db_uri)

    async_run(create_conn)


asyncpg_init(config.DATABASE_URI)

# peewee 配置

import peewee
from playhouse.db_url import connect
from playhouse.shortcuts import model_to_dict

db = connect(config.DATABASE_URI)


class BaseModel(peewee.Model):
    class Meta:
        database = db

    def to_dict(self):
        return model_to_dict(self)

    @classmethod
    def get_by(cls, *exprs):
        try:
            return cls.get(*exprs)
        except cls.DoesNotExist:
            return

    @classmethod
    def get_by_pk(cls, value):
        try:
            return cls.get(cls._meta.primary_key == value)
        except cls.DoesNotExist:
            return

    @classmethod
    def exists_by_pk(cls, value):
        return cls.select().where(cls._meta.primary_key == value).exists()
