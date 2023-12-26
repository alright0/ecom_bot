from datetime import datetime
from typing import List, Optional, Tuple, Type

from telebot.types import Message as TelegramMessage

from app.dao import BaseDao, ChatDao
from app.models import Chat, Message, User


class MessageDao(BaseDao):
    def create_or_update(
        self,
        msg: TelegramMessage,
        chat: Chat,
        user: User,
    ) -> Tuple[Message, bool]:
        message = self.get(msg)
        if message:
            message = self.update(msg, message)
            created = False
        else:
            message = self.create(msg, chat, user)
            created = True
        return message, created

    def get_or_create(
        self,
        msg: TelegramMessage,
        chat: Chat,
        user: User,
    ) -> Tuple[Message, bool]:
        message = self.get(msg)
        if not message:
            message = self.create(msg, chat, user)
            created = True
        else:
            created = False
        return message, created

    def create(self, msg: TelegramMessage, chat: Chat, user: User) -> Message:
        message = Message()
        message.chat_id = chat.id
        message.msg_id = msg.message_id
        message.user_id = user.id
        message.text = msg.text or msg.caption
        message.raw = self.raw(msg.json)

        self.session.add(message)
        self.save()

        return message

    def update(self, msg: TelegramMessage, message: Message) -> Message:
        message.text = msg.text or msg.caption
        message.raw = self.raw(msg.json)
        message.updated = datetime.utcnow()

        self.session.add(message)
        self.save()

        return message

    def get_by_id(self, message_id: int) -> Optional[Message]:
        return self.session.query(Message).filter(Message.id == message_id).first()

    def get(self, message: TelegramMessage) -> Optional[Message]:
        return (
            self.session.query(Message)
            .join(Chat)
            .join(User)
            .filter(Chat.chat_id == message.chat.id)
            .filter(Message.msg_id == message.id)
            .filter(User.user_id == message.from_user.id)
            .first()
        )

    def get_all_by_date(
        self,
        chat: Chat,
        start_date: datetime,
        end_date: datetime,
    ) -> List[Optional[Type[Message]]]:
        chat_ids = [chat.id]
        parent_chat = ChatDao().get_parent_chat(chat.as_object)
        if parent_chat:
            chat_ids.append(parent_chat.id)

        return (
            self.session.query(Message)
            .filter(Message.created >= start_date)
            .filter(Message.created <= end_date)
            .filter(Message.chat_id.in_(chat_ids))
            .all()
        )

    def all(self):
        return self.session.query(Message).all()
