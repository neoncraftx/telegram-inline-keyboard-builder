import type { InlineKeyboardButton } from "../../types/buttons.js";
import type { DiagnosticLocation } from "../types.js";

export function loc(
  rowIndex: number,
  columnIndex: number,
  flatIndex: number,
  field?: string,
): DiagnosticLocation {
  const location: DiagnosticLocation = { row: rowIndex, column: columnIndex, flatIndex };
  if (field !== undefined) {
    location.field = field;
  }
  return location;
}

export function callbackDataByteLength(data: string): number {
  return new TextEncoder().encode(data).length;
}

export function isValidHttpUrl(url: string): boolean {
  try {
    const parsed = new URL(url);
    return parsed.protocol === "http:" || parsed.protocol === "https:";
  } catch {
    return false;
  }
}

export function buttonKind(
  button: InlineKeyboardButton,
): "callback" | "url" | "pay" | "custom" | "invalid" {
  if (!button || typeof button !== "object") return "invalid";
  if ("pay" in button && button.pay === true) return "pay";
  if ("callback_data" in button && button.callback_data !== undefined) {
    return "callback";
  }
  if ("url" in button && button.url !== undefined) return "url";
  if ("text" in button) return "custom";
  return "invalid";
}

export function hasUnexpectedNull(value: unknown): boolean {
  return value === null || value === undefined;
}
