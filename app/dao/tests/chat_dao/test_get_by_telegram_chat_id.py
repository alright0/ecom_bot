from app.dao import ChatDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestChatDaoGetByTelegramChatId(TestDataBaseClass):
    def setUp(self):
        super().setUp()

        self.chat_data = TelegramFixture().generate_random_private_chat()
        self.dao = ChatDao()

    def test_get_by_telegram_chat_id(self):
        self.dao.create(self.chat_data)
        chat = self.dao.get_by_telegram_chat_id(self.chat_data.id)

        self.assertEqual(chat.chat_id, self.chat_data.id)
