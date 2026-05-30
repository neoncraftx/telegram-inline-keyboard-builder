# Smart Validation & Warnings

ESLint-style validation for Telegram inline keyboards. The engine normalizes layout once per run, then executes enabled rules against a shared context.

## Principles

- **Non-breaking by default** — `build()` without options behaves exactly as before.
- **Framework-agnostic** — no Telegraf/node-telegram-bot-api coupling.
- **Normalize once** — rows and button indices are computed a single time per `validate()` call.
- **Pluggable** — custom rules and plugins use the same pipeline as built-ins.
- **Three modes** — `strict` (throw on errors), `warn` (report only), `silent` (collect diagnostics without surfacing; same as manual validate).

## Public API

### `builder.validate(options?)`

Runs all enabled rules and returns a `ValidationResult`:

```ts
const result = builder.validate({ mode: "warn", contextType: "message" });
if (!result.ok) {
  console.warn(result.warnings, result.errors);
}
```

### `builder.build({ validate, validationMode })`

Optional validation before returning `reply_markup`:

```ts
// Throws ValidationError when errors exist
builder.build({ validate: true, validationMode: "strict" });

// Runs validation but still returns markup
builder.build({ validate: true, validationMode: "warn" });
```

### Plugins and rules

```ts
builder
  .registerRule(myRule)
  .use(myPlugin)
  .setRules({ disabled: ["duplicate-callback-data"] })
  .setRuleSeverity("empty-row", "error")
  .setValidationMode("strict")
  .setValidationContext("invoice");
```

### Standalone engine

```ts
import { createValidationEngine } from "telegram-inline-keyboard-builder";

const engine = createValidationEngine();
const result = engine.validate({
  buttons: [...],
  buttonsPerRow: 2,
  autoWrapMaxChars: 0,
});
```

## Validation modes

| Mode     | `validate()` | `build({ validate: true })`      |
|----------|--------------|----------------------------------|
| `strict` | Returns result; caller may throw | Throws `ValidationError` on errors |
| `warn`   | Returns diagnostics              | Never throws; returns markup       |
| `silent` | Same as warn (no console output) | Same as warn                       |

Default mode is `warn` (set via `setValidationMode`).

## Built-in rules

| Rule ID | Severity | Description |
|---------|----------|-------------|
| `callback-data-too-long` | error | `callback_data` > 64 UTF-8 bytes |
| `empty-button-text` | error | Missing or whitespace-only `text` |
| `invalid-url` | error | URL buttons must be valid `http(s)://` |
| `empty-row` | warning | Empty rows or consecutive `newRow()` |
| `too-many-buttons-per-row` | error | Exceeds `buttonsPerRow` or Telegram max (8) |
| `incompatible-button-context` | error | e.g. pay button outside `invoice` context |
| `inconsistent-configuration` | error/warning | Invalid `style`, `buttonsPerRow`, etc. |
| `duplicate-callback-data` | warning | Same `callback_data` used twice |
| `unexpected-null-undefined` | error | Nullish required fields |
| `invalid-keyboard-structure` | error/warning | Malformed buttons or empty keyboard |

## Python API

Same rule IDs and modes as JavaScript. Methods use **snake_case**:

```python
from telegram_inline_keyboard_builder import (
    InlineKeyboardBuilder,
    ValidationError,
    ValidationRule,
)

kb = InlineKeyboardBuilder()
kb.add_callback_button("OK", "menu:ok:1")
result = kb.validate(mode="warn", context_type="message")

kb.build(validate=True, validation_mode="strict")  # raises ValidationError

kb.set_validation_context("invoice")
kb.add_pay_button("Pay now")
kb.validate()
```

Standalone engine:

```python
from telegram_inline_keyboard_builder import create_validation_engine

engine = create_validation_engine()
result = engine.validate({
    "buttons": [{"text": "X", "callback_data": "a"}],
    "buttons_per_row": 2,
    "auto_wrap_max_chars": 0,
})
```

## Custom plugin example

```ts
import type { ValidationPlugin } from "telegram-inline-keyboard-builder";

const productionPlugin: ValidationPlugin = {
  name: "production-guards",
  setup(registry) {
    registry.registerRule({
      id: "reserved-callback-prefix",
      defaultSeverity: "error",
      run(ctx) {
        const diagnostics = [];
        for (const { button, rowIndex, columnIndex, flatIndex } of ctx.normalized.flat) {
          if (
            "callback_data" in button &&
            typeof button.callback_data === "string" &&
            button.callback_data.startsWith("debug:")
          ) {
            diagnostics.push({
              ruleId: "reserved-callback-prefix",
              message: "Remove debug: prefix before production",
              severity: "error",
              location: { row: rowIndex, column: columnIndex, flatIndex },
            });
          }
        }
        return diagnostics;
      },
    });
  },
};

builder.use(productionPlugin);
```

## Sample diagnostics

```json
{
  "ok": false,
  "mode": "warn",
  "errors": [
    {
      "ruleId": "callback-data-too-long",
      "message": "callback_data is 72 bytes (max 64)",
      "severity": "error",
      "location": { "row": 0, "column": 0, "flatIndex": 0, "field": "callback_data" },
      "hint": "Shorten scope/action/id or compress payload encoding"
    }
  ],
  "warnings": [
    {
      "ruleId": "duplicate-callback-data",
      "message": "Duplicate callback_data \"menu:home\"",
      "severity": "warning",
      "location": { "row": 1, "column": 0, "flatIndex": 2, "field": "callback_data" }
    }
  ]
}
```

## Context types

Set `contextType` when validating specialized keyboards:

- `default` — general inline keyboards
- `message` — standard message attachments
- `invoice` — required for `pay: true` buttons
- `edit` — edit-message reply markups

```ts
builder.setValidationContext("invoice");
builder.addPayButton("Pay now");
builder.validate();
```

## Custom plugin example (Python)

```python
from telegram_inline_keyboard_builder import InlineKeyboardBuilder, ValidationRule

def no_debug(ctx):
    out = []
    for ref in ctx.normalized.flat:
        data = ref.button.get("callback_data")
        if isinstance(data, str) and data.startswith("debug:"):
            out.append({
                "rule_id": "no-debug-prefix",
                "message": "Remove debug: prefix before production",
                "severity": "error",
                "location": {"row": ref.row_index, "column": ref.column_index},
            })
    return out

kb = InlineKeyboardBuilder()
kb.register_rule(ValidationRule(id="no-debug-prefix", run=no_debug))
```

## Roadmap

- JSON Schema export for diagnostics
- Auto-fix suggestions (codemods)
- CI reporters (GitHub Actions annotations)
