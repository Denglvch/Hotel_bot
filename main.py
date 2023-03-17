from database.models import db, User, UserRequest
from loader import bot
import handlers


if __name__ == "__main__":
    db.create_tables([User, UserRequest])
    bot.infinity_polling()
