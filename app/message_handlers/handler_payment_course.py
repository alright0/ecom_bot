from app.bot import Bot
from app.config import config
from app.message_handlers import BaseHandler
from app.models import Message


class HandlerGivePaymentCourse(BaseHandler):
    REGEXP = None
    PASS_BOT = True
    CONTENT_TYPE = ["successful_payment"]

    @classmethod
    def exec(cls, message: Message, bot: Bot):
        super().exec(message, bot)

        bot.send_custom_message(
            chat_id=message.chat.id,
            text="Поздравляем с покупкой! Вы успешно оплатили обучающие материалы, "
            "теперь они доступны в списке ваших материалов в разделе /courses",
        )

        material = f"{config.media_path}/example_material_stage_1.txt"
        with open(material, "rb") as f:
            file = f.read()
            bot.send_document(
                chat_id=message.chat.id,
                document=file,
                visible_file_name="Обучающие материалы.txt",
            )

        # 1111111111111026

    @classmethod
    def trigger(cls, message: Message) -> bool:
        return True
