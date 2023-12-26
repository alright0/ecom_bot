import json
import re
from abc import ABC
from typing import List, Union

from telebot.types import Message

from app.bot import Bot


class BaseCommand(ABC):
    DESCRIPTION = ""
    COMMANDS: List[str] = []
    COMMAND_REGEX: Union[str] = None
    HIDDEN = False
    PASS_BOT = True
    OWNER_ONLY = False

    bot: Bot
    message: Message

    @classmethod
    def exec(cls, message: Message, bot: Bot) -> None:
        cls._check_owner(message, bot)
        cls._define_cls_vars(message, bot)

    @classmethod
    def _define_cls_vars(cls, message: Message, bot: Bot) -> None:
        cls.message = message
        cls.bot = bot

    @classmethod
    def clean_command(cls, command: str) -> str:
        for c in cls.COMMANDS:
            command = re.sub(rf"\/{c}.*?(\s|$)", "", command)
        return command.strip()

    @classmethod
    def _check_owner(cls, message: Message, bot: Bot):
        if not cls.OWNER_ONLY:
            return
        if message.from_user.id != bot.owner_id:
            message_json = json.dumps(message.json, indent=2, ensure_ascii=False)
            text = (
                f"Кто-то пытается получить доступ к команде /{cls.COMMANDS[0]}\n"
                "Сообщение:\n"
                f"{message_json}"
            )
            raise OwnerException(text)


class SimpleCommand(BaseCommand):
    TEXT = ""
    markup = None

    @classmethod
    def exec(cls, message: Message, bot: Bot) -> None:
        super().exec(message, bot)

        bot.custom_reply_to(
            message=message,
            text=cls.TEXT,
            reply_markup=cls.markup,
            parse_mode="MARKDOWN",
        )


class OwnerException(Exception):
    ...
