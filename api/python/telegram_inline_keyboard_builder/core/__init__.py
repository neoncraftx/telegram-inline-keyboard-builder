"""
telegram-inline-keyboard-builder
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Universal inline keyboard builder for Telegram bots.
Produces pure Telegram Bot API compliant JSON,
usable with any library (python-telegram-bot, Aiogram, Pyrogram, Telebot…).
"""

from .builder import InlineKeyboardBuilder
from .types.buttons import (
    ButtonStyle,
    CallbackButton,
    UrlButton,
    PayButton,
    CustomButton,
    InlineKeyboardButton,
    ButtonConfig,
    GroupedButtonConfig,
)
from .types.utils import (
    PaginationLabels,
    PaginationConfig,
    PaginatedListOptions,
)

__all__ = [
    "InlineKeyboardBuilder",
    # button types
    "ButtonStyle",
    "CallbackButton",
    "UrlButton",
    "PayButton",
    "CustomButton",
    "InlineKeyboardButton",
    "ButtonConfig",
    "GroupedButtonConfig",
    # pagination types
    "PaginationLabels",
    "PaginationConfig",
    "PaginatedListOptions",
]

__version__ = "3.0.0"
__author__  = "neoncraftx"
