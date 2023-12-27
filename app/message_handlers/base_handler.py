from abc import ABC
from typing import Optional

from telebot.types import Message

from app.bot import Bot


class BaseHandler(ABC):
    REGEXP: str = ".+"
    PASS_BOT: bool = True
    CONTENT_TYPE: list = []

    bot: Bot
    message: Message

    @classmethod
    def exec(cls, message: Message, bot: Bot) -> None:
        cls._define_cls_vars(message, bot)

    @classmethod
    def _define_cls_vars(cls, message: Message, bot: Optional[Bot] = None) -> None:
        cls.bot = bot if cls.PASS_BOT else None
        cls.message = message

    @classmethod
    def trigger(cls, message: Message) -> bool:
        raise NotImplementedError(f"Trigger not set in handler '{cls.__name__}'")
