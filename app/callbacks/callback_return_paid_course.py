from telebot.types import CallbackQuery

from app.bot import Bot
from app.callbacks import BaseCallback
from app.config import config
from app.constants import CALLBACK_SHOW_TEST_COURSE


class CallbackReturnPaidCourse(BaseCallback):
    @classmethod
    def exec(cls, call: CallbackQuery, bot: Bot):
        material = f"{config.media_path}/example_material_stage_1.txt"
        with open(material, "rb") as f:
            file = f.read()
            bot.send_custom_document(
                chat_id=call.message.chat.id,
                document=file,
                visible_file_name="Обучающие материалы 1.txt",
                caption="Обучающие материалы по курсу",
            )

    @classmethod
    def trigger(cls, call: CallbackQuery) -> bool:
        return call.data == CALLBACK_SHOW_TEST_COURSE
