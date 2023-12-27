from telebot.types import CallbackQuery, LabeledPrice

from app.bot import Bot
from app.callbacks import BaseCallback
from app.config import config
from app.constants import (
    CALLBACK_INVOICE_COURSE_1,
    CALLBACK_INVOICE_COURSE_2,
    INVOICE_PAYLOAD_COURSE_1,
)


class CallbackSendCourceInvoice(BaseCallback):
    @classmethod
    def exec(cls, call: CallbackQuery, bot: Bot):
        super().exec(call, bot)
        prices = [
            LabeledPrice("Бумажные материалы", 100_00),
            LabeledPrice("Сопровождние в обучении", 100_00),
            LabeledPrice("Видеоматериалы", 100_00),
            LabeledPrice("1 вебинар в неделю", 100_00),
        ]

        invoice_description = (
            "Вы можете передавать информацию о курсах и их содержании из бота или другого источника."
            "Для оплаты курса используйте данные карты:\n\nНомер карты: 1111111111111026\n"
            "valid thru: 12/22\ncvv: 000\n"
        )
        photo_url = "https://www.akbiz.ru/uploads/images/blog/abius/1623701630_publication%201040x645_web%20(1).png"

        cls.bot.send_invoice(
            chat_id=cls.call.message.chat.id,
            title="Обучающие материалы по курсу 1",
            description=invoice_description,
            invoice_payload=INVOICE_PAYLOAD_COURSE_1,
            currency="rub",
            prices=prices,
            photo_url=photo_url,
            photo_width=1000,
            photo_height=750,
            reply_to_message_id=cls.call.message.message_id,
            provider_token=config.payment_token,
        )

    @classmethod
    def trigger(cls, call: CallbackQuery) -> bool:
        return call.data in [CALLBACK_INVOICE_COURSE_1, CALLBACK_INVOICE_COURSE_2]
