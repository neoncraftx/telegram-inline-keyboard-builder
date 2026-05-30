"""
Validation types for Smart Validation & Warnings.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Literal, Protocol, TypedDict

from typing_extensions import NotRequired, Required

from ..core.types.buttons import InlineKeyboardButton

ValidationMode = Literal["strict", "warn", "silent"]
DiagnosticSeverity = Literal["error", "warning", "info"]
ValidationContextType = Literal["default", "message", "invoice", "edit"]


class DiagnosticLocation(TypedDict, total=False):
    row: int
    column: int
    flat_index: int
    field: str


class Diagnostic(TypedDict, total=False):
    rule_id: Required[str]
    message: Required[str]
    severity: Required[DiagnosticSeverity]
    location: DiagnosticLocation
    hint: str


class RuleSeverityOverride(TypedDict):
    rule_id: str
    severity: DiagnosticSeverity


class RulesConfig(TypedDict, total=False):
    enabled: list[str]
    disabled: list[str]
    severity: list[RuleSeverityOverride]


class ValidateOptions(TypedDict, total=False):
    mode: ValidationMode
    context_type: ValidationContextType


class ValidationResult(TypedDict):
    ok: bool
    diagnostics: list[Diagnostic]
    errors: list[Diagnostic]
    warnings: list[Diagnostic]
    mode: ValidationMode


class KeyboardInput(TypedDict, total=False):
    buttons: Required[list[InlineKeyboardButton]]
    buttons_per_row: Required[int]
    auto_wrap_max_chars: Required[int]
    context_type: ValidationContextType


@dataclass
class NormalizedButtonRef:
    button: InlineKeyboardButton
    row_index: int
    column_index: int
    flat_index: int


@dataclass
class NormalizedKeyboard:
    rows: list[list[InlineKeyboardButton]]
    flat: list[NormalizedButtonRef]
    raw_buttons: list[InlineKeyboardButton]
    buttons_per_row: int
    auto_wrap_max_chars: int
    is_empty: bool


@dataclass
class RuleContext:
    normalized: NormalizedKeyboard
    context_type: ValidationContextType
    buttons_per_row: int
    auto_wrap_max_chars: int


@dataclass
class ValidationRule:
    id: str
    run: Callable[[RuleContext], list[Diagnostic]]
    description: str | None = None
    default_severity: DiagnosticSeverity = "warning"
    enabled: bool | None = None


class PluginSetupRegistry(Protocol):
    def register_rule(self, rule: ValidationRule) -> None: ...
    def set_rule_enabled(self, rule_id: str, enabled: bool) -> None: ...
    def set_rule_severity(
        self, rule_id: str, severity: DiagnosticSeverity
    ) -> None: ...


class ValidationPlugin(TypedDict, total=False):
    name: Required[str]
    rules: list[ValidationRule]
    setup: Callable[[PluginSetupRegistry], None]


class ValidationError(Exception):
    """Raised when build(validate=True, validation_mode='strict') finds errors."""

    def __init__(self, result: ValidationResult) -> None:
        summary = "; ".join(d["message"] for d in result["errors"])
        super().__init__(
            f"Keyboard validation failed: {summary}"
            if summary
            else "Keyboard validation failed"
        )
        self.result = result
        self.name = "ValidationError"
