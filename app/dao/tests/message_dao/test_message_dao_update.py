from app.dao import MessageDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.model_fixture_generator import ModelFixture
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestMessageDaoUpdate(TestDataBaseClass):
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

    def test_update_message(self):
        message = self.dao.create(self.message_data, self.chat, self.user)

        old_update_date = message.updated
        UPDATED_TEXT = "updated"
        self.message_data.text = UPDATED_TEXT

        updated_message = self.dao.update(self.message_data, message)

        self.assertNotEqual(old_update_date, updated_message.updated)
        self.assertEqual(updated_message.text, UPDATED_TEXT)
