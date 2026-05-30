from __future__ import annotations

from ..diagnostics import create_diagnostic
from ..types import Diagnostic, RuleContext, ValidationRule
from .constants import RULE_IDS
from .helpers import loc


def _run(ctx: RuleContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for ref in ctx.normalized.flat:
        text = ref.button.get("text")
        if not isinstance(text, str) or text.strip() == "":
            diagnostics.append(
                create_diagnostic(
                    RULE_IDS.EMPTY_BUTTON_TEXT,
                    "Button text is empty or whitespace-only",
                    "error",
                    loc(ref.row_index, ref.column_index, ref.flat_index, "text"),
                )
            )
    return diagnostics


empty_button_text_rule = ValidationRule(
    id=RULE_IDS.EMPTY_BUTTON_TEXT,
    description="Button text must be non-empty",
    default_severity="error",
    run=_run,
)
