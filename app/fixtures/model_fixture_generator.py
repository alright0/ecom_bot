import inspect
from typing import Optional

import faker
from telebot.types import Chat as TelegramChat
from telebot.types import Message as TelegramMessage
from telebot.types import User as TelegramUser

from app.dao import ChatDao, MessageDao, UserDao
from app.fixtures.telegram_fixture_generator import TelegramFixture
from app.models import Chat, Message, User


class ModelFixture:
    def __init__(self):
        try:
            target_class_name = "TestDataBaseClass"
            caller_class = inspect.stack()[1][0].f_locals["self"].__class__
            parent_class = caller_class.__bases__[0]
            if parent_class.__name__ != target_class_name:
                print(
                    f"Warning: ModelFixture called in class: {caller_class.__name__} with "
                    f"parent of {parent_class.__name__} instead {target_class_name}",
                )
        except Exception as e:
            print(f"Warning: Error checking caller class in ModelFixture. {e}")

        self.user_dao = UserDao()
        self.chat_dao = ChatDao()
        self.message_dao = MessageDao()
        self.fake: faker.Faker = faker.Faker()
        self.tf = TelegramFixture()

    def create_model_chat(self, chat_data: Optional[TelegramChat] = None) -> Chat:
        if not chat_data:
            chat_data = self.tf.generate_random_private_chat()
        return ChatDao().create(chat_data)

    def create_model_message(
        self,
        message_data: Optional[TelegramMessage] = None,
    ) -> Message:
        if not message_data:
            message_data, *_ = self.tf.generate_random_message_pack()
        user = self.user_dao.create(message_data.from_user)
        chat = self.chat_dao.create(message_data.chat)
        return self.message_dao.create(message_data, chat, user)

    def create_model_user(
        self,
        user_data: Optional[TelegramUser] = None,
    ) -> User:
        if not user_data:
            user_data = self.tf.generate_random_user()
        return UserDao().create(user_data)
