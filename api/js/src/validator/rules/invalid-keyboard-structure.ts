import { createDiagnostic } from "../diagnostics.js";
import type { ValidationRule } from "../types.js";
import { RULE_IDS } from "./constants.js";
import { buttonKind, loc } from "./helpers.js";

export const invalidKeyboardStructureRule: ValidationRule = {
  id: RULE_IDS.INVALID_KEYBOARD_STRUCTURE,
  description: "Validates overall keyboard structural integrity",
  defaultSeverity: "error",
  run(ctx) {
    const diagnostics = [];

    if (!Array.isArray(ctx.normalized.rawButtons)) {
      diagnostics.push(
        createDiagnostic(
          RULE_IDS.INVALID_KEYBOARD_STRUCTURE,
          "buttons must be an array",
          "error",
        ),
      );
      return diagnostics;
    }

    if (ctx.normalized.isEmpty) {
      diagnostics.push(
        createDiagnostic(
          RULE_IDS.INVALID_KEYBOARD_STRUCTURE,
          "Keyboard has no buttons",
          "warning",
        ),
      );
    }

    let flatIndex = 0;
    for (const raw of ctx.normalized.rawButtons) {
      if (raw.__newRow) {
        continue;
      }
      if (typeof raw !== "object" || raw === null) {
        diagnostics.push(
          createDiagnostic(
            RULE_IDS.INVALID_KEYBOARD_STRUCTURE,
            "Invalid button entry (not an object)",
            "error",
            { flatIndex },
          ),
        );
        flatIndex += 1;
        continue;
      }

      const kind = buttonKind(raw);
      if (kind === "invalid") {
        diagnostics.push(
          createDiagnostic(
            RULE_IDS.INVALID_KEYBOARD_STRUCTURE,
            "Button has no recognized action (callback_data, url, or pay)",
            "error",
            { flatIndex },
          ),
        );
      }

      flatIndex += 1;
    }

    for (const ref of ctx.normalized.flat) {
      const { button, rowIndex, columnIndex, flatIndex: fi } = ref;
      if (typeof button !== "object") {
        diagnostics.push(
          createDiagnostic(
            RULE_IDS.INVALID_KEYBOARD_STRUCTURE,
            "Laid-out button is not an object",
            "error",
            loc(rowIndex, columnIndex, fi),
          ),
        );
      }
    }

    return diagnostics;
  },
};
