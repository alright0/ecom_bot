import pandas as pd
from telebot.types import BotCommand

from app.bot import Bot
from app.callbacks import CALLBACKS
from app.commands import COMMANDS
from app.config import config
from app.ExceptionLogger import ChatExceptionLogger
from app.log import init_logging
from app.message_handlers import HANDLERS
from app.middlewares import MIDDLEWARES

pd.options.plotting.backend = "plotly"


bot = Bot(config.token)
bot.exception_handler = ChatExceptionLogger(bot)

init_logging(config)

bot.set_my_commands(
    [BotCommand(c.COMMANDS[0], c.DESCRIPTION) for c in COMMANDS if not c.HIDDEN],
)

for command in COMMANDS:
    bot.register_message_handler(
        callback=command.exec,
        commands=command.COMMANDS if not command.COMMAND_REGEX else None,
        pass_bot=command.PASS_BOT,
        regexp=command.COMMAND_REGEX,
    )

for callback in CALLBACKS:
    bot.register_callback_query_handler(
        callback=callback.exec,
        func=callback.trigger,
        pass_bot=callback.PASS_BOT,
    )

for middleware in MIDDLEWARES:
    bot.register_middleware_handler(
        callback=middleware.exec,
        update_types=middleware.UPDATE_TYPES,
    )

for handler in HANDLERS:
    bot.register_message_handler(
        callback=handler.exec,
        func=handler.trigger,
        pass_bot=handler.PASS_BOT,
    )

# bot.register_shipping_query_handler(
#
# )

if __name__ == "__main__":
    bot.infinity_polling(interval=0, timeout=600)
