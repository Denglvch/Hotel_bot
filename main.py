from database.models import db, User, UserRequest, UserMessage
from loader import bot
import handlers


if __name__ == "__main__":
    db.create_tables([User, UserRequest, UserMessage])
    User(user_id=bot.get_me().id).save()
    bot.infinity_polling()
