from unittest.mock import MagicMock

from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.model_fixture_generator import ModelFixture
from app.fixtures.telegram_fixture_generator import TelegramFixture
from app.middlewares import MiddlewareUserMessage


class TestMiddlewareUserAddedToChat(TestDataBaseClass):
    def setUp(self):
        super().setUp()

        self.bot = MagicMock()
        self.mf = ModelFixture()
        self.tf = TelegramFixture()
        self.user = self.tf.generate_random_user()
        self.message, *_ = self.tf.generate_random_message_pack(
            new_chat_members=[self.user.to_json()],
        )
        self.middleware = MiddlewareUserMessage

    def test_middleware_add_to_chat_exec_user(self):
        self.middleware.exec(self.bot, self.message)

        users_count = len(self.mf.user_dao.all())
        chats_count = len(self.mf.chat_dao.all())
        messages_count = len(self.mf.message_dao.all())

        self.assertEqual(users_count, 1)
        self.assertEqual(chats_count, 1)
        self.assertEqual(messages_count, 1)
