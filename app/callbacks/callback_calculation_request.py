from telebot.types import CallbackQuery

from app import constants as c
from app.bot import Bot
from app.callbacks import BaseCallback


class CallbackCalculationRequest(BaseCallback):
    SEND_REQUEST_TEXT = (
        "Отлично! Заявка отправлена, наш менеджер скоро с вами свяжется!"
    )
    CANCEL_REQUEST_TEXT = (
        "Заявка отменена! Возвращайтесь как можно скорей!\n"
        "Перезаполнить заявку можно через команду /calculation"
    )

    @classmethod
    def exec(cls, call: CallbackQuery, bot: Bot):
        if call.data == c.CALLBACK_CALC_REQUEST:
            return bot.custom_edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=cls.SEND_REQUEST_TEXT,
                reply_markup=None,
            )
        if call.data == c.CALLBACK_CALC_REQUEST_CANCEL:
            return bot.custom_edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=cls.CANCEL_REQUEST_TEXT,
                reply_markup=None,
            )

    @classmethod
    def trigger(cls, call: CallbackQuery) -> bool:
        return call.data in [c.CALLBACK_CALC_REQUEST_CANCEL, c.CALLBACK_CALC_REQUEST]
