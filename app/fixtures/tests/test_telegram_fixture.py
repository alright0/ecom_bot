import datetime
import unittest

from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestTelegramFixture(unittest.TestCase):
    def setUp(self):
        self.tf = TelegramFixture()

    def test_generate_random_user(self):
        user = self.tf.generate_random_user()

        self.assertTrue(user.username)
        self.assertEqual(user.language_code, "ru")
        self.assertFalse(user.is_bot)
        self.assertFalse(user.is_premium)

    def test_generate_user(self):
        first_name = "test_firts_name"
        last_name = "test_last_name"
        username = "test_username"
        user_id = 123123123
        language_code = "fr"
        full_name = f"{first_name} {last_name}"

        user = self.tf.generate_user(
            first_name=first_name,
            last_name=last_name,
            username=username,
            id=user_id,
            is_premium=True,
            is_bot=False,
            language_code=language_code,
        )

        self.assertEqual(user.first_name, first_name)
        self.assertEqual(user.last_name, last_name)
        self.assertEqual(user.username, username)
        self.assertEqual(user.language_code, language_code)
        self.assertEqual(user.id, user_id)
        self.assertEqual(user.full_name, full_name)
        self.assertTrue(user.is_premium)
        self.assertFalse(user.is_bot)

    def test_generate_random_bot(self):
        user_bot = self.tf.generate_random_bot()

        self.assertTrue(user_bot.is_bot)
        self.assertIsNone(user_bot.is_premium)
        self.assertIsNone(user_bot.last_name)
        self.assertIsNone(user_bot.language_code)
        self.assertIsNone(user_bot.added_to_attachment_menu)
        self.assertIsNone(user_bot.supports_inline_queries)
        self.assertIsNone(user_bot.can_read_all_group_messages)

    def test_generate_user_from_chat(self):
        chat = self.tf.generate_random_private_chat()
        user = self.tf.generate_user_from_private_chat(chat)

        self.assertEqual(chat.id, user.id)
        self.assertEqual(chat.first_name, user.first_name)
        self.assertEqual(chat.last_name, user.last_name)
        self.assertEqual(chat.username, user.username)
        self.assertFalse(user.is_bot)

        chat.type = "group"
        with self.assertRaises(AttributeError):
            self.tf.generate_user_from_private_chat(chat)

    def test_generate_random_message_from_user_and_chat(self):
        user = self.tf.generate_random_user()
        chat = self.tf.generate_random_group_chat()

        edit_date = int(datetime.datetime.now().timestamp())
        message = self.tf.generate_random_message_from_user_and_chat(
            user,
            chat,
            edit_date=edit_date,
        )

        self.assertEqual(user.to_json(), message.from_user.to_json())
        self.assertEqual(chat.__dict__, message.chat.__dict__)
        self.assertTrue(message.text)
        self.assertEqual(type(message.id), int)
        self.assertEqual(type(message.date), int)
        self.assertEqual(message.edit_date, edit_date)

    def test_generate_random_messages_chain(self):
        user_0 = self.tf.generate_random_user()
        user_1 = self.tf.generate_random_user()
        chat = self.tf.generate_random_supergroup_chat()

        messages = self.tf.generate_random_messages_chain(
            chat,
            [user_0, user_1],
            quantity=10,
        )
        for message in messages:
            self.assertIn(message.from_user.id, [u.id for u in [user_1, user_0]])
            self.assertEqual(message.chat.__dict__, chat.__dict__)

        with self.assertRaises(AttributeError):
            self.tf.generate_random_messages_chain(chat, [user_0, user_1], quantity=0)

    def test_generate_random_private_chat(self):
        chat = self.tf.generate_random_private_chat()

        self.assertIsNone(chat.title)
        self.assertEqual(chat.type, "private")
        self.assertTrue(chat.first_name)
        self.assertTrue(chat.last_name)
        self.assertTrue(chat.username)

        with self.assertRaises(AttributeError):
            self.tf.generate_random_private_chat(id=1)

        chat = self.tf.generate_random_private_chat(has_protected_content=True)
        self.assertTrue(chat.has_protected_content)

    def test_generate_random_group_chat(self):
        chat = self.tf.generate_random_group_chat()

        self.assertIsNone(chat.title)
        self.assertEqual(chat.type, "group")
        self.assertIsNone(chat.first_name)
        self.assertIsNone(chat.last_name)
        self.assertIsNone(chat.username)

        with self.assertRaises(AttributeError):
            self.tf.generate_random_group_chat(type="private")

        chat = self.tf.generate_random_group_chat(has_protected_content=True)
        self.assertTrue(chat.has_protected_content)

    def test_generate_random_supergroup_chat(self):
        chat = self.tf.generate_random_supergroup_chat()

        self.assertIsNotNone(chat.title)
        self.assertEqual(chat.type, "supergroup")
        self.assertIsNone(chat.first_name)
        self.assertIsNone(chat.last_name)
        self.assertIsNone(chat.username)

        with self.assertRaises(AttributeError):
            self.tf.generate_random_supergroup_chat(title="test_supergroup")

        chat = self.tf.generate_random_supergroup_chat(has_protected_content=True)
        self.assertTrue(chat.has_protected_content)

    def test_generate_random_message_pack(self):
        message, user, chat = self.tf.generate_random_message_pack()

        self.assertEqual(message.from_user.to_json(), user.to_json())
        self.assertEqual(message.chat.__dict__, chat.__dict__)
        self.assertEqual(chat.first_name, user.first_name)
        self.assertEqual(chat.last_name, user.last_name)
        self.assertEqual(chat.username, user.username)

    def test_genetate_random_group_conversation(self):
        len_users = 10
        len_messages = 20

        chat, users, messages = self.tf.genetate_random_group_conversation(
            users_quantity=len_users,
            messages_quantity=len_messages,
        )

        self.assertEqual(len(users), len_users)
        self.assertEqual(len(messages), len_messages)
        for message in messages:
            self.assertIn(message.from_user.id, [u.id for u in users])

        with self.assertRaises(ValueError):
            self.tf.genetate_random_group_conversation(
                users_quantity=-1,
                messages_quantity=1,
            )

        with self.assertRaises(ValueError):
            self.tf.genetate_random_group_conversation(
                users_quantity=1,
                messages_quantity=-1,
            )

    def test_generate_random_callback(self):
        callback_data = "test_callback_data"
        callback_query = self.tf.generate_random_callback(
            callback_data,
            inline_message_id=1,
        )

        self.assertEqual(callback_query.data, callback_data)

        with self.assertRaises(AttributeError):
            self.tf.generate_random_callback(callback_data, data="text")

    def test_generate_callback_from_data(self):
        chat = self.tf.generate_random_private_chat()
        user = self.tf.generate_user_from_private_chat(chat)
        message = self.tf.generate_random_message_from_user_and_chat(user, chat)
        callback_data = "test_data"
        callback_query = self.tf.generate_callback_from_data(
            chat,
            message,
            user,
            callback_data,
        )

        self.assertEqual(callback_query.data, callback_data)
        self.assertEqual(callback_query.chat_instance.__dict__, chat.__dict__)
        self.assertEqual(callback_query.message.json, message.json)
        self.assertEqual(callback_query.from_user.to_json(), user.to_json())
        self.assertEqual(callback_query.message.from_user.to_json(), user.to_json())

        with self.assertRaises(AttributeError):
            self.tf.generate_random_callback(callback_data, data="text")
