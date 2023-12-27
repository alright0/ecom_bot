from telebot.types import Message

from app.bot import Bot
from app.commands import BaseCommand
from app.markup.markup_cources_list import markup_show_courses_list


class CommandShowCources(BaseCommand):
    DESCRIPTION = "Обучающие материалы"
    COMMANDS = ["courses"]

    @classmethod
    def exec(cls, message: Message, bot: Bot):
        super().exec(message, bot)

        text = "Данная команда может выдавать список материало, уже купленных и досупных к покупке."
        cls.bot.custom_reply_to(
            message=message,
            text=text,
            parse_mode="MARKDOWN",
            reply_markup=markup_show_courses_list(),
        )
