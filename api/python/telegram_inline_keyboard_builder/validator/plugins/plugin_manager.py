from __future__ import annotations

from ..context.rule_registry import RuleRegistry
from ..types import ValidationPlugin


class PluginManager:
    def __init__(self, registry: RuleRegistry) -> None:
        self._registry = registry
        self._loaded: set[str] = set()

    def use(self, plugin: ValidationPlugin) -> None:
        if plugin["name"] in self._loaded:
            return
        if "rules" in plugin:
            for rule in plugin["rules"]:
                self._registry.register_rule(rule)
        if "setup" in plugin:
            plugin["setup"](self._registry)
        self._loaded.add(plugin["name"])
