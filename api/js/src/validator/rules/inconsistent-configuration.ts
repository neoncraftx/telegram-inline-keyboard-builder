import { createDiagnostic } from "../diagnostics.js";
import type { ValidationRule } from "../types.js";
import { RULE_IDS } from "./constants.js";
import { loc } from "./helpers.js";

const ALLOWED_STYLES = new Set(["primary", "danger", "success"]);

export const inconsistentConfigurationRule: ValidationRule = {
  id: RULE_IDS.INCONSISTENT_CONFIGURATION,
  description: "Detects invalid builder or button configuration",
  defaultSeverity: "warning",
  run(ctx) {
    const diagnostics = [];

    if (!Number.isFinite(ctx.buttonsPerRow) || ctx.buttonsPerRow < 1) {
      diagnostics.push(
        createDiagnostic(
          RULE_IDS.INCONSISTENT_CONFIGURATION,
          `buttonsPerRow must be >= 1 (got ${ctx.buttonsPerRow})`,
          "error",
        ),
      );
    }

    if (ctx.autoWrapMaxChars < 0) {
      diagnostics.push(
        createDiagnostic(
          RULE_IDS.INCONSISTENT_CONFIGURATION,
          "autoWrapMaxChars cannot be negative",
          "error",
        ),
      );
    }

    for (const ref of ctx.normalized.flat) {
      const { button, rowIndex, columnIndex, flatIndex } = ref;
      if (
        button.style !== undefined &&
        !ALLOWED_STYLES.has(button.style)
      ) {
        diagnostics.push(
          createDiagnostic(
            RULE_IDS.INCONSISTENT_CONFIGURATION,
            `Invalid button style: ${String(button.style)}`,
            "error",
            loc(rowIndex, columnIndex, flatIndex, "style"),
            "Allowed: primary, danger, success",
          ),
        );
      }
    }

    return diagnostics;
  },
};
