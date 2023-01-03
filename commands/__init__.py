from typing import Any
from . import lowprice


def get(bot: Any):
    lowprice.bot_load(bot)
