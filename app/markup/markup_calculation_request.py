from telebot import types

from app.constants import CALLBACK_CALC_REQUEST, CALLBACK_CALC_REQUEST_CANCEL
from app.markup import BaseInlineKeyboardMarkup


def markup_calculation_request() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(
            "Отмена",
            callback_data=CALLBACK_CALC_REQUEST_CANCEL,
        ),
        types.InlineKeyboardButton(
            "Отправить заявку на просчет",
            callback_data=CALLBACK_CALC_REQUEST,
        ),
    ]

    return BaseInlineKeyboardMarkup(buttons).markup
