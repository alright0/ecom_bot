from typing import Callable, Optional

import telebot
from telebot import HandlerBackend, StateMemoryStorage, StateStorageBase
from telebot.types import Message as TelegramMssage

from app.config import config
from app.dao import ChatDao, MessageDao, UserDao


class Bot(telebot.TeleBot):
    telebot.apihelper.ENABLE_MIDDLEWARE = True
    owner_id = config.owner

    def __init__(
        self,
        token: str,
        parse_mode: Optional[str] = None,
        threaded: Optional[bool] = True,
        skip_pending: Optional[bool] = False,
        num_threads: Optional[int] = 2,
        next_step_backend: Optional[HandlerBackend] = None,
        reply_backend: Optional[HandlerBackend] = None,
        exception_handler: Optional[telebot.ExceptionHandler] = None,
        last_update_id: Optional[int] = 0,
        suppress_middleware_excepions: Optional[bool] = False,
        state_storage: Optional[StateStorageBase] = StateMemoryStorage(),
        use_class_middlewares: Optional[bool] = False,
        disable_web_page_preview: Optional[bool] = None,
        disable_notification: Optional[bool] = None,
        protect_content: Optional[bool] = None,
        allow_sending_without_reply: Optional[bool] = None,
        colorful_logs: Optional[bool] = False,
    ):
        super().__init__(
            token=token,
            parse_mode=parse_mode,
            threaded=threaded,
            skip_pending=skip_pending,
            num_threads=num_threads,
            next_step_backend=next_step_backend,
            reply_backend=reply_backend,
            exception_handler=exception_handler,
            suppress_middleware_excepions=suppress_middleware_excepions,
            last_update_id=last_update_id,
            state_storage=state_storage,
            use_class_middlewares=use_class_middlewares,
            disable_web_page_preview=disable_web_page_preview,
            disable_notification=disable_notification,
            protect_content=protect_content,
            allow_sending_without_reply=allow_sending_without_reply,
            colorful_logs=colorful_logs,
        )
        config.bot_id = self.get_me().id

    def skip_update(self):
        self.set_webhook(drop_pending_updates=True)
        self.delete_webhook(drop_pending_updates=True)

    def send_to_log(self, text: str, *args, **kwargs) -> TelegramMssage:
        return self.send_custom_message(
            chat_id=config.log_chat, text=text, *args, **kwargs
        )

    def send_custom_message(self, *args, **kwargs) -> TelegramMssage:
        return self._wrap(self.send_message, *args, **kwargs)

    def send_custom_animation(self, *args, **kwargs) -> TelegramMssage:
        return self._wrap(self.send_animation, *args, **kwargs)

    def send_custom_photo(self, *args, **kwargs) -> TelegramMssage:
        return self._wrap(self.send_photo, *args, **kwargs)

    def send_custom_document(self, *args, **kwargs) -> TelegramMssage:
        return self._wrap(self.send_document, *args, **kwargs)

    def send_custom_video(self, *args, **kwargs) -> TelegramMssage:
        return self._wrap(self.send_video, *args, **kwargs)

    def send_custom_voice(self, *args, **kwargs) -> TelegramMssage:
        return self._wrap(self.send_voice, *args, **kwargs)

    def send_custom_video_note(self, *args, **kwargs) -> TelegramMssage:
        return self._wrap(self.send_video_note, *args, **kwargs)

    def custom_reply_to(self, *args, **kwargs) -> TelegramMssage:
        return self._wrap(self.reply_to, *args, **kwargs)

    def custom_edit_message_text(self, *args, **kwargs) -> TelegramMssage:
        return self._wrap(self.edit_message_text, *args, **kwargs)

    def custom_edit_message_caption(self, *args, **kwargs) -> TelegramMssage:
        return self._wrap(self.edit_message_caption, *args, **kwargs)

    def _wrap(self, send_func: Callable, *args, **kwargs) -> TelegramMssage:
        message = send_func(*args, **kwargs)
        chat, _ = ChatDao().create_or_update(message.chat)
        user, _ = UserDao().create_or_update(message.from_user)
        MessageDao().create_or_update(message, chat, user)

        return message
