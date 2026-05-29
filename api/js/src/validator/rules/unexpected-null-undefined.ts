import { createDiagnostic } from "../diagnostics.js";
import type { ValidationRule } from "../types.js";
import { RULE_IDS } from "./constants.js";
import { hasUnexpectedNull, loc } from "./helpers.js";

export const unexpectedNullUndefinedRule: ValidationRule = {
  id: RULE_IDS.UNEXPECTED_NULL_UNDEFINED,
  description: "Detects null or undefined in required button fields",
  defaultSeverity: "error",
  run(ctx) {
    const diagnostics = [];

    for (const ref of ctx.normalized.flat) {
      const { button, rowIndex, columnIndex, flatIndex } = ref;

      if (hasUnexpectedNull(button)) {
        diagnostics.push(
          createDiagnostic(
            RULE_IDS.UNEXPECTED_NULL_UNDEFINED,
            "Button entry is null or undefined",
            "error",
            loc(rowIndex, columnIndex, flatIndex),
          ),
        );
        continue;
      }

      if (hasUnexpectedNull(button.text)) {
        diagnostics.push(
          createDiagnostic(
            RULE_IDS.UNEXPECTED_NULL_UNDEFINED,
            "Button text is null or undefined",
            "error",
            loc(rowIndex, columnIndex, flatIndex, "text"),
          ),
        );
      }

      if ("callback_data" in button && hasUnexpectedNull(button.callback_data)) {
        diagnostics.push(
          createDiagnostic(
            RULE_IDS.UNEXPECTED_NULL_UNDEFINED,
            "callback_data is null or undefined",
            "error",
            loc(rowIndex, columnIndex, flatIndex, "callback_data"),
          ),
        );
      }

      if ("url" in button && hasUnexpectedNull(button.url)) {
        diagnostics.push(
          createDiagnostic(
            RULE_IDS.UNEXPECTED_NULL_UNDEFINED,
            "url is null or undefined",
            "error",
            loc(rowIndex, columnIndex, flatIndex, "url"),
          ),
        );
      }
    }

    return diagnostics;
  },
};
