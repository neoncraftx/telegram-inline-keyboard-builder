import { layoutButtons } from "../layout.js";
import type { InlineKeyboardButton } from "../types/buttons.js";
import type { KeyboardInput } from "./types.js";

export interface NormalizedButtonRef {
  button: InlineKeyboardButton;
  rowIndex: number;
  columnIndex: number;
  flatIndex: number;
}

export interface NormalizedKeyboard {
  rows: InlineKeyboardButton[][];
  flat: NormalizedButtonRef[];
  rawButtons: InlineKeyboardButton[];
  buttonsPerRow: number;
  autoWrapMaxChars: number;
  isEmpty: boolean;
}

/**
 * Normalizes keyboard state once for all rules (layout + indexed refs).
 */
export function normalizeKeyboard(input: KeyboardInput): NormalizedKeyboard {
  const { buttons, buttonsPerRow, autoWrapMaxChars } = input;
  const rows = layoutButtons(buttons, buttonsPerRow, autoWrapMaxChars);
  const flat: NormalizedButtonRef[] = [];
  let flatIndex = 0;

  for (let rowIndex = 0; rowIndex < rows.length; rowIndex++) {
    const row = rows[rowIndex];
    if (!row) continue;
    for (let columnIndex = 0; columnIndex < row.length; columnIndex++) {
      const button = row[columnIndex];
      if (!button) continue;
      flat.push({ button, rowIndex, columnIndex, flatIndex });
      flatIndex += 1;
    }
  }

  return {
    rows,
    flat,
    rawButtons: buttons,
    buttonsPerRow,
    autoWrapMaxChars,
    isEmpty: flat.length === 0,
  };
}
