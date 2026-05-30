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
from ..validator import (
    RULE_IDS,
    TELEGRAM_CALLBACK_DATA_MAX_BYTES,
    TELEGRAM_MAX_BUTTONS_PER_ROW,
    ValidationEngine,
    ValidationError,
    builtin_rules,
    create_diagnostic,
    create_validation_engine,
    normalize_keyboard,
)
from ..validator.types import (
    Diagnostic,
    DiagnosticLocation,
    DiagnosticSeverity,
    KeyboardInput,
    PluginSetupRegistry,
    RuleContext,
    RuleSeverityOverride,
    RulesConfig,
    ValidateOptions,
    ValidationContextType,
    ValidationMode,
    ValidationPlugin,
    ValidationResult,
    ValidationRule,
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
    # validation
    "ValidationEngine",
    "create_validation_engine",
    "ValidationError",
    "create_diagnostic",
    "normalize_keyboard",
    "builtin_rules",
    "RULE_IDS",
    "TELEGRAM_CALLBACK_DATA_MAX_BYTES",
    "TELEGRAM_MAX_BUTTONS_PER_ROW",
    "Diagnostic",
    "DiagnosticLocation",
    "DiagnosticSeverity",
    "KeyboardInput",
    "PluginSetupRegistry",
    "RuleContext",
    "RuleSeverityOverride",
    "RulesConfig",
    "ValidateOptions",
    "ValidationContextType",
    "ValidationMode",
    "ValidationPlugin",
    "ValidationResult",
    "ValidationRule",
]

__version__ = "3.2.3"
__author__  = "neoncraftx"
