from __future__ import annotations

from ..types import (
    DiagnosticSeverity,
    PluginSetupRegistry,
    RulesConfig,
    ValidationRule,
)


class RuleRegistry(PluginSetupRegistry):
    def __init__(self) -> None:
        self._rules: dict[str, ValidationRule] = {}
        self._enabled: dict[str, bool] = {}
        self._severity_overrides: dict[str, DiagnosticSeverity] = {}

    def register_rule(self, rule: ValidationRule) -> None:
        self._rules[rule.id] = rule
        if rule.enabled is not None and rule.id not in self._enabled:
            self._enabled[rule.id] = rule.enabled

    def set_rule_enabled(self, rule_id: str, enabled: bool) -> None:
        if rule_id not in self._rules:
            raise ValueError(f"Unknown rule: {rule_id}")
        self._enabled[rule_id] = enabled

    def set_rule_severity(self, rule_id: str, severity: DiagnosticSeverity) -> None:
        if rule_id not in self._rules:
            raise ValueError(f"Unknown rule: {rule_id}")
        self._severity_overrides[rule_id] = severity

    def apply_config(self, config: RulesConfig) -> None:
        if "enabled" in config:
            for rule_id in config["enabled"]:
                self.set_rule_enabled(rule_id, True)
        if "disabled" in config:
            for rule_id in config["disabled"]:
                self.set_rule_enabled(rule_id, False)
        if "severity" in config:
            for entry in config["severity"]:
                self.set_rule_severity(entry["rule_id"], entry["severity"])

    def get_active_rules(self) -> list[ValidationRule]:
        return [r for r in self._rules.values() if self.is_enabled(r.id)]

    def is_enabled(self, rule_id: str) -> bool:
        if rule_id in self._enabled:
            return self._enabled[rule_id]
        rule = self._rules.get(rule_id)
        return rule.enabled is not False if rule else False

    def resolve_severity(
        self, rule_id: str, default_severity: DiagnosticSeverity
    ) -> DiagnosticSeverity:
        return self._severity_overrides.get(rule_id, default_severity)

    def has_rule(self, rule_id: str) -> bool:
        return rule_id in self._rules
