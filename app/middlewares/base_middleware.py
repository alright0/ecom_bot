from telebot.types import Message as TelegramMessage

from app.bot import Bot
from app.dao import ChatDao, MessageDao, UserDao
from app.models import Chat, Message, User

# update_types = [
#     "message",
#     "edited_message",
#     "channel_post",
#     "edited_channel_post",
#     "inline_query",
#     "chosen_inline_result",
#     "callback_query",
#     "shipping_query",
#     "pre_checkout_query",
#     "poll", "poll_answer",
#     "my_chat_member",
#     "chat_member",
#     "chat_join_request",
# ]


class BaseMiddleware:
    UPDATE_TYPES: list[str] = None

    bot: Bot = None
    message: TelegramMessage = None

    user_dao = UserDao()
    chat_dao = ChatDao()
    message_dao = MessageDao()

    user: User
    chat: Chat
    msg: Message

    @classmethod
    def exec(cls, bot: Bot, message: TelegramMessage) -> None:
        cls._prepare_args(bot, message)

    @classmethod
    def _prepare_args(cls, bot: Bot, message: TelegramMessage) -> None:
        if not cls.UPDATE_TYPES:
            raise NotImplementedError(
                f"UPDATE_TYPES not set for middleware '{cls.__name__}'",
            )

        cls.bot = bot
        cls.message = message
        cls.user, _ = cls.user_dao.create_or_update(cls.message.from_user)
        cls.chat, _ = cls.chat_dao.create_or_update(cls.message.chat)
        cls.msg, _ = cls.message_dao.create_or_update(cls.message, cls.chat, cls.user)

    @classmethod
    def _check_its_me(cls, user_id: int) -> bool:
        return cls.bot.get_me().id == user_id
