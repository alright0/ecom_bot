from telebot.types import Message

from app.bot import Bot
from app.commands import BaseCommand
from app.markup.markup_calculation_request import markup_calculation_request


class CommandCalcRequest(BaseCommand):
    DESCRIPTION = "Заявка на просчет стоимости услуг"
    COMMANDS = ["calculation_request"]

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
        print("in set number")
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
        cls.bot.send_custom_message(
            cls.message.chat.id,
            "Имя: Тестовый пользователь\n"
            "Номер телеофна: 9991234567\n"
            "Описание: Тестовое описание",
            parse_mode=None,
            reply_markup=markup_calculation_request(),
        )
