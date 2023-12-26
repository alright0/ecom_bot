import unittest
from unittest.mock import patch

import sqlalchemy
from sqlalchemy.orm import Session
from sqlalchemy.orm.decl_api import DeclarativeMeta, declarative_base

from app.models import ASSOCIATED_TABLES, TABLES


class TestDataBaseClass(unittest.TestCase):
    def setUp(self):
        self.db_url = "sqlite:///:memory:"
        self.engine = sqlalchemy.create_engine(self.db_url, echo=False)
        self.session = Session(bind=self.engine)
        self.Base: DeclarativeMeta = declarative_base()

        self._migrate()
        patch("app.dao.base_dao.BaseDao.session", self.session).start()

    def _migrate(self):
        for m in TABLES:
            m.__table__.create(self.engine)

        for m in ASSOCIATED_TABLES:
            m.create(self.engine)
