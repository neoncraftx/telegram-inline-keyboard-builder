from __future__ import annotations

from ..diagnostics import create_diagnostic
from ..types import Diagnostic, RuleContext, ValidationRule
from .constants import RULE_IDS, TELEGRAM_MAX_BUTTONS_PER_ROW


def _run(ctx: RuleContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    configured_max = max(1, ctx.buttons_per_row)

    for row_index, row in enumerate(ctx.normalized.rows):
        count = len(row)
        if count > configured_max:
            diagnostics.append(
                create_diagnostic(
                    RULE_IDS.TOO_MANY_BUTTONS_PER_ROW,
                    f"Row {row_index + 1} has {count} buttons (configured max {configured_max})",
                    "error",
                    {"row": row_index},
                    "Call newRow() or increase buttonsPerRow intentionally",
                )
            )
        if count > TELEGRAM_MAX_BUTTONS_PER_ROW:
            diagnostics.append(
                create_diagnostic(
                    RULE_IDS.TOO_MANY_BUTTONS_PER_ROW,
                    f"Row {row_index + 1} has {count} buttons (Telegram max {TELEGRAM_MAX_BUTTONS_PER_ROW})",
                    "error",
                    {"row": row_index},
                )
            )

    return diagnostics


too_many_buttons_per_row_rule = ValidationRule(
    id=RULE_IDS.TOO_MANY_BUTTONS_PER_ROW,
    description="Rows must not exceed configured or Telegram limits",
    default_severity="error",
    run=_run,
)
