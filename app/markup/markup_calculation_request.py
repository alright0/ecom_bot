from telebot import types

from app.constants import CALLBACK_CALC_REQUEST, CALLBACK_CALC_REQUEST_CANCEL
from app.markup import BaseInlineKeyboardMarkup


def markup_calculation_request() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(
            "🟢 Отправить на просчет",
            callback_data=CALLBACK_CALC_REQUEST,
        ),
        types.InlineKeyboardButton(
            "🔴️ Отмена",
            callback_data=CALLBACK_CALC_REQUEST_CANCEL,
        ),
    ]

    return BaseInlineKeyboardMarkup(buttons, row_width=1).markup
