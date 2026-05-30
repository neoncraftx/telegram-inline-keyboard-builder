from __future__ import annotations

from .context.rule_registry import RuleRegistry
from .normalization import normalize_keyboard
from .plugins.plugin_manager import PluginManager
from .rules.builtin import builtin_rules
from .types import (
    Diagnostic,
    DiagnosticSeverity,
    KeyboardInput,
    RuleContext,
    RulesConfig,
    ValidateOptions,
    ValidationContextType,
    ValidationMode,
    ValidationPlugin,
    ValidationResult,
    ValidationRule,
)


class ValidationEngine:
    def __init__(self) -> None:
        self._registry = RuleRegistry()
        self._plugins = PluginManager(self._registry)
        self._default_mode: ValidationMode = "warn"
        self._context_type: ValidationContextType = "default"
        for rule in builtin_rules:
            self._registry.register_rule(rule)

    def set_default_mode(self, mode: ValidationMode) -> None:
        self._default_mode = mode

    def get_default_mode(self) -> ValidationMode:
        return self._default_mode

    def set_context_type(self, context_type: ValidationContextType) -> None:
        self._context_type = context_type

    def register_rule(self, rule: ValidationRule) -> None:
        self._registry.register_rule(rule)

    def use(self, plugin: ValidationPlugin) -> None:
        self._plugins.use(plugin)

    def set_rules(self, config: RulesConfig) -> None:
        self._registry.apply_config(config)

    def set_rule_enabled(self, rule_id: str, enabled: bool) -> None:
        self._registry.set_rule_enabled(rule_id, enabled)

    def set_rule_severity(self, rule_id: str, severity: DiagnosticSeverity) -> None:
        self._registry.set_rule_severity(rule_id, severity)

    def validate(
        self,
        input_data: KeyboardInput,
        options: ValidateOptions | None = None,
    ) -> ValidationResult:
        opts = options or {}
        mode: ValidationMode = opts.get("mode", self._default_mode)  # type: ignore[assignment]
        context_type: ValidationContextType = opts.get(  # type: ignore[assignment]
            "context_type", self._context_type
        )
        normalized = normalize_keyboard(input_data)
        rule_ctx = RuleContext(
            normalized=normalized,
            context_type=context_type,
            buttons_per_row=input_data["buttons_per_row"],
            auto_wrap_max_chars=input_data["auto_wrap_max_chars"],
        )

        diagnostics: list[Diagnostic] = []

        for rule in self._registry.get_active_rules():
            raw = rule.run(rule_ctx)
            default_severity = rule.default_severity or "warning"
            for diagnostic in raw:
                diag_severity = diagnostic.get("severity", default_severity)
                severity = self._registry.resolve_severity(
                    rule.id,
                    diag_severity,  # type: ignore[arg-type]
                )
                merged: Diagnostic = {**diagnostic, "severity": severity}
                diagnostics.append(merged)

        errors = [d for d in diagnostics if d["severity"] == "error"]
        warnings = [d for d in diagnostics if d["severity"] == "warning"]
        ok = len(errors) == 0

        return {
            "ok": ok,
            "diagnostics": diagnostics,
            "errors": errors,
            "warnings": warnings,
            "mode": mode,
        }


def create_validation_engine() -> ValidationEngine:
    return ValidationEngine()
