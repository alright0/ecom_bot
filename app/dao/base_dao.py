import json
import logging
from abc import ABC

from sqlalchemy.orm import Session

from app import session

logger = logging.getLogger("manual")


class BaseDao(ABC):
    session: Session = session

    def save(self) -> None:
        try:
            self.session.commit()
        except Exception as e:
            self.session.rollback()
            self.session.close()
            logger.error(f"Database exception in BaseDao: {e}")

    def raw(self, cls_dict):
        return json.dumps(cls_dict, ensure_ascii=False)
