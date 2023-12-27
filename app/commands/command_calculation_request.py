from telebot.types import Message

from app.bot import Bot
from app.commands import BaseCommand
from app.markup.markup_calculation_request import markup_calculation_request


class CommandCalcRequest(BaseCommand):
    DESCRIPTION = "Заявка на просчет стоимости услуг"
    COMMANDS = ["calculation"]

    phone = 0
    user_name = ""
    description = ""

    @classmethod
    def exec(cls, message: Message, bot: Bot):
        super().exec(message, bot)

        text = "Здесь вы можете составить заявку на просчет стоимости услуг.\n Укажите ваше имя"
        bot.send_custom_message(
            cls.message.chat.id,
            text,
        )

        bot.register_next_step_handler(message=message, callback=cls.set_number)

    @classmethod
    def set_number(cls, message):
        text = "Теперь укажите номер телефона"

        cls.user_name = message.text

        cls.bot.send_custom_message(cls.message.chat.id, text)
        cls.bot.register_next_step_handler(
            message=message,
            callback=cls.validate_number,
        )

    @classmethod
    def validate_number(cls, message):
        valid_len = 11
        phone_number = message.text.strip()
        try:
            phone_number = int(phone_number)
        except Exception:
            cls.bot.send_custom_message(
                cls.message.chat.id,
                "Номер телефона указан неверно. В сообщении должны быть только цифры. Попробуйте снова",
            )
            cls.bot.register_next_step_handler(
                message=message,
                callback=cls.validate_number,
            )
            return
        if not len(str(phone_number)) == valid_len:
            cls.bot.send_custom_message(
                cls.message.chat.id,
                f"Номер телефона указан неверно. Похоже, в нем {len(str(phone_number))} "
                f"символов, а не {valid_len}. Попробуйте еще раз",
            )
            cls.bot.register_next_step_handler(
                message=message,
                callback=cls.validate_number,
            )
            return

        cls.phone = message.text

        cls.bot.send_custom_message(
            cls.message.chat.id,
            "Теперь укажите описание заявки, пожелания и/или требования",
        )
        cls.bot.register_next_step_handler(
            message=message,
            callback=cls.set_description,
        )

    @classmethod
    def set_description(cls, message):
        cls.description = message.text

        cls.bot.send_custom_message(
            cls.message.chat.id,
            f"Имя: {cls.user_name}\n"
            f"Номер телеофна: {cls.phone}\n"
            f"Описание: {cls.description}",
            parse_mode=None,
            reply_markup=markup_calculation_request(),
        )
