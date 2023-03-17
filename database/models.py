from datetime import datetime

from peewee import *

db = SqliteDatabase('history.db')


class BaseModel(Model):
    class Meta:
        database = db


class User(BaseModel):
    class Meta:
        db_table = 'users'

    user_id = IntegerField()


class UserRequest(BaseModel):
    class Meta:
        db_table = 'user_requests'

    user_id = ForeignKeyField(User)
    date = DateTimeField(default=datetime.now)
    request = TextField()