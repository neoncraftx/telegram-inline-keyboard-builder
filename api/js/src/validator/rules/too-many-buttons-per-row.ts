import { createDiagnostic } from "../diagnostics.js";
import type { ValidationRule } from "../types.js";
import { RULE_IDS, TELEGRAM_MAX_BUTTONS_PER_ROW } from "./constants.js";

export const tooManyButtonsPerRowRule: ValidationRule = {
  id: RULE_IDS.TOO_MANY_BUTTONS_PER_ROW,
  description: "Rows must not exceed configured or Telegram limits",
  defaultSeverity: "error",
  run(ctx) {
    const diagnostics = [];
    const configuredMax = Math.max(1, ctx.buttonsPerRow);

    for (let rowIndex = 0; rowIndex < ctx.normalized.rows.length; rowIndex++) {
      const row = ctx.normalized.rows[rowIndex];
      if (!row) continue;
      const count = row.length;

      if (count > configuredMax) {
        diagnostics.push(
          createDiagnostic(
            RULE_IDS.TOO_MANY_BUTTONS_PER_ROW,
            `Row ${rowIndex + 1} has ${count} buttons (configured max ${configuredMax})`,
            "error",
            { row: rowIndex },
            "Call newRow() or increase buttonsPerRow intentionally",
          ),
        );
      }

      if (count > TELEGRAM_MAX_BUTTONS_PER_ROW) {
        diagnostics.push(
          createDiagnostic(
            RULE_IDS.TOO_MANY_BUTTONS_PER_ROW,
            `Row ${rowIndex + 1} has ${count} buttons (Telegram max ${TELEGRAM_MAX_BUTTONS_PER_ROW})`,
            "error",
            { row: rowIndex },
          ),
        );
      }
    }

    return diagnostics;
  },
};
