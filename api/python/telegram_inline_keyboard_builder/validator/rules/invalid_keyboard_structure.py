from __future__ import annotations

from ..diagnostics import create_diagnostic
from ..types import Diagnostic, RuleContext, ValidationRule
from .constants import RULE_IDS
from .helpers import button_kind, loc


def _run(ctx: RuleContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    if not isinstance(ctx.normalized.raw_buttons, list):
        diagnostics.append(
            create_diagnostic(
                RULE_IDS.INVALID_KEYBOARD_STRUCTURE,
                "buttons must be an array",
                "error",
            )
        )
        return diagnostics

    if ctx.normalized.is_empty:
        diagnostics.append(
            create_diagnostic(
                RULE_IDS.INVALID_KEYBOARD_STRUCTURE,
                "Keyboard has no buttons",
                "warning",
            )
        )

    flat_index = 0
    for raw in ctx.normalized.raw_buttons:
        if raw.get("__newRow"):
            continue
        if not isinstance(raw, dict):
            diagnostics.append(
                create_diagnostic(
                    RULE_IDS.INVALID_KEYBOARD_STRUCTURE,
                    "Invalid button entry (not an object)",
                    "error",
                    {"flat_index": flat_index},
                )
            )
            flat_index += 1
            continue

        if button_kind(raw) == "invalid":
            diagnostics.append(
                create_diagnostic(
                    RULE_IDS.INVALID_KEYBOARD_STRUCTURE,
                    "Button has no recognized action (callback_data, url, or pay)",
                    "error",
                    {"flat_index": flat_index},
                )
            )

        flat_index += 1

    for ref in ctx.normalized.flat:
        if not isinstance(ref.button, dict):
            diagnostics.append(
                create_diagnostic(
                    RULE_IDS.INVALID_KEYBOARD_STRUCTURE,
                    "Laid-out button is not an object",
                    "error",
                    loc(ref.row_index, ref.column_index, ref.flat_index),
                )
            )

    return diagnostics


invalid_keyboard_structure_rule = ValidationRule(
    id=RULE_IDS.INVALID_KEYBOARD_STRUCTURE,
    description="Validates overall keyboard structural integrity",
    default_severity="error",
    run=_run,
)
