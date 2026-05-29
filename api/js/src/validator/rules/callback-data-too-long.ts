import { createDiagnostic } from "../diagnostics.js";
import type { ValidationRule } from "../types.js";
import { RULE_IDS, TELEGRAM_CALLBACK_DATA_MAX_BYTES } from "./constants.js";
import { callbackDataByteLength, loc } from "./helpers.js";

export const callbackDataTooLongRule: ValidationRule = {
  id: RULE_IDS.CALLBACK_DATA_TOO_LONG,
  description: "callback_data must not exceed 64 UTF-8 bytes",
  defaultSeverity: "error",
  run(ctx) {
    const diagnostics = [];
    for (const ref of ctx.normalized.flat) {
      const { button, rowIndex, columnIndex, flatIndex } = ref;
      if (!("callback_data" in button) || typeof button.callback_data !== "string") {
        continue;
      }
      const bytes = callbackDataByteLength(button.callback_data);
      if (bytes > TELEGRAM_CALLBACK_DATA_MAX_BYTES) {
        diagnostics.push(
          createDiagnostic(
            RULE_IDS.CALLBACK_DATA_TOO_LONG,
            `callback_data is ${bytes} bytes (max ${TELEGRAM_CALLBACK_DATA_MAX_BYTES})`,
            "error",
            loc(rowIndex, columnIndex, flatIndex, "callback_data"),
            "Shorten scope/action/id or compress payload encoding",
          ),
        );
      }
    }
    return diagnostics;
  },
};
