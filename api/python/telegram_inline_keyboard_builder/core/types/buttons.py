"""
Button type definitions for the Telegram Inline Keyboard Builder.

Mirrors the TypeScript types in buttons.ts.
All types are fully compatible with the Telegram Bot API inline_keyboard schema.
"""

from __future__ import annotations
from typing import Literal, Union
from typing_extensions import TypedDict, Required, NotRequired


# ---------------------------------------------------------------------------
# Primitives
# ---------------------------------------------------------------------------

#: Visual style applied to a premium Telegram button.
ButtonStyle = Literal["primary", "danger", "success"]

#: Telegram custom emoji identifier (requires bot owner premium subscription).
CustomEmojiId = str


# ---------------------------------------------------------------------------
# Button TypedDicts
# ---------------------------------------------------------------------------

class _ButtonBase(TypedDict, total=False):
    """
    Shared fields present on every button type.
    """
    style: ButtonStyle
    """Optional visual style of the button."""

    icon_custom_emoji_id: CustomEmojiId
    """Optional premium emoji icon displayed on the button."""

    __newRow: bool
    """Internal row-break marker — never sent to Telegram."""


class CallbackButton(_ButtonBase, total=False):
    """
    Inline button that triggers a callback query when pressed.

    Example::

        btn: CallbackButton = {
            "text": "✅ Confirm",
            "callback_data": "confirm:action:42",
        }
    """
    text: Required[str]
    """Label displayed on the button."""

    callback_data: Required[str]
    """Data sent back in the callback query (max 64 bytes)."""


class UrlButton(_ButtonBase, total=False):
    """
    Inline button that opens an external URL when pressed.

    Example::

        btn: UrlButton = {
            "text": "📖 Docs",
            "url": "https://example.com",
        }
    """
    text: Required[str]
    """Label displayed on the button."""

    url: Required[str]
    """URL to open when the button is pressed."""


class PayButton(_ButtonBase, total=False):
    """
    Telegram payment button.

    .. warning::
        Must only be used inside ``sendInvoice`` / ``replyWithInvoice``.
        Using it in regular messages causes a Telegram API error.

    Example::

        btn: PayButton = {"text": "💳 Pay now", "pay": True}
    """
    text: Required[str]
    """Label displayed on the button."""

    pay: Required[bool]
    """Must be ``True`` to activate Telegram payment behavior."""


class CustomButton(_ButtonBase, total=False):
    """
    Fully custom inline button.
    Use for Telegram button types not explicitly covered by this library.

    Example::

        btn: CustomButton = {
            "text": "🔔 Subscribe",
            "switch_inline_query": "start",
        }
    """
    text: Required[str]
    """Label displayed on the button."""


#: Union of all supported inline keyboard button types.
InlineKeyboardButton = Union[CallbackButton, UrlButton, PayButton, CustomButton]


# ---------------------------------------------------------------------------
# Config-based API types  (used by add_buttons())
# ---------------------------------------------------------------------------

#: Supported button configuration types.
ButtonConfigType = Literal["callback", "url", "pay", "custom"]


class ButtonConfig(TypedDict, total=False):
    """
    Declarative configuration describing a single button.
    Used by :meth:`~builder.InlineKeyboardBuilder.add_buttons`.

    Example::

        cfg: ButtonConfig = {
            "type": "callback",
            "text": "OK",
            "data": "ok_action",
        }
    """
    type: Required[ButtonConfigType]
    """Behavior type of the button."""

    text: Required[str]
    """Label displayed on the button."""

    data: NotRequired[str]
    """Callback data — required when ``type == "callback"``."""

    url: NotRequired[str]
    """URL — required when ``type == "url"``."""

    button: NotRequired[InlineKeyboardButton]
    """Raw button object — required when ``type == "custom"``."""


class GroupedButtonConfig(TypedDict):
    """
    Groups multiple buttons under a shared type.
    Used by :meth:`~builder.InlineKeyboardBuilder.add_buttons`.

    Example::

        cfg: GroupedButtonConfig = {
            "type": "callback",
            "buttons": [
                {"text": "Yes", "data": "answer:yes"},
                {"text": "No",  "data": "answer:no"},
            ],
        }
    """
    type: ButtonConfigType
    """Shared behavior type for all buttons in the group."""

    buttons: list[ButtonConfig]
    """List of button configurations."""
