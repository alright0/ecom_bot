from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.model_fixture_generator import ModelFixture
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestTelegramFixture(TestDataBaseClass):
    def setUp(self):
        super().setUp()

        self.mf = ModelFixture()
        self.tf = TelegramFixture()

    def tearDown(self):
        super().tearDown()

    def test_create_model_chat(self):
        chat_data = self.tf.generate_random_private_chat()
        chat = self.mf.create_model_chat(chat_data)

        self.assertEqual(chat.chat_id, chat_data.id)
        self.assertEqual(chat.json.get("first_name"), chat_data.first_name)
        self.assertEqual(self.mf.chat_dao.get(chat_data).id, 1)

    def test_create_model_message_from_tf(self):
        message_data, *_ = self.tf.generate_random_message_pack()

        message = self.mf.create_model_message(message_data)

        self.assertEqual(message.chat.chat_id, message_data.chat.id)
        self.assertEqual(message.user.user_id, message_data.from_user.id)
        self.assertEqual(message.text, message_data.text)
        self.assertEqual(self.mf.message_dao.get(message_data).id, 1)

    def test_create_model_message(self):
        message = self.mf.create_model_message()
        self.assertTrue(self.mf.message_dao.get(message.as_message))

    def test_create_model_user_from_tf(self):
        user_data = self.tf.generate_random_user()
        user = self.mf.create_model_user(user_data)

        self.assertEqual(user.user_id, user_data.id)
        self.assertEqual(user.first_name, user_data.first_name)
        self.assertEqual(self.mf.user_dao.get(user_data).id, 1)

    def test_create_model_user(self):
        user = self.mf.create_model_user()

        self.assertTrue(self.mf.user_dao.get(user.as_object))
