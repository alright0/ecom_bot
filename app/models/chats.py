from typing import TYPE_CHECKING, List

from sqlalchemy import BIGINT, Column, String
from sqlalchemy.orm import Mapped, relationship
from telebot.types import Chat as TelegramChat

from app.models.base_models import (
    BaseIdModel,
    BaseIsDeletedModel,
    BaseRawFieldModel,
    BaseTimeModel,
)

if TYPE_CHECKING:
    from app.models import Message


class Chat(BaseIdModel, BaseRawFieldModel, BaseTimeModel, BaseIsDeletedModel):
    __tablename__ = "chats"

    chat_id = Column(BIGINT, unique=True, nullable=False)
    type = Column(String, nullable=True)
    title = Column(String, nullable=True)

    messages: Mapped[List["Message"]] = relationship("Message", back_populates="chat")

    def __repr__(self) -> str:
        return f"{self.chat_id}: {self.as_object.type}"

    @property
    def as_object(self):
        return TelegramChat.de_json(self.json)
