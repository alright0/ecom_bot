from telebot.types import Message

from app.bot import Bot
from app.commands import BaseCommand


class CommandStart(BaseCommand):
    DESCRIPTION = "Главное меню"
    COMMANDS = ["start"]

    @classmethod
    def exec(cls, message: Message, bot: Bot):
        super().exec(message, bot)

        text = (
            f"Добрый день!\n\nЯ - бот, созданный для демонстрации возможностей автоматизации Вашего бизнеса.\n\n"
            f"Вот что я умею:\n{cls._get_commands()}"
        )
        bot.send_custom_message(message.chat.id, text)

    @staticmethod
    def _get_commands():
        from app.commands import COMMANDS

        substr_list = [
            f"/{c.COMMANDS[0]} - {c.DESCRIPTION}" for c in COMMANDS if not c.HIDDEN
        ]
        return "\n".join(substr_list)
