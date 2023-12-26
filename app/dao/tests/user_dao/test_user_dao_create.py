from app.dao import UserDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestUserDaoCreate(TestDataBaseClass):
    def setUp(self):
        super().setUp()

        self.user = TelegramFixture().generate_random_user()
        self.dao = UserDao()

    def test_create_user(self):
        self.dao.create(self.user)

        self.assertTrue(self.dao.get(self.user))
        self.assertEqual(1, len(self.dao.all()))
