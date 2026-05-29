import { createDiagnostic } from "../diagnostics.js";
import type { ValidationRule } from "../types.js";
import { RULE_IDS } from "./constants.js";
import { loc } from "./helpers.js";

export const duplicateCallbackDataRule: ValidationRule = {
  id: RULE_IDS.DUPLICATE_CALLBACK_DATA,
  description: "Warns when the same callback_data is reused",
  defaultSeverity: "warning",
  run(ctx) {
    const diagnostics = [];
    const seen = new Map<string, { rowIndex: number; columnIndex: number; flatIndex: number }>();

    for (const ref of ctx.normalized.flat) {
      const { button, rowIndex, columnIndex, flatIndex } = ref;
      if (!("callback_data" in button) || typeof button.callback_data !== "string") {
        continue;
      }
      const data = button.callback_data;
      const previous = seen.get(data);
      if (previous) {
        diagnostics.push(
          createDiagnostic(
            RULE_IDS.DUPLICATE_CALLBACK_DATA,
            `Duplicate callback_data "${data}"`,
            "warning",
            loc(rowIndex, columnIndex, flatIndex, "callback_data"),
            `Also used at row ${previous.rowIndex + 1}, column ${previous.columnIndex + 1}`,
          ),
        );
      } else {
        seen.set(data, { rowIndex, columnIndex, flatIndex });
      }
    }

    return diagnostics;
  },
};
