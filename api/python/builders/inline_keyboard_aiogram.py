from core.inline_keyboard_builder import InlineKeyboardBuilder
from adapters.aiogram_adapter import AiogramInlineAdapter


class InlineKeyboardAiogram(InlineKeyboardBuilder):
    def __init__(self, buttons_per_row=2, auto_wrap_max_chars=0):
        super().__init__(
            AiogramInlineAdapter(),
            buttons_per_row,
            auto_wrap_max_chars
        )