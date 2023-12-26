from abc import ABC
from typing import Any, Optional

from telebot.types import CallbackQuery

from app.bot import Bot
from app.dao import ChatDao, UserDao
from app.models import Chat, User


class BaseCallback(ABC):
    PASS_BOT: bool = True
    bot: Optional[Bot] = None
    call: CallbackQuery
    data: Any = None
    chat_dao: ChatDao = ChatDao()
    user_dao: UserDao = UserDao()
    chat: Chat
    user: User

    @classmethod
    def exec(cls, call: CallbackQuery, bot: Optional[Bot]) -> None:
        cls._define_cls_vars(call, bot)

    @classmethod
    def _define_cls_vars(cls, call: CallbackQuery, bot: Optional[Bot] = None) -> None:
        cls.bot = bot if cls.PASS_BOT else None
        cls.call = call
        cls.data = call.data
        cls.chat, _ = cls.chat_dao.get_or_create(cls.call.message.chat)
        cls.user, _ = cls.user_dao.create_or_update(cls.call.from_user)

    @classmethod
    def trigger(cls, call: CallbackQuery) -> bool:
        raise NotImplementedError("Callback trigger not set")
