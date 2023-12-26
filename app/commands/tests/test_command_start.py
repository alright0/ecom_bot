from unittest.mock import MagicMock

from app.commands import COMMANDS, CommandStart
from app.fixtures.base_test_class import TestDataBaseClass
from app.fixtures.telegram_fixture_generator import TelegramFixture


class TestCommandStart(TestDataBaseClass):
    def setUp(self):
        super().setUp()

        self.bot = MagicMock()
        self.message, *_ = TelegramFixture().generate_random_message_pack()
        self.command = CommandStart()

    def test_public_commands_in_message_exec(self):
        self.command.exec(self.message, self.bot)

        for c in COMMANDS:
            if not c.HIDDEN:
                text = self.bot.send_custom_message.call_args[0][1]
                command_represent = f"/{c.COMMANDS[0]} - {c.DESCRIPTION}"
                self.assertIn(command_represent, text)

    def test_hidden_commands_not_in_message_exec(self):
        self.command.exec(self.message, self.bot)

        for c in COMMANDS:
            if c.HIDDEN:
                text = self.bot.send_custom_message.call_args[0][1]
                command_represent = f"/{c.COMMANDS[0]} - {c.DESCRIPTION}"
                self.assertNotIn(command_represent, text)
