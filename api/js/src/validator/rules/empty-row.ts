import { createDiagnostic } from "../diagnostics.js";
import type { ValidationRule } from "../types.js";
import { RULE_IDS } from "./constants.js";

export const emptyRowRule: ValidationRule = {
  id: RULE_IDS.EMPTY_ROW,
  description: "Detects rows without buttons after layout",
  defaultSeverity: "warning",
  run(ctx) {
    const diagnostics = [];

    for (let i = 0; i < ctx.normalized.rows.length; i++) {
      const row = ctx.normalized.rows[i];
      if (row && row.length === 0) {
        diagnostics.push(
          createDiagnostic(
            RULE_IDS.EMPTY_ROW,
            `Row ${i + 1} has no buttons`,
            "warning",
            { row: i },
          ),
        );
      }
    }

    let pendingBreak = false;
    for (const raw of ctx.normalized.rawButtons) {
      if (raw.__newRow) {
        if (pendingBreak) {
          diagnostics.push(
            createDiagnostic(
              RULE_IDS.EMPTY_ROW,
              "Consecutive newRow() markers can produce empty rows",
              "warning",
            ),
          );
        }
        pendingBreak = true;
        continue;
      }
      pendingBreak = false;
    }

    return diagnostics;
  },
};
