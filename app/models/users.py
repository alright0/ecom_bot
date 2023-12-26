from typing import TYPE_CHECKING, List

from sqlalchemy import BIGINT, Column, String
from sqlalchemy.orm import Mapped, relationship
from telebot.types import User as TelegramUser

from app.models.base_models import BaseIdModel, BaseRawFieldModel, BaseTimeModel

if TYPE_CHECKING:
    from app.models import Message


class User(BaseIdModel, BaseRawFieldModel, BaseTimeModel):
    __tablename__ = "users"

    user_id = Column(BIGINT, nullable=True)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    messages: Mapped[List["Message"]] = relationship("Message", back_populates="user")

    def __repr__(self) -> str:
        username = f"({self.username})" or ""
        created = self.created.strftime("%d.%m.%Y %H:%M") if self.created else ""
        last_activity = self.updated.strftime("%d.%m.%Y %H:%M") if self.updated else ""

        return (
            f"User: {self.full_name} {username}. Created: {created}. "
            f"Last activity {last_activity}"
        )

    @property
    def full_name(self):
        first_name = self.first_name or ""
        last_name = self.last_name or ""
        return f"{first_name} {last_name}"

    @property
    def as_object(self) -> TelegramUser:
        return TelegramUser.de_json(self.raw)
