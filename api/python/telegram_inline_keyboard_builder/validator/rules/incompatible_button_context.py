from __future__ import annotations

from ..diagnostics import create_diagnostic
from ..types import Diagnostic, RuleContext, ValidationRule
from .constants import RULE_IDS
from .helpers import button_kind, loc


def _run(ctx: RuleContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    context_type = ctx.context_type

    for ref in ctx.normalized.flat:
        button = ref.button
        kind = button_kind(button)

        if kind == "pay" and context_type != "invoice":
            diagnostics.append(
                create_diagnostic(
                    RULE_IDS.INCOMPATIBLE_BUTTON_CONTEXT,
                    "Pay buttons are only valid in invoice keyboards",
                    "error",
                    loc(ref.row_index, ref.column_index, ref.flat_index),
                    'Set validate(context_type="invoice") when building payment keyboards',
                )
            )

        has_callback = (
            "callback_data" in button and button.get("callback_data") is not None
        )
        has_url = "url" in button and button.get("url") is not None
        has_pay = button.get("pay") is True
        action_count = sum([has_callback, has_url, has_pay])
        if action_count > 1:
            diagnostics.append(
                create_diagnostic(
                    RULE_IDS.INCOMPATIBLE_BUTTON_CONTEXT,
                    "Button defines multiple mutually exclusive actions",
                    "error",
                    loc(ref.row_index, ref.column_index, ref.flat_index),
                )
            )

        if kind == "custom" and context_type == "invoice":
            diagnostics.append(
                create_diagnostic(
                    RULE_IDS.INCOMPATIBLE_BUTTON_CONTEXT,
                    "Custom buttons without url/callback/pay are unusual in invoice context",
                    "warning",
                    loc(ref.row_index, ref.column_index, ref.flat_index),
                )
            )

    return diagnostics


incompatible_button_context_rule = ValidationRule(
    id=RULE_IDS.INCOMPATIBLE_BUTTON_CONTEXT,
    description="Buttons must match the declared validation context",
    default_severity="error",
    run=_run,
)
