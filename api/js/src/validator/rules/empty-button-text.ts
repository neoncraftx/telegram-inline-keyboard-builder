import { createDiagnostic } from "../diagnostics.js";
import type { ValidationRule } from "../types.js";
import { RULE_IDS } from "./constants.js";
import { loc } from "./helpers.js";

export const emptyButtonTextRule: ValidationRule = {
  id: RULE_IDS.EMPTY_BUTTON_TEXT,
  description: "Button text must be non-empty",
  defaultSeverity: "error",
  run(ctx) {
    const diagnostics = [];
    for (const ref of ctx.normalized.flat) {
      const { button, rowIndex, columnIndex, flatIndex } = ref;
      const text = button.text;
      if (typeof text !== "string" || text.trim().length === 0) {
        diagnostics.push(
          createDiagnostic(
            RULE_IDS.EMPTY_BUTTON_TEXT,
            "Button text is empty or whitespace-only",
            "error",
            loc(rowIndex, columnIndex, flatIndex, "text"),
          ),
        );
      }
    }
    return diagnostics;
  },
};
