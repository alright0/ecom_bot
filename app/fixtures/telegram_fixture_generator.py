import datetime
import random
from typing import Any, List, Tuple

import faker
from telebot.types import CallbackQuery, Chat, Message, User


class TelegramFixture:
    def __init__(self):
        self.fake: faker.Faker = faker.Faker()

    def _base_chat(self, **kwargs) -> Chat:
        self._add_key_if_not_exists(kwargs, "id", self.random_private_chat_id())
        self._add_key_if_not_exists(kwargs, "first_name", self.fake.first_name())
        self._add_key_if_not_exists(kwargs, "last_name", self.fake.last_name())
        self._add_key_if_not_exists(kwargs, "username", self.fake.user_name())
        self._add_key_if_not_exists(kwargs, "title", self.fake.word())

        return Chat(**kwargs)

    def _base_message(
        self, json_data: dict, from_json: bool = True, **kwargs
    ) -> Message:
        if from_json:
            return Message.de_json(json_data)
        return Message(**kwargs)

    def _base_user(self, **kwargs) -> User:
        self._add_key_if_not_exists(kwargs, "id", self.random_user_id())
        self._add_key_if_not_exists(kwargs, "first_name", self.fake.first_name())
        self._add_key_if_not_exists(kwargs, "last_name", self.fake.last_name())
        self._add_key_if_not_exists(kwargs, "username", self.fake.user_name())

        return User(**kwargs)

    def _base_callback(
        self, chat: Chat, message: Message, user: User, callback_data: str, **kwargs
    ) -> CallbackQuery:
        frozen_keys = [
            "id",
            "from_user",
            "message",
            "json_string",
            "chat_instance",
            "data",
            "chat",
        ]
        self._raise_for_frozen_keys(frozen_keys, kwargs)

        return CallbackQuery(
            id=self.fake.word(),  # ???
            from_user=user,
            message=message,
            json_string=message.json,
            chat_instance=chat,
            data=callback_data,
            chat=chat,
            **kwargs,
        )

    def generate_user(self, **kwargs) -> User:
        """Создает  пользователя с указанными параметрами или с минимальным набором данных:
        id, first_name, last_name, username.
        """
        return self._base_user(**kwargs)

    def generate_user_from_private_chat(self, chat: Chat) -> User:
        """Генерирует пользователя из приватного чата."""

        if chat.type != "private":
            raise AttributeError("Chat type must be private for extract user")

        data = chat.__dict__
        return self._base_user(
            id=data.get("id"),
            first_name=data.get("first_name"),
            last_name=data.get("last_name"),
            username=data.get("username"),
            is_bot=False,
        )

    def generate_random_user(self) -> User:
        """Создает пользователя со случайным минимальным набором параметров."""

        return self._base_user(
            is_bot=False,
            language_code="ru",
        )

    def generate_random_bot(self) -> User:
        """Создает случайного бота."""

        return self._base_user(
            is_bot=True,
            is_premium=None,
            last_name=None,
            language_code=None,
            added_to_attachment_menu=None,
            supports_inline_queries=None,
            can_read_all_group_messages=None,
            can_join_groups=None,
        )

    def generate_random_message_from_user_and_chat(
        self,
        user: User,
        chat: Chat,
        **kwargs,
    ) -> Message:
        """Создает случайное сообщение от пользователя в чате."""

        self._add_key_if_not_exists(kwargs, "message_id", self.random_message_id())
        self._add_key_if_not_exists(
            kwargs,
            "date",
            int(datetime.datetime.now().timestamp()),
        )
        self._add_key_if_not_exists(kwargs, "text", self.fake.text())

        json_string = {
            "from": user.__dict__,
            "chat": chat.__dict__,
            **kwargs,
        }
        return self._base_message(json_data=json_string)

    def generate_random_messages_chain(
        self,
        chat: Chat,
        users: List[User],
        quantity: int = 10,
    ) -> List[Message]:
        """Создает указанное количество сообщений от случайно выбранных
        пользователей в указанном чате.
        """

        if quantity <= 0:
            raise AttributeError("quantity must be positive integer")

        messages = []
        for message_id in range(1, quantity + 1):
            user = random.choice(users)
            message = self.generate_random_message_from_user_and_chat(
                user,
                chat,
                message_id=message_id,
            )
            messages.append(message)
        return messages

    def generate_random_private_chat(self, **kwargs) -> Chat:
        """Создает случайный приватный чат. Подходит для извлечения пользователя из чата."""

        frozen_keys = ["id", "title", "type"]
        self._raise_for_frozen_keys(frozen_keys, kwargs)

        return self._base_chat(
            id=self.random_private_chat_id(), title=None, type="private", **kwargs
        )

    def generate_random_group_chat(self, **kwargs) -> Chat:
        """Создает случайный групповой чат. НЕ Подходит для извлечения пользователя."""

        frozen_keys = ["id", "title", "type", "first_name", "last_name", "username"]
        self._raise_for_frozen_keys(frozen_keys, kwargs)

        return self._base_chat(
            id=self.random_group_chat_id(),
            title=None,
            type="group",
            first_name=None,
            last_name=None,
            username=None,
            **kwargs,
        )

    def generate_random_supergroup_chat(self, **kwargs):
        """Создает случайную супергруппу. НЕ Подходит для извлечения пользователя."""

        frozen_keys = ["id", "title", "type", "first_name", "last_name", "username"]
        self._raise_for_frozen_keys(frozen_keys, kwargs)

        return self._base_chat(
            id=self.random_supergroup_chat_id(),
            title=f"super_group_chat_{self.fake.word()}",
            type="supergroup",
            first_name=None,
            last_name=None,
            username=None,
            **kwargs,
        )

    def generate_random_message_pack(self, **kwargs) -> Tuple[Message, User, Chat]:
        """Создает случайный набор приватного чата, пользователя из приватного чата
        и сообщения в нем.
        """

        chat = self.generate_random_private_chat()
        user = self.generate_user_from_private_chat(chat)
        message = self.generate_random_message_from_user_and_chat(user, chat, **kwargs)

        return message, user, chat

    def genetate_random_group_conversation(
        self,
        users_quantity: int,
        messages_quantity: int,
    ) -> Tuple[Chat, List[User], List[Message]]:
        """Создает набор случайных сообщений и пользователей в групповом чате."""

        if users_quantity <= 0:
            raise ValueError("Users must be positive integer")

        if messages_quantity <= 0:
            raise ValueError("messages must be positive integer")

        users_list = []
        chat = self.generate_random_group_chat()
        for user in range(users_quantity):
            users_list.append(self.generate_random_user())
        messages = self.generate_random_messages_chain(
            chat,
            users_list,
            messages_quantity,
        )

        return chat, users_list, messages

    def generate_random_callback(self, callback_data: str, **kwargs) -> CallbackQuery:
        """Создает callback_query из случайных чата, пользователя и сообщения"""
        message, user, chat = self.generate_random_message_pack()
        return self.generate_callback_from_data(
            chat, message, user, callback_data, **kwargs
        )

    def generate_callback_from_data(
        self, chat: Chat, message: Message, user: User, callback_data: str, **kwargs
    ) -> CallbackQuery:
        """Создает коллбэк из переданных чата, сообщенея, пользователя и даты."""

        return self._base_callback(chat, message, user, callback_data, **kwargs)

    @staticmethod
    def _add_key_if_not_exists(data: dict, key: Any, value: Any) -> dict:
        if key not in data.keys():
            data.update({key: value})
        return data

    @staticmethod
    def _raise_for_frozen_keys(keys, data):
        for key in keys:
            if key in data.keys():
                raise AttributeError(f'key: "{key} cannot be set. "')

    def random_user_id(self) -> int:
        return self.random_private_chat_id()

    @staticmethod
    def random_private_chat_id() -> int:
        return random.randint(100000000, 999999999)

    @staticmethod
    def random_group_chat_id() -> int:
        return random.randint(-999999999, -100000000)

    @staticmethod
    def random_supergroup_chat_id() -> int:
        return random.randint(-9999999999999, -1000000000000)

    @staticmethod
    def random_message_id() -> int:
        return random.randint(1, 100000)
