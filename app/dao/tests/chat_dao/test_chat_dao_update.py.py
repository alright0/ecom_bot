from app.dao import ChatDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestChatDaoUpdate(TestDataBaseClass):
    def setUp(self):
        super().setUp()

        self.chat_data = TelegramFixture().generate_random_private_chat()
        self.NEW_TITLE = "new_chat_title"
        self.dao = ChatDao()

    def test_update_chat(self):
        chat = self.dao.create(self.chat_data)
        old_title = self.chat_data.title
        old_updated = chat.updated

        self.chat_data.title = self.NEW_TITLE
        updated_chat = self.dao.update(self.chat_data, chat)
        new_updated = updated_chat.updated

        self.assertNotEqual(old_title, updated_chat)
        self.assertNotEqual(old_updated, new_updated)
