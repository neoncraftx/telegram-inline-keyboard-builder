from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


class AiogramInlineAdapter:
    def create_callback(self, text, data, hide=False):
        return InlineKeyboardButton(text=text, callback_data=data)

    def create_url(self, text, url, hide=False):
        return InlineKeyboardButton(text=text, url=url)

    def create_pay(self, text, hide=False):
        return InlineKeyboardButton(text=text, pay=True)

    def build_keyboard(self, rows):
        keyboard = InlineKeyboardMarkup(inline_keyboard=rows)
        return keyboard