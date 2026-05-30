from __future__ import annotations

from ..core.layout import layout_buttons
from .types import KeyboardInput, NormalizedButtonRef, NormalizedKeyboard


def normalize_keyboard(input_data: KeyboardInput) -> NormalizedKeyboard:
    """Normalize keyboard state once for all rules (layout + indexed refs)."""
    buttons = input_data["buttons"]
    buttons_per_row = input_data["buttons_per_row"]
    auto_wrap_max_chars = input_data["auto_wrap_max_chars"]
    rows = layout_buttons(buttons, buttons_per_row, auto_wrap_max_chars)
    flat: list[NormalizedButtonRef] = []
    flat_index = 0

    for row_index, row in enumerate(rows):
        for column_index, button in enumerate(row):
            flat.append(
                NormalizedButtonRef(
                    button=button,
                    row_index=row_index,
                    column_index=column_index,
                    flat_index=flat_index,
                )
            )
            flat_index += 1

    return NormalizedKeyboard(
        rows=rows,
        flat=flat,
        raw_buttons=buttons,
        buttons_per_row=buttons_per_row,
        auto_wrap_max_chars=auto_wrap_max_chars,
        is_empty=len(flat) == 0,
    )
