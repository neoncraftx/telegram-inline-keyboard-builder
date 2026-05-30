from __future__ import annotations

from .types import Diagnostic, DiagnosticLocation, DiagnosticSeverity


def create_diagnostic(
    rule_id: str,
    message: str,
    severity: DiagnosticSeverity,
    location: DiagnosticLocation | None = None,
    hint: str | None = None,
) -> Diagnostic:
    diagnostic: Diagnostic = {
        "rule_id": rule_id,
        "message": message,
        "severity": severity,
    }
    if location is not None:
        diagnostic["location"] = location
    if hint is not None:
        diagnostic["hint"] = hint
    return diagnostic
