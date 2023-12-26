from datetime import datetime
from typing import TYPE_CHECKING

from sqlalchemy import BIGINT, Column, ForeignKey, Text
from sqlalchemy.orm import Mapped, relationship
from telebot.types import Message as TelegramMessage

from app.models.base_models import BaseIdModel, BaseRawFieldModel, BaseTimeModel

if TYPE_CHECKING:
    from app.models import Chat, User


class Message(BaseIdModel, BaseRawFieldModel, BaseTimeModel):
    __tablename__ = "messages"

    chat_id: Mapped["Chat"] = Column(ForeignKey("chats.id"))
    user_id: Mapped["User"] = Column(ForeignKey("users.id"))
    msg_id = Column(BIGINT, nullable=True)
    text = Column(Text, nullable=True)

    chat: Mapped["Chat"] = relationship("Chat", back_populates="messages")
    user: Mapped["User"] = relationship("User", back_populates="messages")

    def __repr__(self) -> str:
        created = self.created or datetime.fromtimestamp(self.as_message.date)
        return (
            f"message {self.as_message.id}({self.id}) "
            f"in chat: {self.chat.chat_id}({self.chat_id}). "
            f"{created}. '{self.text}' "
        )

    @property
    def as_message(self) -> TelegramMessage:
        return TelegramMessage.de_json(self.json)
