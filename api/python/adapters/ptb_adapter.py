from telegram import InlineKeyboardButton, InlineKeyboardMarkup


class PTBInlineAdapter:
    def create_callback(self, text, data, hide=False):
        return InlineKeyboardButton(text=text, callback_data=data)

    def create_url(self, text, url, hide=False):
        return InlineKeyboardButton(text=text, url=url)

    def create_pay(self, text, hide=False):
        return InlineKeyboardButton(text=text, pay=True)

    def build_keyboard(self, rows):
        return InlineKeyboardMarkup(rows)