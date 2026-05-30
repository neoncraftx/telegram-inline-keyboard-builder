from __future__ import annotations

from ..diagnostics import create_diagnostic
from ..types import Diagnostic, RuleContext, ValidationRule
from .constants import RULE_IDS


def _run(ctx: RuleContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    for i, row in enumerate(ctx.normalized.rows):
        if len(row) == 0:
            diagnostics.append(
                create_diagnostic(
                    RULE_IDS.EMPTY_ROW,
                    f"Row {i + 1} has no buttons",
                    "warning",
                    {"row": i},
                )
            )

    pending_break = False
    for raw in ctx.normalized.raw_buttons:
        if raw.get("__newRow"):
            if pending_break:
                diagnostics.append(
                    create_diagnostic(
                        RULE_IDS.EMPTY_ROW,
                        "Consecutive newRow() markers can produce empty rows",
                        "warning",
                    )
                )
            pending_break = True
            continue
        pending_break = False

    return diagnostics


empty_row_rule = ValidationRule(
    id=RULE_IDS.EMPTY_ROW,
    description="Detects rows without buttons after layout",
    default_severity="warning",
    run=_run,
)
