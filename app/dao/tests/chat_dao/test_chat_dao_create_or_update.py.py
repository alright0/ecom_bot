from app.dao import ChatDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestChatDaoCreateOrUpdate(TestDataBaseClass):
    def setUp(self):
        super().setUp()
        self.chat_data = TelegramFixture().generate_random_private_chat()
        self.NEW_TITLE = "new_chat_title"
        self.dao = ChatDao()

    def test_update_chat(self):
        chat = self.dao.create(self.chat_data)
        old_updated = chat.updated

        updated_chat, created = self.dao.create_or_update(self.chat_data, chat)
        new_updated = updated_chat.updated

        self.assertNotEqual(old_updated, new_updated)
        self.assertFalse(created)

    def test_create_chat(self):
        updated_chat, created = self.dao.create_or_update(self.chat_data, chat)

        self.assertFalse(created)
        self.assertTrue(updated_chat.chat_id, self.chat_data.id)
