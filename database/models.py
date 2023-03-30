from datetime import datetime

from peewee import (
    SqliteDatabase,
    Model,
    IntegerField,
    ForeignKeyField,
    TextField,
    DateTimeField
)

db = SqliteDatabase('history.db')


class BaseModel(Model):
    """
    This class describes the underlying database model.
    """
    class Meta:
        database = db


class User(BaseModel):
    """
    The class describes the table in which user IDs should be stored.
    """
    class Meta:
        db_table = 'users'

    user_id = IntegerField()


class UserRequest(BaseModel):
    """
    The class describes a table in which the history of user requests and responses for them should be stored.
    """
    class Meta:
        db_table = 'user_requests'

    user_id = ForeignKeyField(User, field='user_id')
    text = TextField()
    request = TextField()
    date = DateTimeField(default=datetime.now)
