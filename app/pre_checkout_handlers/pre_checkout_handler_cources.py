from telebot.types import PreCheckoutQuery

from app.bot import Bot
from app.constants import INVOICE_PAYLOAD_COURSE_1, INVOICE_PAYLOAD_COURSE_2


class PreCheckoutHandlerGivePaymentCourse:
    UPDATE_TYPES = ["pre_checkout_query"]
    PASS_BOT = True

    @classmethod
    def exec(cls, pre_checkout_query: PreCheckoutQuery, bot: Bot) -> bool:
        return bot.answer_pre_checkout_query(
            pre_checkout_query_id=int(pre_checkout_query.id),
            error_message="Тестовое сообщение об отмене оплаты",
            ok=True,
        )

    @classmethod
    def trigger(cls, pre_checkout_query: PreCheckoutQuery) -> bool:
        print("pre_checkout_query: ", pre_checkout_query)
        return pre_checkout_query.invoice_payload in [
            INVOICE_PAYLOAD_COURSE_1,
            INVOICE_PAYLOAD_COURSE_2,
        ]
