from app.dao import MessageDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.model_fixture_generator import ModelFixture
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestMessageDaoCreate(TestDataBaseClass):
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

    def test_create_message(self):
        message = self.dao.create(self.message_data, self.chat, self.user)
        message_from_model = message.as_message

        self.assertEqual(message_from_model.date, self.message_data.date)
        self.assertEqual(message_from_model.id, self.message_data.id)
        self.assertEqual(message_from_model.message_id, self.message_data.message_id)
