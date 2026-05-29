import { callbackDataTooLongRule } from "./callback-data-too-long.js";
import { duplicateCallbackDataRule } from "./duplicate-callback-data.js";
import { emptyButtonTextRule } from "./empty-button-text.js";
import { emptyRowRule } from "./empty-row.js";
import { incompatibleButtonContextRule } from "./incompatible-button-context.js";
import { inconsistentConfigurationRule } from "./inconsistent-configuration.js";
import { invalidKeyboardStructureRule } from "./invalid-keyboard-structure.js";
import { invalidUrlRule } from "./invalid-url.js";
import { tooManyButtonsPerRowRule } from "./too-many-buttons-per-row.js";
import { unexpectedNullUndefinedRule } from "./unexpected-null-undefined.js";

export const builtinRules = [
  callbackDataTooLongRule,
  emptyButtonTextRule,
  invalidUrlRule,
  emptyRowRule,
  tooManyButtonsPerRowRule,
  incompatibleButtonContextRule,
  inconsistentConfigurationRule,
  duplicateCallbackDataRule,
  unexpectedNullUndefinedRule,
  invalidKeyboardStructureRule,
];

export { RULE_IDS } from "./constants.js";
