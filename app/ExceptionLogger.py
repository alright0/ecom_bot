import traceback

import telebot

from app.bot import Bot


class ChatExceptionLogger(telebot.ExceptionHandler):
    def __init__(self, bot: Bot):
        self.bot: Bot = bot
        self.chunk_length: int = 4000
        self.trace_back: str = ""

    def handle(self, exception: Exception):
        self.trace_back = traceback.format_exc(100, chain=True)
        chunks = self._split_chunks()
        for i, chunk in enumerate(chunks, 1):
            chunk_head = (
                f"{i}/{len(chunks)} traceback chunk:\n" if len(chunks) > 1 else ""
            )
            text = f"```bash\n{chunk_head}{chunk}\n```"
            self.bot.send_to_log(text=text, parse_mode="MARKDOWN")
        self.bot.skip_update()

    def _split_chunks(self):
        chunks = []
        for i in range(0, len(self.trace_back), self.chunk_length):
            chunks.append(self.trace_back[i : i + self.chunk_length])
        return chunks
