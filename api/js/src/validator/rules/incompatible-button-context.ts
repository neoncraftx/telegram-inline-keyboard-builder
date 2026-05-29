import { createDiagnostic } from "../diagnostics.js";
import type { ValidationRule } from "../types.js";
import { RULE_IDS } from "./constants.js";
import { buttonKind, loc } from "./helpers.js";

export const incompatibleButtonContextRule: ValidationRule = {
  id: RULE_IDS.INCOMPATIBLE_BUTTON_CONTEXT,
  description: "Buttons must match the declared validation context",
  defaultSeverity: "error",
  run(ctx) {
    const diagnostics = [];
    const contextType = ctx.contextType;

    for (const ref of ctx.normalized.flat) {
      const { button, rowIndex, columnIndex, flatIndex } = ref;
      const kind = buttonKind(button);

      if (kind === "pay" && contextType !== "invoice") {
        diagnostics.push(
          createDiagnostic(
            RULE_IDS.INCOMPATIBLE_BUTTON_CONTEXT,
            "Pay buttons are only valid in invoice keyboards",
            "error",
            loc(rowIndex, columnIndex, flatIndex),
            'Set validate({ contextType: "invoice" }) when building payment keyboards',
          ),
        );
      }

      const hasCallback =
        "callback_data" in button && button.callback_data !== undefined;
      const hasUrl = "url" in button && button.url !== undefined;
      const hasPay = "pay" in button && button.pay === true;

      const actionCount = [hasCallback, hasUrl, hasPay].filter(Boolean).length;
      if (actionCount > 1) {
        diagnostics.push(
          createDiagnostic(
            RULE_IDS.INCOMPATIBLE_BUTTON_CONTEXT,
            "Button defines multiple mutually exclusive actions",
            "error",
            loc(rowIndex, columnIndex, flatIndex),
          ),
        );
      }

      if (kind === "custom" && contextType === "invoice") {
        diagnostics.push(
          createDiagnostic(
            RULE_IDS.INCOMPATIBLE_BUTTON_CONTEXT,
            "Custom buttons without url/callback/pay are unusual in invoice context",
            "warning",
            loc(rowIndex, columnIndex, flatIndex),
          ),
        );
      }
    }

    return diagnostics;
  },
};
