from app.dao import UserDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.model_fixture_generator import ModelFixture
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestUserDaoUpdate(TestDataBaseClass):
    def setUp(self):
        super().setUp()

        self.mf = ModelFixture()
        self.user_data = TelegramFixture().generate_random_user()
        self.user = self.mf.create_model_user(self.user_data)
        self.dao = UserDao()

    def test_update_user(self):
        user = self.dao.get(self.user_data)
        user_updated_old = user.updated

        updated_user = self.dao.update(self.user, self.user_data)
        user_updated_new = updated_user.updated

        self.assertNotEqual(user_updated_old, user_updated_new)
