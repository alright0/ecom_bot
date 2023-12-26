from app.dao import MessageDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.model_fixture_generator import ModelFixture
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestMessageDaoGet(TestDataBaseClass):
    def setUp(self):
        super().setUp()

        self.mf = ModelFixture()
        self.tf = TelegramFixture()
        (
            self.message_data,
            self.user_data,
            self.chat_data,
        ) = self.tf.generate_random_message_pack()
        self.chat = self.mf.create_model_chat(self.chat_data)
        self.user = self.mf.create_model_user(self.user_data)
        self.dao = MessageDao()

    def test_get_existing_message(self):
        self.dao.create(self.message_data, self.chat, self.user)
        message = self.dao.get(self.message_data)

        self.assertIsNotNone(message)
        self.assertEqual(message.msg_id, self.message_data.id)

    def test_get_not_existing_message(self):
        message = self.dao.get(self.message_data)

        self.assertIsNone(message)
