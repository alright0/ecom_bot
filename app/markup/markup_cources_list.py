from telebot import types

from app.constants import (
    CALLBACK_INVOICE_COURSE_1,
    CALLBACK_INVOICE_COURSE_2,
    CALLBACK_SHOW_TEST_COURSE,
)
from app.markup import BaseInlineKeyboardMarkup


def markup_show_courses_list() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(
            "✅ Куплено. Обучающий Курс 1. Посмотреть",
            callback_data=CALLBACK_SHOW_TEST_COURSE,
        ),
        types.InlineKeyboardButton(
            "💰 Обучающий Курс 2. Купить",
            callback_data=CALLBACK_INVOICE_COURSE_1,
        ),
        types.InlineKeyboardButton(
            "💰 Обучающий Курс 3. Купить",
            callback_data=CALLBACK_INVOICE_COURSE_2,
        ),
    ]

    return BaseInlineKeyboardMarkup(buttons, row_width=1).markup
