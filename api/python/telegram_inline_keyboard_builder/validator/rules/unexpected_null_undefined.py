from __future__ import annotations

from ..diagnostics import create_diagnostic
from ..types import Diagnostic, RuleContext, ValidationRule
from .constants import RULE_IDS
from .helpers import has_unexpected_null, loc


def _run(ctx: RuleContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    for ref in ctx.normalized.flat:
        button = ref.button

        if has_unexpected_null(button):
            diagnostics.append(
                create_diagnostic(
                    RULE_IDS.UNEXPECTED_NULL_UNDEFINED,
                    "Button entry is null or undefined",
                    "error",
                    loc(ref.row_index, ref.column_index, ref.flat_index),
                )
            )
            continue

        if has_unexpected_null(button.get("text")):
            diagnostics.append(
                create_diagnostic(
                    RULE_IDS.UNEXPECTED_NULL_UNDEFINED,
                    "Button text is null or undefined",
                    "error",
                    loc(ref.row_index, ref.column_index, ref.flat_index, "text"),
                )
            )

        if "callback_data" in button and has_unexpected_null(
            button.get("callback_data")
        ):
            diagnostics.append(
                create_diagnostic(
                    RULE_IDS.UNEXPECTED_NULL_UNDEFINED,
                    "callback_data is null or undefined",
                    "error",
                    loc(
                        ref.row_index,
                        ref.column_index,
                        ref.flat_index,
                        "callback_data",
                    ),
                )
            )

        if "url" in button and has_unexpected_null(button.get("url")):
            diagnostics.append(
                create_diagnostic(
                    RULE_IDS.UNEXPECTED_NULL_UNDEFINED,
                    "url is null or undefined",
                    "error",
                    loc(ref.row_index, ref.column_index, ref.flat_index, "url"),
                )
            )

    return diagnostics


unexpected_null_undefined_rule = ValidationRule(
    id=RULE_IDS.UNEXPECTED_NULL_UNDEFINED,
    description="Detects null or undefined in required button fields",
    default_severity="error",
    run=_run,
)
