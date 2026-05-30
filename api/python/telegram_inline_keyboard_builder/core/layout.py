"""
Shared layout engine for inline keyboard rows.

Used by InlineKeyboardBuilder and the validation normalizer.
"""

from __future__ import annotations

from .types.buttons import InlineKeyboardButton


def layout_buttons(
    buttons: list[InlineKeyboardButton],
    buttons_per_row: int,
    auto_wrap_max_chars: int,
) -> list[list[InlineKeyboardButton]]:
    """
    Arrange a flat button list into rows.

    Respects *buttons_per_row*, *auto_wrap_max_chars*, and explicit
    ``__newRow`` markers.
    """
    rows: list[list[InlineKeyboardButton]] = []
    row: list[InlineKeyboardButton] = []
    row_chars = 0

    def push_row() -> None:
        nonlocal row, row_chars
        if row:
            rows.append(row)
            row = []
            row_chars = 0

    for btn in buttons:
        if btn.get("__newRow"):  # type: ignore[typeddict-item]
            push_row()
            continue

        text_length = len(str(btn.get("text", "")))

        if (
            auto_wrap_max_chars > 0
            and row
            and row_chars + text_length > auto_wrap_max_chars
        ):
            push_row()

        if len(row) >= buttons_per_row:
            push_row()

        row.append(btn)
        row_chars += text_length

    push_row()
    return rows
