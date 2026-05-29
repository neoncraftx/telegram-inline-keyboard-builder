import { RuleRegistry } from "../context/rule-registry.js";
import type { ValidationPlugin } from "../types.js";

export class PluginManager {
  private readonly registry: RuleRegistry;
  private readonly loaded = new Set<string>();

  constructor(registry: RuleRegistry) {
    this.registry = registry;
  }

  use(plugin: ValidationPlugin): void {
    if (this.loaded.has(plugin.name)) {
      return;
    }
    if (plugin.rules) {
      for (const rule of plugin.rules) {
        this.registry.registerRule(rule);
      }
    }
    plugin.setup?.(this.registry);
    this.loaded.add(plugin.name);
  }
}
