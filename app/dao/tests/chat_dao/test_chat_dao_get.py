from app.dao import ChatDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.model_fixture_generator import ModelFixture
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestChatDaoGet(TestDataBaseClass):
    def setUp(self):
        super().setUp()

        self.mf = ModelFixture()
        self.chat_data = TelegramFixture().generate_random_private_chat()
        self.not_saved_chat_data = TelegramFixture().generate_random_private_chat()
        self.chat = self.mf.create_model_chat(self.chat_data)
        self.dao = ChatDao()

    def test_get_existed_chat(self):
        chat = self.dao.get(self.chat_data)

        self.assertTrue(chat)

    def test_get_not_existed_chat(self):
        chat = self.dao.get(self.not_saved_chat_data)

        self.assertIsNone(chat)
