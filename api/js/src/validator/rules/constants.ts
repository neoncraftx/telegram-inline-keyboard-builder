export const RULE_IDS = {
  CALLBACK_DATA_TOO_LONG: "callback-data-too-long",
  EMPTY_BUTTON_TEXT: "empty-button-text",
  INVALID_URL: "invalid-url",
  EMPTY_ROW: "empty-row",
  TOO_MANY_BUTTONS_PER_ROW: "too-many-buttons-per-row",
  INCOMPATIBLE_BUTTON_CONTEXT: "incompatible-button-context",
  INCONSISTENT_CONFIGURATION: "inconsistent-configuration",
  DUPLICATE_CALLBACK_DATA: "duplicate-callback-data",
  UNEXPECTED_NULL_UNDEFINED: "unexpected-null-undefined",
  INVALID_KEYBOARD_STRUCTURE: "invalid-keyboard-structure",
} as const;

export const TELEGRAM_CALLBACK_DATA_MAX_BYTES = 64;
export const TELEGRAM_MAX_BUTTONS_PER_ROW = 8;
