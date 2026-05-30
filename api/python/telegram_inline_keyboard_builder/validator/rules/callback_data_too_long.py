from __future__ import annotations

from ..diagnostics import create_diagnostic
from ..types import Diagnostic, RuleContext, ValidationRule
from .constants import RULE_IDS, TELEGRAM_CALLBACK_DATA_MAX_BYTES
from .helpers import callback_data_byte_length, loc


def _run(ctx: RuleContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for ref in ctx.normalized.flat:
        button = ref.button
        if "callback_data" not in button or not isinstance(
            button.get("callback_data"), str
        ):
            continue
        data = button["callback_data"]
        byte_len = callback_data_byte_length(data)
        if byte_len > TELEGRAM_CALLBACK_DATA_MAX_BYTES:
            diagnostics.append(
                create_diagnostic(
                    RULE_IDS.CALLBACK_DATA_TOO_LONG,
                    f"callback_data is {byte_len} bytes (max {TELEGRAM_CALLBACK_DATA_MAX_BYTES})",
                    "error",
                    loc(ref.row_index, ref.column_index, ref.flat_index, "callback_data"),
                    "Shorten scope/action/id or compress payload encoding",
                )
            )
    return diagnostics


callback_data_too_long_rule = ValidationRule(
    id=RULE_IDS.CALLBACK_DATA_TOO_LONG,
    description="callback_data must not exceed 64 UTF-8 bytes",
    default_severity="error",
    run=_run,
)
