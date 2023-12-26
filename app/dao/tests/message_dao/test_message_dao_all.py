from app.dao import MessageDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.model_fixture_generator import ModelFixture


class TestMessageDaoAll(TestDataBaseClass):
    def test_create_message(self):
        self.mf = ModelFixture()
        self.mf.create_model_message()
        self.mf.create_model_message()
        self.mf.create_model_message()

        messages = MessageDao().all()

        self.assertEqual(len(messages), 3)
