from app.dao import ChatDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestChatDaoGet(TestDataBaseClass):
    def setUp(self):
        super().setUp()
        self.chat_data = TelegramFixture().generate_random_private_chat()
        self.dao = ChatDao()

    def test_delete_existed_chat(self):
        self.dao.create(self.chat_data)
        deleted_chat = self.dao.delete(self.chat_data)

        self.assertTrue(deleted_chat.deleted)

    def test_delete_not_existed_chat(self):
        chat = self.dao.delete(self.chat_data)

        self.assertTrue(chat.deleted)
        self.assertEqual(chat.chat_id, self.chat_data.id)
