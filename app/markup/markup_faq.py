from telebot import types

from app.markup import BaseInlineKeyboardMarkup


def markup_faq() -> types.InlineKeyboardMarkup:
    buttons = [
        types.InlineKeyboardButton(
            "Укладка кафеля",
            url="https://mosplitka.ru/staty/ukladka/"
            "ukladka-plitki-na-stenu-svoimi-rukami-podrobnaya-poshagovaya-instruktsiya/",
        ),
        types.InlineKeyboardButton(
            "Отделка потолка",
            url="https://www.youtube.com/watch?v=RHlOsKLjaa0",
        ),
        types.InlineKeyboardButton(
            "Покраска стен за 6 минут",
            url="https://www.youtube.com/watch?v=Lmv5BMXfFfg",
        ),
    ]

    return BaseInlineKeyboardMarkup(buttons, row_width=1).markup
