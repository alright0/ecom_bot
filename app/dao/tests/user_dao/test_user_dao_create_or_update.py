from app.dao import UserDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestUserDaoCreateOrUpdate(TestDataBaseClass):
    def setUp(self):
        super().setUp()

        self.user_data = TelegramFixture().generate_random_user()
        self.dao = UserDao()

    def test_create_user(self):
        user, created = self.dao.create_or_update(self.user_data)

        self.assertTrue(created)

    def test_update_user(self):
        user = self.dao.create(self.user_data)
        user_updated_old = user.updated
        updated_user, created = self.dao.create_or_update(self.user_data)

        self.assertFalse(created)
        self.assertNotEqual(user_updated_old, updated_user.updated)
