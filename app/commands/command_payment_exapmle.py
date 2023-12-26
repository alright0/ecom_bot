from telebot.types import LabeledPrice, Message

from app.bot import Bot
from app.commands import BaseCommand
from app.config import config as c


class CommandPaymentExample(BaseCommand):
    DESCRIPTION = "Тестовые покупки"
    COMMANDS = ["payment"]

    @classmethod
    def exec(cls, message: Message, bot: Bot):
        super().exec(message, bot)

        prices = [
            LabeledPrice("Бумажные материалы", 200_00),
            LabeledPrice("Сопровождние в обучении", 500_00),
            LabeledPrice("Видеоматериалы", 1000_00),
            LabeledPrice("1 вебинар в неделю", 2000_00),
        ]

        cls.bot.send_invoice(
            chat_id=cls.message.chat.id,
            title="Оплата Курсов. Ступень 1",
            description="В данном кейсе мы проводим тестовое выставление счета "
            "на оплату пользователю",
            invoice_payload="COURSES STAGE 1",
            currency="rub",
            prices=prices,
            reply_to_message_id=cls.message.message_id,
            provider_token=c.payment_token,
        )
