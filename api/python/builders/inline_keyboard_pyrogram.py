from core.inline_keyboard_builder import InlineKeyboardBuilder
from adapters.pyrogram_adapter import PyrogramInlineAdapter


class InlineKeyboardPyrogram(InlineKeyboardBuilder):
    def __init__(self, buttons_per_row=2, auto_wrap_max_chars=0):
        super().__init__(PyrogramInlineAdapter(), buttons_per_row, auto_wrap_max_chars)
ow,
            auto_wrap_max_chars
        )