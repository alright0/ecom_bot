from telebot import types

from app.markup import BaseInlineKeyboardMarkup


def markup_faq() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(
            "Этапы ремонта ванной комнаты",
            url="https://vk.com/hdgroupkrasnodar?w=wall-211271126_225",
        ),
        types.InlineKeyboardButton(
            "Дизайн-проект: Нужен или нет?",
            url="https://vk.com/hdgroupkrasnodar?w=wall-211271126_219",
        ),
        types.InlineKeyboardButton(
            "Рубрика Вопрос-Ответ",
            url="https://vk.com/hdgroupkrasnodar?w=wall-211271126_209",
        ),
    ]

    return BaseInlineKeyboardMarkup(buttons, row_width=1).markup
