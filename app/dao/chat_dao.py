from datetime import datetime
from typing import List, Optional, Tuple, Type

from telebot.types import Chat as TelegramChat

from app.dao import BaseDao
from app.models import Chat


class ChatDao(BaseDao):
    def create_or_update(self, chat_data: TelegramChat) -> Tuple[Chat, bool]:
        chat = self.get(chat_data)
        if chat:
            chat = self.update(chat_data, chat)
            created = False
        else:
            chat = self.create(chat_data)
            created = True

        return chat, created

    def create(self, chat_data: TelegramChat) -> Chat:
        chat = Chat()
        chat.chat_id = chat_data.id
        chat.type = chat_data.type
        chat.title = chat_data.title
        chat.raw = self.raw(chat_data.__dict__)

        self.session.add(chat)
        self.save()

        return chat

    def update(self, chat_data: TelegramChat, chat: Chat) -> Chat:
        chat.chat_id = chat_data.id
        chat.type = chat_data.type
        chat.title = chat_data.title
        chat.raw = self.raw(chat_data.__dict__)
        chat.updated = datetime.utcnow()

        self.session.add(chat)
        self.save()

        return chat

    def get(self, chat_data: TelegramChat) -> Optional[Chat]:
        return self.session.query(Chat).filter(Chat.chat_id == chat_data.id).first()

    def get_by_id(self, chat_id: int) -> Optional[Chat]:
        return self.session.query(Chat).filter(Chat.id == chat_id).first()

    def get_by_telegram_chat_id(self, chat_id: int) -> Optional[Chat]:
        return self.session.query(Chat).filter(Chat.chat_id == chat_id).first()

    def all(self) -> List[Optional[Type[Chat]]]:
        return self.session.query(Chat).all()

    def get_or_create(self, chat_data: TelegramChat) -> Tuple[Chat, bool]:
        chat = self.get(chat_data)
        if not chat:
            chat = self.create(chat_data)
            created = True
        else:
            created = False
        return chat, created

    def delete(self, chat_data: TelegramChat) -> Chat:
        chat, _ = self.get_or_create(chat_data)
        chat.deleted = True
        chat.updated = datetime.utcnow()

        self.session.add(chat)
        self.save()

        return chat

    def get_parent_chat(self, chat_data: TelegramChat) -> Optional[Chat]:
        group_anon_bot = "GroupAnonymousBot"

        this_chat = self.get(chat_data)
        messages = sorted(this_chat.messages, key=lambda x: x.id)
        first_message = messages[0] if len(messages) else None
        if not (first_message and first_message.user.username == group_anon_bot):
            return None

        message = first_message.as_message
        parent_chat_id = message.migrate_from_chat_id
        if not parent_chat_id:
            return None

        return self.get_by_telegram_chat_id(parent_chat_id)
