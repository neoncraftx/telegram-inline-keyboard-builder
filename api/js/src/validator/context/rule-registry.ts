import type {
  DiagnosticSeverity,
  PluginSetupRegistry,
  RulesConfig,
  ValidationRule,
} from "../types.js";

export class RuleRegistry implements PluginSetupRegistry {
  private readonly rules = new Map<string, ValidationRule>();
  private readonly enabled = new Map<string, boolean>();
  private readonly severityOverrides = new Map<string, DiagnosticSeverity>();

  registerRule(rule: ValidationRule): void {
    this.rules.set(rule.id, rule);
    if (rule.enabled !== undefined && !this.enabled.has(rule.id)) {
      this.enabled.set(rule.id, rule.enabled);
    }
  }

  setRuleEnabled(ruleId: string, enabled: boolean): void {
    if (!this.rules.has(ruleId)) {
      throw new Error(`Unknown rule: ${ruleId}`);
    }
    this.enabled.set(ruleId, enabled);
  }

  setRuleSeverity(ruleId: string, severity: DiagnosticSeverity): void {
    if (!this.rules.has(ruleId)) {
      throw new Error(`Unknown rule: ${ruleId}`);
    }
    this.severityOverrides.set(ruleId, severity);
  }

  applyConfig(config: RulesConfig): void {
    if (config.enabled) {
      for (const id of config.enabled) {
        this.setRuleEnabled(id, true);
      }
    }
    if (config.disabled) {
      for (const id of config.disabled) {
        this.setRuleEnabled(id, false);
      }
    }
    if (config.severity) {
      for (const { ruleId, severity } of config.severity) {
        this.setRuleSeverity(ruleId, severity);
      }
    }
  }

  getActiveRules(): ValidationRule[] {
    return [...this.rules.values()].filter((rule) => this.isEnabled(rule.id));
  }

  isEnabled(ruleId: string): boolean {
    const explicit = this.enabled.get(ruleId);
    if (explicit !== undefined) return explicit;
    const rule = this.rules.get(ruleId);
    return rule?.enabled !== false;
  }

  resolveSeverity(
    ruleId: string,
    defaultSeverity: DiagnosticSeverity,
  ): DiagnosticSeverity {
    return this.severityOverrides.get(ruleId) ?? defaultSeverity;
  }

  hasRule(ruleId: string): boolean {
    return this.rules.has(ruleId);
  }
}
