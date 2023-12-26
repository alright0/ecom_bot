from app.models.base_models import BaseIdModel, BaseRawFieldModel, BaseTimeModel
from app.models.chats import Chat
from app.models.message import Message
from app.models.users import User

TABLES = [
    User,
    Chat,
    Message,
]

ASSOCIATED_TABLES = []
