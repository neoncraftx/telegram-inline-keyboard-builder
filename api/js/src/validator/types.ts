import type { InlineKeyboardButton } from "../types/buttons.js";
import type { NormalizedKeyboard } from "./normalization.js";

export type ValidationMode = "strict" | "warn" | "silent";

export type DiagnosticSeverity = "error" | "warning" | "info";

export type ValidationContextType =
  | "default"
  | "message"
  | "invoice"
  | "edit";

export interface DiagnosticLocation {
  row?: number;
  column?: number;
  flatIndex?: number;
  field?: string;
}

export interface Diagnostic {
  ruleId: string;
  message: string;
  severity: DiagnosticSeverity;
  location?: DiagnosticLocation;
  hint?: string;
}

export interface ValidationRule {
  id: string;
  description?: string;
  defaultSeverity?: DiagnosticSeverity;
  enabled?: boolean;
  run(ctx: RuleContext): Diagnostic[];
}

export interface RuleContext {
  normalized: NormalizedKeyboard;
  contextType: ValidationContextType;
  buttonsPerRow: number;
  autoWrapMaxChars: number;
}

export interface RuleSeverityOverride {
  ruleId: string;
  severity: DiagnosticSeverity;
}

export interface RulesConfig {
  enabled?: string[];
  disabled?: string[];
  severity?: RuleSeverityOverride[];
}

export interface ValidationPlugin {
  name: string;
  rules?: ValidationRule[];
  setup?: (registry: PluginSetupRegistry) => void;
}

export interface PluginSetupRegistry {
  registerRule(rule: ValidationRule): void;
  setRuleEnabled(ruleId: string, enabled: boolean): void;
  setRuleSeverity(ruleId: string, severity: DiagnosticSeverity): void;
}

export interface ValidationResult {
  ok: boolean;
  diagnostics: Diagnostic[];
  errors: Diagnostic[];
  warnings: Diagnostic[];
  mode: ValidationMode;
}

export interface BuildOptions {
  validate?: boolean;
  validationMode?: ValidationMode;
}

export interface ValidateOptions {
  mode?: ValidationMode;
  contextType?: ValidationContextType;
}

/** @internal Layout snapshot passed into the engine. */
export interface KeyboardInput {
  buttons: InlineKeyboardButton[];
  buttonsPerRow: number;
  autoWrapMaxChars: number;
  contextType?: ValidationContextType;
}

export class ValidationError extends Error {
  readonly result: ValidationResult;

  constructor(result: ValidationResult) {
    const summary = result.errors.map((d) => d.message).join("; ");
    super(
      summary
        ? `Keyboard validation failed: ${summary}`
        : "Keyboard validation failed",
    );
    this.name = "ValidationError";
    this.result = result;
  }
}
