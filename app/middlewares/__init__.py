from app.middlewares.base_middleware import BaseMiddleware
from app.middlewares.middleware_user_message import MiddlewareUserMessage

MIDDLEWARES = [
    MiddlewareUserMessage,
]
