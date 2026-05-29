import { RuleRegistry } from "./context/rule-registry.js";
import { normalizeKeyboard } from "./normalization.js";
import { PluginManager } from "./plugins/plugin-manager.js";
import { builtinRules } from "./rules/builtin.js";
import type {
  Diagnostic,
  DiagnosticSeverity,
  KeyboardInput,
  RuleContext,
  RulesConfig,
  ValidateOptions,
  ValidationMode,
  ValidationPlugin,
  ValidationResult,
  ValidationRule,
} from "./types.js";

export class ValidationEngine {
  private readonly registry = new RuleRegistry();
  private readonly plugins = new PluginManager(this.registry);
  private defaultMode: ValidationMode = "warn";
  private contextType: RuleContext["contextType"] = "default";

  constructor() {
    for (const rule of builtinRules) {
      this.registry.registerRule(rule);
    }
  }

  setDefaultMode(mode: ValidationMode): void {
    this.defaultMode = mode;
  }

  getDefaultMode(): ValidationMode {
    return this.defaultMode;
  }

  setContextType(contextType: RuleContext["contextType"]): void {
    this.contextType = contextType;
  }

  registerRule(rule: ValidationRule): void {
    this.registry.registerRule(rule);
  }

  use(plugin: ValidationPlugin): void {
    this.plugins.use(plugin);
  }

  setRules(config: RulesConfig): void {
    this.registry.applyConfig(config);
  }

  setRuleEnabled(ruleId: string, enabled: boolean): void {
    this.registry.setRuleEnabled(ruleId, enabled);
  }

  setRuleSeverity(ruleId: string, severity: DiagnosticSeverity): void {
    this.registry.setRuleSeverity(ruleId, severity);
  }

  validate(
    input: KeyboardInput,
    options: ValidateOptions = {},
  ): ValidationResult {
    const mode = options.mode ?? this.defaultMode;
    const contextType = options.contextType ?? this.contextType;
    const normalized = normalizeKeyboard(input);
    const ruleCtx: RuleContext = {
      normalized,
      contextType,
      buttonsPerRow: input.buttonsPerRow,
      autoWrapMaxChars: input.autoWrapMaxChars,
    };

    const diagnostics: Diagnostic[] = [];

    for (const rule of this.registry.getActiveRules()) {
      const raw = rule.run(ruleCtx);
      const defaultSeverity = rule.defaultSeverity ?? "warning";
      for (const diagnostic of raw) {
        const severity = this.registry.resolveSeverity(
          rule.id,
          diagnostic.severity ?? defaultSeverity,
        );
        diagnostics.push({ ...diagnostic, severity });
      }
    }

    const errors = diagnostics.filter((d) => d.severity === "error");
    const warnings = diagnostics.filter((d) => d.severity === "warning");
    const ok = errors.length === 0;

    if (mode === "strict" && !ok) {
      // Caller throws ValidationError; engine stays side-effect free.
    }

    return {
      ok,
      diagnostics,
      errors,
      warnings,
      mode,
    };
  }

}

export function createValidationEngine(): ValidationEngine {
  return new ValidationEngine();
}
