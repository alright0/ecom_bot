import json
from datetime import datetime
from json import JSONDecodeError
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, Integer, String
from sqlalchemy.orm import Mapped
from sqlalchemy.sql import func

from app import Base


class BaseIdModel(Base):
    __abstract__ = True

    id: Mapped[int] = Column(
        Integer,
        primary_key=True,
        nullable=False,
        unique=True,
        autoincrement=True,
    )


class BaseTimeModel(Base):
    __abstract__ = True

    created: Mapped[datetime] = Column(
        DateTime,
        nullable=False,
        server_default=func.now(),
    )
    updated: Mapped[datetime] = Column(
        DateTime,
        nullable=True,
        onupdate=func.current_timestamp,
        server_default=func.now(),
    )

    @property
    def created_ts(self) -> Optional[int]:
        return int(self.created.timestamp()) if self.created else None

    @property
    def updated_ts(self) -> Optional[int]:
        return int(self.updated.timestamp()) if self.updated else None


class BaseIsDeletedModel(Base):
    __abstract__ = True

    deleted: Mapped[bool] = Column(Boolean, default=False)


class BaseRawFieldModel(Base):
    __abstract__ = True

    raw: Mapped[str] = Column(String, nullable=True)

    @property
    def json(self) -> dict:
        if not self.raw:
            return {}
        try:
            return json.loads(self.raw)
        except JSONDecodeError:
            return {}

    def get_param(self, key):
        return self.json.get(key)

    def set_param(self, key, value):
        data = self.json
        data.update({key: value})
        self.raw = json.dumps(data, ensure_ascii=False)

    def del_param(self, key):
        data = self.json
        try:
            data.pop(key)
            self.raw = json.dumps(data)
        except KeyError:
            pass
