from datetime import datetime
from typing import List, Optional, Tuple, Type

from telebot.types import User as TelegramUser

from app.dao import BaseDao
from app.models import User


class UserDao(BaseDao):
    def get(self, user_data: TelegramUser) -> Optional[User]:
        return self.session.query(User).filter(User.user_id == user_data.id).first()

    def all(self) -> List[Optional[Type[User]]]:
        return self.session.query(User).all()

    def create_or_update(self, user_data: TelegramUser) -> Tuple[User, bool]:
        user = self.get(user_data)
        if user:
            user = self.update(user, user_data)
            created = False
        else:
            user = self.create(user_data)
            created = True
        return user, created

    def update(self, user: User, user_data: TelegramUser) -> User:
        user.first_name = user_data.first_name
        user.last_name = user_data.last_name
        user.username = user_data.username
        user.raw = self.raw(user_data.__dict__)
        user.updated = datetime.utcnow()

        self.session.add(user)
        self.save()

        return user

    def create(self, user_data: TelegramUser) -> User:
        user = User()
        user.user_id = user_data.id
        user.first_name = user_data.first_name
        user.last_name = user_data.last_name
        user.username = user_data.username
        user.raw = self.raw(user_data.__dict__)

        self.session.add(user)
        self.save()

        return user
