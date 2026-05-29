import type {
  Diagnostic,
  DiagnosticLocation,
  DiagnosticSeverity,
} from "./types.js";

export function createDiagnostic(
  ruleId: string,
  message: string,
  severity: DiagnosticSeverity,
  location?: DiagnosticLocation,
  hint?: string,
): Diagnostic {
  const diagnostic: Diagnostic = { ruleId, message, severity };
  if (location !== undefined) {
    diagnostic.location = location;
  }
  if (hint !== undefined) {
    diagnostic.hint = hint;
  }
  return diagnostic;
}
