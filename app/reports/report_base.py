from abc import ABC, abstractmethod
from typing import List

import pandas as pd
from _plotly_utils.colors.qualitative import Light24

from app.libs.period import Period
from app.models import Chat, User


class BaseReport(ABC):
    df = pd.DataFrame([])
    fig = None
    description: str = ""
    caption: str = ""
    text: str = ""
    empty_text: str = ""
    private_chat_text: str = ""
    is_empty: bool = False

    period: Period
    available_periods: list = Period.ALL_PERIODS

    @abstractmethod
    def __init__(self, chat: Chat, period: Period):
        self.chat = chat
        self.period = period
        self.start_date, self.end_date = self.period.start_date, self.period.end_date

    @abstractmethod
    def exec(self):
        raise NotImplementedError()

    @abstractmethod
    def render(self):
        raise NotImplementedError()

    @abstractmethod
    def prepare_data(self):
        raise NotImplementedError()

    def png(self) -> bytes:
        return self._to_buffer("png")

    def _to_buffer(self, file_format: str) -> bytes:
        if not self.fig:
            return b""
        fig_data = self.fig.to_image(format=file_format)
        return fig_data

    def define_colorscheme(self, column: str, colorscheme: List[str] = Light24):
        """Считает количество значений в указанной колонке и отдает цветовую схему соответствующей длины."""

        scheme_len = len(set(self.df[column].tolist()))
        return colorscheme[:scheme_len]

    @staticmethod
    def set_full_name(user: User) -> str:
        if user.first_name and user.last_name:
            return f"{user.first_name or ''} {user.last_name or ''}"
        else:
            return user.username or str(user.id)

    def _format_caption(self, caption: str) -> str:
        return caption.format(self.period.title)
