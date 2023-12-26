from app.dao import MessageDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.model_fixture_generator import ModelFixture
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestMessageDaoCreateOrUpdate(TestDataBaseClass):
    def setUp(self):
        super().setUp()

        self.tf = TelegramFixture()
        self.mf = ModelFixture()
        (
            self.message_data,
            self.user_data,
            self.chat_data,
        ) = self.tf.generate_random_message_pack()

        self.chat = self.mf.create_model_chat(self.chat_data)
        self.user = self.mf.create_model_user(self.user_data)
        self.dao = MessageDao()

    def test_create_message(self):
        message, created = self.dao.create_or_update(
            self.message_data,
            self.chat,
            self.user,
        )

        self.assertTrue(created)

    def test_update_message(self):
        self.dao.create_or_update(self.message_data, self.chat, self.user)
        updated_message, created = self.dao.create_or_update(
            self.message_data,
            self.chat,
            self.user,
        )

        self.assertFalse(created)
