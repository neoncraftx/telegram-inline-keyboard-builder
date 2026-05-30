from __future__ import annotations

from ..diagnostics import create_diagnostic
from ..types import Diagnostic, RuleContext, ValidationRule
from .constants import RULE_IDS
from .helpers import is_valid_http_url, loc


def _run(ctx: RuleContext) -> list[Diagnostic]:
    diagnostics: list[Diagnostic] = []
    for ref in ctx.normalized.flat:
        button = ref.button
        if "url" not in button or not isinstance(button.get("url"), str):
            continue
        url = button["url"]
        if not is_valid_http_url(url):
            diagnostics.append(
                create_diagnostic(
                    RULE_IDS.INVALID_URL,
                    f"Invalid URL: {url}",
                    "error",
                    loc(ref.row_index, ref.column_index, ref.flat_index, "url"),
                    "Use an absolute http:// or https:// URL",
                )
            )
    return diagnostics


invalid_url_rule = ValidationRule(
    id=RULE_IDS.INVALID_URL,
    description="URL buttons must use a valid http(s) URL",
    default_severity="error",
    run=_run,
)
