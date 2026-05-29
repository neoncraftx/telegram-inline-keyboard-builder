import { createDiagnostic } from "../diagnostics.js";
import type { ValidationRule } from "../types.js";
import { RULE_IDS } from "./constants.js";
import { isValidHttpUrl, loc } from "./helpers.js";

export const invalidUrlRule: ValidationRule = {
  id: RULE_IDS.INVALID_URL,
  description: "URL buttons must use a valid http(s) URL",
  defaultSeverity: "error",
  run(ctx) {
    const diagnostics = [];
    for (const ref of ctx.normalized.flat) {
      const { button, rowIndex, columnIndex, flatIndex } = ref;
      if (!("url" in button) || typeof button.url !== "string") continue;
      if (!isValidHttpUrl(button.url)) {
        diagnostics.push(
          createDiagnostic(
            RULE_IDS.INVALID_URL,
            `Invalid URL: ${String(button.url)}`,
            "error",
            loc(rowIndex, columnIndex, flatIndex, "url"),
            "Use an absolute http:// or https:// URL",
          ),
        );
      }
    }
    return diagnostics;
  },
};
