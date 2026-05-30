from __future__ import annotations

from urllib.parse import urlparse

from ...core.types.buttons import InlineKeyboardButton
from ..types import DiagnosticLocation


def loc(
    row_index: int,
    column_index: int,
    flat_index: int,
    field: str | None = None,
) -> DiagnosticLocation:
    location: DiagnosticLocation = {
        "row": row_index,
        "column": column_index,
        "flat_index": flat_index,
    }
    if field is not None:
        location["field"] = field
    return location


def callback_data_byte_length(data: str) -> int:
    return len(data.encode("utf-8"))


def is_valid_http_url(url: str) -> bool:
    try:
        parsed = urlparse(url)
        return parsed.scheme in ("http", "https")
    except Exception:
        return False


def button_kind(
    button: InlineKeyboardButton,
) -> str:
    if not button or not isinstance(button, dict):
        return "invalid"
    if button.get("pay") is True:
        return "pay"
    if "callback_data" in button and button.get("callback_data") is not None:
        return "callback"
    if "url" in button and button.get("url") is not None:
        return "url"
    if "text" in button:
        return "custom"
    return "invalid"


def has_unexpected_null(value: object) -> bool:
    return value is None
