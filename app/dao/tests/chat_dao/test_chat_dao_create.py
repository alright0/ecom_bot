from app.dao import ChatDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestChatDaoCreate(TestDataBaseClass):
    def setUp(self):
        super().setUp()

        self.chat_data = TelegramFixture().generate_random_private_chat()
        self.dao = ChatDao()

    def test_create_chat(self):
        chat = self.dao.create(self.chat_data)

        self.assertFalse(chat.deleted)
        self.assertEqual(chat.chat_id, self.chat_data.id)
