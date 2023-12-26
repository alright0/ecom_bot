from typing import Union

from telebot import types


class BaseInlineKeyboardMarkup:
    def __init__(
        self,
        buttons: Union[list, types.InlineKeyboardButton],
        row_width: int = 3,
    ):
        self.buttons = buttons
        self.row_width = row_width

    @property
    def markup(self):
        markup = types.InlineKeyboardMarkup(row_width=self.row_width)
        if isinstance(self.buttons, list):
            markup.add(*self.buttons)
        else:
            markup.add(self.buttons)

        return markup
