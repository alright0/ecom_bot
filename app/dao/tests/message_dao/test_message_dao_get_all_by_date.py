from datetime import datetime, timedelta

from telebot.types import Message, User

from app.dao import MessageDao, UserDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.model_fixture_generator import ModelFixture
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestMessageDaoCreateOrUpdate(TestDataBaseClass):
    def setUp(self):
        super().setUp()

        self.tf = TelegramFixture()
        self.mf = ModelFixture()
        self.dao = MessageDao()
        self.user_dao = UserDao()

        self.chat_data_1 = self.tf.generate_random_group_chat()
        self.chat_data_2 = self.tf.generate_random_group_chat()
        self.chat_data_3 = self.tf.generate_random_group_chat()
        self.chat_data_with_parent = self.tf.generate_random_supergroup_chat()
        self.chat_1 = self.mf.create_model_chat(self.chat_data_1)
        self.chat_2 = self.mf.create_model_chat(self.chat_data_2)
        self.chat_3 = self.mf.create_model_chat(self.chat_data_3)
        self.chat_with_parent = self.mf.create_model_chat(self.chat_data_with_parent)

        self.user_data_1 = self.tf.generate_random_user()
        self.user_data_2 = self.tf.generate_random_user()
        self.user_data_3 = self.tf.generate_random_user()
        self.user_data_4 = self.tf.generate_random_user()
        self.user_data_migrator_bot = User.de_json(
            {
                "id": 1087968824,
                "is_bot": True,
                "first_name": "Group",
                "username": "GroupAnonymousBot",
            },
        )
        self.user_1 = self.mf.create_model_user(self.user_data_1)
        self.user_2 = self.mf.create_model_user(self.user_data_2)
        self.user_3 = self.mf.create_model_user(self.user_data_3)
        self.user_4 = self.mf.create_model_user(self.user_data_4)
        self.user_migrator_bot = self.mf.create_model_user(self.user_data_migrator_bot)

        self.chat_1_users = [self.user_data_1, self.user_data_2, self.user_data_3]
        self.chat_1_messages_count = 35
        self.messages_in_chat_1 = self.tf.generate_random_messages_chain(
            self.chat_data_1,
            self.chat_1_users,
            self.chat_1_messages_count,
        )

        for message in self.messages_in_chat_1:
            user = self.user_dao.get(message.from_user)
            self.dao.create(message, self.chat_1, user)

        self.chat_2_users = [self.user_data_1, self.user_data_2]
        self.chat_2_messages_count = 60
        self.messages_in_chat_2 = self.tf.generate_random_messages_chain(
            self.chat_data_2,
            self.chat_2_users,
            self.chat_2_messages_count,
        )

        for message in self.messages_in_chat_2:
            user = self.user_dao.get(message.from_user)
            self.dao.create(message, self.chat_2, user)

        self.chat_3_users = [self.user_data_1, self.user_data_3, self.user_data_4]
        self.chat_3_messages_count = 100
        self.messages_in_chat_3 = self.tf.generate_random_messages_chain(
            self.chat_data_3,
            self.chat_3_users,
            self.chat_3_messages_count,
        )

        for message in self.messages_in_chat_3:
            user = self.user_dao.get(message.from_user)
            self.dao.create(message, self.chat_3, user)

        self.chat_with_parent_users = [self.user_data_1, self.user_data_2]
        self.chat_with_parent_messages_count = 10
        self.messages_in_chat_with_parent = self.tf.generate_random_messages_chain(
            self.chat_data_with_parent,
            self.chat_with_parent_users,
            self.chat_with_parent_messages_count,
        )

        self.migration_message_data = Message.de_json(
            {
                "message_id": 1,
                "from": self.user_data_migrator_bot.to_json(),
                "sender_chat": {
                    "id": self.chat_data_with_parent.id,
                    "title": "test_chat",
                    "type": "supergroup",
                },
                "chat": {
                    "id": self.chat_data_with_parent.id,
                    "title": "test_chat",
                    "type": "supergroup",
                },
                "date": 1692445861,
                "migrate_from_chat_id": self.chat_data_1.id,
            },
        )

        migration_message = self.dao.create(
            self.migration_message_data,
            self.chat_with_parent,
            self.user_migrator_bot,
        )

        for message in self.messages_in_chat_with_parent:
            user = self.user_dao.get(message.from_user)
            self.dao.create(message, self.chat_with_parent, user)

    def test_get_all_messages_by_date(self):
        """сообщения из чата, от которого прошла миграция, тоже попадают в статистику подсчета."""

        start_date = datetime.now() - timedelta(hours=10)
        end_date = datetime.now() + timedelta(hours=10)

        all_messages_in_chat_1 = self.dao.get_all_by_date(
            self.chat_1,
            start_date,
            end_date,
        )
        self.assertEqual(len(all_messages_in_chat_1), len(self.messages_in_chat_1))
        self.assertEqual(
            len(set(m.user_id for m in all_messages_in_chat_1)),
            len(self.chat_1_users),
        )

        all_messages_in_chat_2 = self.dao.get_all_by_date(
            self.chat_2,
            start_date,
            end_date,
        )
        self.assertEqual(len(all_messages_in_chat_2), len(self.messages_in_chat_2))
        self.assertEqual(
            len(set(m.user_id for m in all_messages_in_chat_2)),
            len(self.chat_2_users),
        )

        all_messages_in_chat_3 = self.dao.get_all_by_date(
            self.chat_3,
            start_date,
            end_date,
        )
        self.assertEqual(len(all_messages_in_chat_3), len(self.messages_in_chat_3))
        self.assertEqual(
            len(set(m.user_id for m in all_messages_in_chat_3)),
            len(self.chat_3_users),
        )

    def test_get_all_messages_by_date_with_parent_chat(self):
        start_date = datetime.now() - timedelta(hours=10)
        end_date = datetime.now() + timedelta(hours=10)

        all_messages_in_parent_chat = self.dao.get_all_by_date(
            self.chat_1,
            start_date,
            end_date,
        )

        self.assertEqual(len(all_messages_in_parent_chat), len(self.messages_in_chat_1))
        self.assertEqual(
            len(set(m.user_id for m in all_messages_in_parent_chat)),
            len(self.chat_1_users),
        )

        all_messages_in_chat_with_parent = self.dao.get_all_by_date(
            self.chat_with_parent,
            start_date,
            end_date,
        )
        all_messages = (
            self.chat_1_messages_count + self.chat_with_parent_messages_count + 1
        )
        self.assertEqual(all_messages, len(all_messages_in_chat_with_parent))
