from telebot.types import CallbackQuery

from app import constants as c
from app.bot import Bot
from app.callbacks import BaseCallback


class CallbackCalculationRequest(BaseCallback):
    @classmethod
    def exec(cls, call: CallbackQuery, bot: Bot):
        if call.data == c.CALLBACK_CALC_REQUEST:
            return bot.custom_edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Отлично! Наш менеджер скоро с вами свяжется!",
                reply_markup=None,
            )
            # SEND TO CRM
        if call.data == c.CALLBACK_CALC_REQUEST_CANCEL:
            return bot.custom_edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text="Заявка отменена! Возвращайтесь как можно скорей!",
                reply_markup=None,
            )

    @classmethod
    def trigger(cls, call: CallbackQuery) -> bool:
        return call.data in [c.CALLBACK_CALC_REQUEST_CANCEL, c.CALLBACK_CALC_REQUEST]
