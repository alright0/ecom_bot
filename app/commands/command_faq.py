from telebot.types import Message

from app.bot import Bot
from app.commands import BaseCommand
from app.markup.markup_faq import markup_faq


class CommandFaq(BaseCommand):
    DESCRIPTION = "Часто задаваемые вопросы"
    COMMANDS = ["faq"]

    @classmethod
    def exec(cls, message: Message, bot: Bot):
        super().exec(message, bot)

        text = "Данный раздел может содержать ссылки на полезные материалы, видео и прочую полезную информацию"
        cls.bot.custom_reply_to(
            message=message,
            text=text,
            parse_mode="MARKDOWN",
            reply_markup=markup_faq(),
        )
