from __future__ import annotations

from ..diagnostics import create_diagnostic
from ..types import Diagnostic, RuleContext, ValidationRule
from .constants import RULE_IDS
from .helpers import loc


def _run(ctx: RuleContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    seen: dict[str, tuple[int, int, int]] = {}

    for ref in ctx.normalized.flat:
        button = ref.button
        if "callback_data" not in button or not isinstance(
            button.get("callback_data"), str
        ):
            continue
        data = button["callback_data"]
        previous = seen.get(data)
        if previous:
            prev_row, prev_col, _ = previous
            diagnostics.append(
                create_diagnostic(
                    RULE_IDS.DUPLICATE_CALLBACK_DATA,
                    f'Duplicate callback_data "{data}"',
                    "warning",
                    loc(ref.row_index, ref.column_index, ref.flat_index, "callback_data"),
                    f"Also used at row {prev_row + 1}, column {prev_col + 1}",
                )
            )
        else:
            seen[data] = (ref.row_index, ref.column_index, ref.flat_index)

    return diagnostics


duplicate_callback_data_rule = ValidationRule(
    id=RULE_IDS.DUPLICATE_CALLBACK_DATA,
    description="Warns when the same callback_data is reused",
    default_severity="warning",
    run=_run,
)
