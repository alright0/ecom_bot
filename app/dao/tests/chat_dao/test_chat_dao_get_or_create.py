from app.dao import ChatDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestChatDaoGetOrCreate(TestDataBaseClass):
    def setUp(self):
        super().setUp()

        self.chat_data = TelegramFixture().generate_random_private_chat()
        self.dao = ChatDao()

    def test_get_chat(self):
        self.dao.create(self.chat_data)
        chat, created = self.dao.get_or_create(self.chat_data)

        self.assertEqual(chat.chat_id, self.chat_data.id)
        self.assertFalse(created)

    def test_create_chat(self):
        chat, created = self.dao.get_or_create(self.chat_data)

        self.assertTrue(created)
