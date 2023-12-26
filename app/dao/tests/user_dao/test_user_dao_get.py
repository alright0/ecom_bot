from app.dao import UserDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.model_fixture_generator import ModelFixture
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestUserDaoGet(TestDataBaseClass):
    def setUp(self):
        super().setUp()

        self.mf = ModelFixture()
        self.user = TelegramFixture().generate_random_user()
        self.dao = UserDao()

    def test_all_existed_users(self):
        for _ in range(3):
            self.mf.create_model_user(self.user)
        users = self.dao.all()

        self.assertEqual(3, len(users))

    def test_all_non_existed_users(self):
        users = self.dao.all()

        self.assertEqual(0, len(users))
