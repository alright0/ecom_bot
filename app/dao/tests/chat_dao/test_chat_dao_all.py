from app.dao import ChatDao
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.model_fixture_generator import ModelFixture


class TestChatDaoAll(TestDataBaseClass):
    def setUp(self):
        super().setUp()

        self.mf = ModelFixture()
        for i in range(4):
            self.mf.create_model_chat()
        self.dao = ChatDao()

    def test_get_all_chats(self):
        chats = self.dao.all()

        self.assertEqual(4, len(chats))

    def test_get_wrong_count_chats(self):
        chats = self.dao.all()

        self.assertNotEqual(5, len(chats))
