import assert from "node:assert/strict";
import { describe, it } from "node:test";
import {
  InlineKeyboardBuilder,
  ValidationError,
  RULE_IDS,
  createValidationEngine,
} from "../dist/index.js";

describe("Smart Validation & Warnings", () => {
  it("validate() returns ok for a valid keyboard", () => {
    const kb = new InlineKeyboardBuilder();
    kb.addCallbackButton("Yes", "ok:yes:1");
    const result = kb.validate();
    assert.equal(result.ok, true);
    assert.equal(result.errors.length, 0);
  });

  it("detects callback_data exceeding 64 bytes", () => {
    const kb = new InlineKeyboardBuilder();
    const long = "x".repeat(65);
    kb.addCustomButton({ text: "Go", callback_data: long });
    const result = kb.validate();
    assert.equal(result.ok, false);
    assert.ok(
      result.errors.some((d) => d.ruleId === RULE_IDS.CALLBACK_DATA_TOO_LONG),
    );
  });

  it("detects empty button text", () => {
    const kb = new InlineKeyboardBuilder();
    kb.addCustomButton({ text: "   ", callback_data: "a" });
    const result = kb.validate();
    assert.ok(
      result.diagnostics.some((d) => d.ruleId === RULE_IDS.EMPTY_BUTTON_TEXT),
    );
  });

  it("detects invalid URL", () => {
    const kb = new InlineKeyboardBuilder();
    kb.addUrlButton("Site", "not-a-url");
    const result = kb.validate();
    assert.ok(
      result.errors.some((d) => d.ruleId === RULE_IDS.INVALID_URL),
    );
  });

  it("warns on duplicate callback_data", () => {
    const kb = new InlineKeyboardBuilder();
    kb.addCallbackButton("A", "dup");
    kb.addCallbackButton("B", "dup");
    const result = kb.validate();
    assert.ok(
      result.warnings.some((d) => d.ruleId === RULE_IDS.DUPLICATE_CALLBACK_DATA),
    );
  });

  it("detects pay button outside invoice context", () => {
    const kb = new InlineKeyboardBuilder();
    kb.addPayButton("Pay");
    const result = kb.validate({ contextType: "message" });
    assert.ok(
      result.errors.some(
        (d) => d.ruleId === RULE_IDS.INCOMPATIBLE_BUTTON_CONTEXT,
      ),
    );
  });

  it("build({ validate: true }) throws in strict mode", () => {
    const kb = new InlineKeyboardBuilder();
    kb.addUrlButton("Bad", "ftp://bad");
    assert.throws(
      () => kb.build({ validate: true, validationMode: "strict" }),
      ValidationError,
    );
  });

  it("build({ validate: true }) does not throw in warn mode", () => {
    const kb = new InlineKeyboardBuilder();
    kb.addUrlButton("Bad", "ftp://bad");
    const markup = kb.build({ validate: true, validationMode: "warn" });
    assert.ok(markup.reply_markup.inline_keyboard.length > 0);
  });

  it("supports custom rules via registerRule", () => {
    const kb = new InlineKeyboardBuilder();
    kb.registerRule({
      id: "no-test-label",
      run() {
        return [
          {
            ruleId: "no-test-label",
            message: "Avoid TEST labels in production",
            severity: "warning",
          },
        ];
      },
    });
    kb.addCallbackButton("TEST", "x");
    const result = kb.validate();
    assert.ok(result.warnings.some((d) => d.ruleId === "no-test-label"));
  });

  it("supports plugins via use()", () => {
    const kb = new InlineKeyboardBuilder();
    kb.use({
      name: "demo-plugin",
      rules: [
        {
          id: "always-info",
          defaultSeverity: "info",
          run() {
            return [
              {
                ruleId: "always-info",
                message: "Plugin attached",
                severity: "info",
              },
            ];
          },
        },
      ],
    });
    const result = kb.validate();
    assert.ok(result.diagnostics.some((d) => d.ruleId === "always-info"));
  });

  it("setRules can disable a rule", () => {
    const kb = new InlineKeyboardBuilder();
    kb.addUrlButton("Bad", "not-valid");
    kb.setRules({ disabled: [RULE_IDS.INVALID_URL] });
    const result = kb.validate();
    assert.ok(
      !result.errors.some((d) => d.ruleId === RULE_IDS.INVALID_URL),
    );
  });

  it("detects more than Telegram max buttons in one row", () => {
    const kb = new InlineKeyboardBuilder(10);
    for (let i = 0; i < 9; i++) {
      kb.addCallbackButton(`B${i}`, `btn:${i}`);
    }
    const result = kb.validate();
    assert.ok(
      result.errors.some(
        (d) => d.ruleId === RULE_IDS.TOO_MANY_BUTTONS_PER_ROW,
      ),
    );
  });

  it("warns on consecutive newRow markers", () => {
    const kb = new InlineKeyboardBuilder();
    kb.newRow();
    kb.newRow();
    kb.addCallbackButton("Only", "x");
    const result = kb.validate();
    assert.ok(
      result.warnings.some((d) => d.ruleId === RULE_IDS.EMPTY_ROW),
    );
  });

  it("standalone ValidationEngine works without builder", () => {
    const engine = createValidationEngine();
    const result = engine.validate({
      buttons: [{ text: "X", callback_data: "a" }],
      buttonsPerRow: 2,
      autoWrapMaxChars: 0,
    });
    assert.equal(result.ok, true);
  });
});
