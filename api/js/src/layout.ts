import type { InlineKeyboardButton } from "./types/buttons.js";

/**
 * Lays out a flat button list into rows using builder configuration.
 * Shared by the builder output and the validation normalizer.
 */
export function layoutButtons(
  buttons: InlineKeyboardButton[],
  buttonsPerRow: number,
  autoWrapMaxChars: number,
): InlineKeyboardButton[][] {
  const rows: InlineKeyboardButton[][] = [];
  let row: InlineKeyboardButton[] = [];
  let rowChars = 0;

  const pushRow = () => {
    if (row.length > 0) {
      rows.push([...row]);
      row = [];
      rowChars = 0;
    }
  };

  for (const b of buttons) {
    if (b.__newRow) {
      pushRow();
      continue;
    }
    const textLength = String(b.text || "").length;
    if (
      autoWrapMaxChars > 0 &&
      row.length > 0 &&
      rowChars + textLength > autoWrapMaxChars
    ) {
      pushRow();
    }
    if (row.length >= buttonsPerRow) {
      pushRow();
    }
    row.push(b);
    rowChars += textLength;
  }
  pushRow();
  return rows;
}
