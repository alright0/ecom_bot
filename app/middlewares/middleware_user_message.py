from telebot.types import Message as TelegramMessage

from app.bot import Bot
from app.middlewares import BaseMiddleware


class MiddlewareUserMessage(BaseMiddleware):
    UPDATE_TYPES = ["message"]

    @classmethod
    def exec(cls, bot: Bot, message: TelegramMessage) -> None:
        super().exec(bot, message)
