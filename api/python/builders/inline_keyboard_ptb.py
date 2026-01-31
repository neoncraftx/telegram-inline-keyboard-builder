from core.inline_keyboard_builder import InlineKeyboardBuilder
from adapters.ptb_adapter import PTBInlineAdapter


class InlineKeyboardPTB(InlineKeyboardBuilder):
    def __init__(self, buttons_per_row=2, auto_wrap_max_chars=0):
        super().__init__(
            PTBInlineAdapter(),
            buttons_per_row,
            auto_wrap_max_chars
        )