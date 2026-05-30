from __future__ import annotations

import math

from ..diagnostics import create_diagnostic
from ..types import Diagnostic, RuleContext, ValidationRule
from .constants import RULE_IDS
from .helpers import loc

_ALLOWED_STYLES = frozenset({"primary", "danger", "success"})


def _run(ctx: RuleContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []

    if not math.isfinite(ctx.buttons_per_row) or ctx.buttons_per_row < 1:
        diagnostics.append(
            create_diagnostic(
                RULE_IDS.INCONSISTENT_CONFIGURATION,
                f"buttonsPerRow must be >= 1 (got {ctx.buttons_per_row})",
                "error",
            )
        )

    if ctx.auto_wrap_max_chars < 0:
        diagnostics.append(
            create_diagnostic(
                RULE_IDS.INCONSISTENT_CONFIGURATION,
                "autoWrapMaxChars cannot be negative",
                "error",
            )
        )

    for ref in ctx.normalized.flat:
        style = ref.button.get("style")
        if style is not None and style not in _ALLOWED_STYLES:
            diagnostics.append(
                create_diagnostic(
                    RULE_IDS.INCONSISTENT_CONFIGURATION,
                    f"Invalid button style: {style}",
                    "error",
                    loc(ref.row_index, ref.column_index, ref.flat_index, "style"),
                    "Allowed: primary, danger, success",
                )
            )

    return diagnostics


inconsistent_configuration_rule = ValidationRule(
    id=RULE_IDS.INCONSISTENT_CONFIGURATION,
    description="Detects invalid builder or button configuration",
    default_severity="warning",
    run=_run,
)
