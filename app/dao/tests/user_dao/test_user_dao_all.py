from app.dao import UserDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.model_fixture_generator import ModelFixture
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestUserDaoAll(TestDataBaseClass):
    def setUp(self):
        super().setUp()

        self.mf = ModelFixture()
        self.user = TelegramFixture().generate_random_user()
        self.dao = UserDao()

    def test_get_existed_user(self):
        self.mf.create_model_user(self.user)
        user_exists = self.dao.get(self.user)

        self.assertTrue(user_exists)

    def test_get_non_existed_user(self):
        user_exists = self.dao.get(self.user)

        self.assertFalse(user_exists)
