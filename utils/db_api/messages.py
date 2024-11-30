import asyncio

import aiofiles
import orjson


class Messages:
    def __init__(self, messages_path='data/translations/{lang_code}.json'):
        self.messages_path = messages_path
        self.messages = {}

    async def load_messages(self):
        # Load files concurrently
        tasks = {
            lang: self._load_file(self.messages_path.format(lang_code=lang))
            for lang in ['uz', 'ru']
        }
        self.messages = await asyncio.gather(*tasks.values())
        self.messages = dict(zip(tasks.keys(), self.messages))

    async def _load_file(self, path):
        try:
            async with aiofiles.open(path, mode='r', encoding='utf-8') as f:
                return orjson.loads(await f.read())
        except FileNotFoundError:
            raise ValueError(f"File not found: {path}")
        except orjson.JSONDecodeError:
            raise ValueError(f"Invalid JSON in file: {path}")

    async def get_message(self, lang_code, message_key):
        return self.messages.get(lang_code, {}).get(message_key, f"Message Key {message_key} not found.")
