![Logo](https://i.ibb.co/BKVnp8dZ/20260202-141042.png) [![npm version](https://img.shields.io/npm/v/telegram-inline-keyboard-builder?style=flat&logo=npm&logoColor=white&color=cb3837)](https://www.npmjs.com/package/telegram-inline-keyboard-builder) [![npm downloads](https://img.shields.io/npm/dw/telegram-inline-keyboard-builder?style=flat&logo=npm&logoColor=white&color=2CA5E0)](https://www.npmjs.com/package/telegram-inline-keyboard-builder) [![license](https://img.shields.io/npm/l/telegram-inline-keyboard-builder?style=flat&color=555555)](LICENSE) ![Telegram](https://img.shields.io/badge/Telegram-Inline%20Keyboard-2CA5E0?style=flat&logo=telegram&logoColor=white)

# Inline Keyboard Builder (v3.2.3)

Universal inline keyboard builder for Telegram Bots.

Produces **pure Telegram Bot API compliant JSON**, usable with **any library** (Telegraf, node-telegram-bot-api, Pyrogram, Aiogram, Puregram, Telebot…).

**New in 3.2.3:** [Smart Validation & Warnings](#version-323--smart-validation--warnings) — catch `callback_data` limits, invalid URLs, pay-button context errors, and more **before** sending to Telegram.

---

## Table of Contents

- [New in v3.2.3 — Smart Validation & Warnings](#version-323--smart-validation--warnings)
  - [Why use it](#why-use-smart-validation)
  - [Performance & design](#performance-and-design-optimizations)
  - [Validation modes](#validation-modes)
  - [Built-in rules](#built-in-rules)
  - [Public validation API](#validation-api-on-the-builder)
  - [Concrete examples](#concrete-validation-examples)
  - [Custom plugins](#custom-plugins-eslint-style)
  - [Migration from 3.1.x](#migration-to-323)
- [New in v3](#version-3-enriched-builder-and-stronger-typing)
  - [Key highlights](#key-highlights-of-the-update)
  - [addCallbackButtonFromParts()](#addcallbackbuttonfromparts)
  - [preview()](#preview)
  - [callbackDataParse()](#callbackdataparse)
  - [paginatedList()](#paginatedlist)
  - [v3 full example](#concrete-v3-example)
- [Premium button styles (v2)](#-new-update-)
- [Key Features](#-key-features---fluent--chainable-api---library-agnostic-no-adapters-no-dependencies-)
- [Installation](#installation)
- [Import](#importation)
- [Core Concept](#-core-concept)
- [Public API](#-public-api)
- [Usage — Telegraf](#usage-example-telegraf)
- [Usage — node-telegram-bot-api](#usage-example-node-telegram-bot-api)
- [Payment Buttons](#-payment-buttons)
- [Common Errors](#-common-errors)
- [Migration to V2](#migration-to-v2)
- [Support this project](#-support-this-project-crypto)
- [Contribution](#️-contribution)

---

## Version 3.2.3 — Smart Validation & Warnings

**v3.2.3** adds a native, **ESLint-style validation engine** for inline keyboards. It detects Telegram API mistakes **before** `build()` returns markup, surfaces **non-blocking warnings**, supports **custom rules via plugins**, and stays **100% framework-agnostic** (no Telegraf / node-telegram-bot-api coupling).

> Full reference: [`docs/validation.md`](../../docs/validation.md) · Live demo: [`test-demo/product-catalog-bot`](../../test-demo/product-catalog-bot)

### Why use Smart Validation?

| Problem without validation | What v3.2.3 gives you |
| -------------------------- | --------------------- |
| `callback_data` > 64 bytes → silent Telegram API error | `callback-data-too-long` with **row/column** location + hint |
| Pay button on a normal message → runtime failure | `incompatible-button-context` when `contextType` is not `invoice` |
| Duplicate `callback_data` → confusing handler behaviour | `duplicate-callback-data` warning before deploy |
| Invalid URL (`ftp://…`, typo) | `invalid-url` at build time |
| Empty rows after chained `newRow()` | `empty-row` warning |
| Team-specific conventions (no `debug:` prefix) | `registerRule()` / `use(plugin)` |

**Main advantages:**

1. **Shift-left quality** — catch keyboard bugs in development, unit tests, or CI, not in production Telegram errors.
2. **Structured diagnostics** — each issue includes `ruleId`, `severity`, `message`, optional `location` (`row`, `column`, `flatIndex`), and `hint`.
3. **Three modes** — `strict` (block invalid builds), `warn` (report + still build), `silent` (collect only; for programmatic checks).
4. **Non-breaking by default** — `build()` without options behaves exactly like v3.1.x.
5. **Extensible** — enable/disable rules, override severities, ship team plugins like ESLint configs.
6. **Typed end-to-end** — `ValidationResult`, `Diagnostic`, `ValidationRule`, `ValidationPlugin`, `ValidationError` exported from the package.

### Performance and design optimizations

The engine is designed to stay **lightweight** for a library (no Zod, no AJV, no extra runtime dependencies):

| Optimization | Detail |
| -------------- | ------ |
| **Normalize once** | Each `validate()` call runs `normalizeKeyboard()` a single time; all rules share the same `RuleContext`. |
| **Shared layout engine** | `layout.ts` is used by both `InlineKeyboardBuilder._layoutButtons()` and the validator — layout logic is not duplicated. |
| **Active rules only** | `RuleRegistry.getActiveRules()` skips disabled rules; no work for turned-off checks. |
| **O(n) rules** | Each built-in rule iterates the flat button list once; suitable for large paginated keyboards. |
| **Zero new dependencies** | Validation ships inside the existing package footprint (~35 KB ESM/CJS build). |
| **Lazy opt-in** | No validation cost until you call `validate()` or `build({ validate: true })`. |

### Validation modes

| Mode | `validate()` | `build({ validate: true })` |
| ---- | -------------- | --------------------------- |
| `strict` | Returns `ValidationResult`; you may throw manually | Throws `ValidationError` if any **error**-severity diagnostic exists |
| `warn` | Returns diagnostics; `ok === false` if errors exist | Never throws; always returns markup |
| `silent` | Same as `warn` (no console side effects) | Same as `warn` |

Default mode: **`warn`** (set once with `.setValidationMode("strict")` for production pipelines).

```ts
builder.setValidationMode("strict"); // default for subsequent build({ validate: true })
```

### Built-in rules

| Rule ID | Default severity | Detects |
| ------- | ---------------- | ------- |
| `callback-data-too-long` | error | `callback_data` > 64 UTF-8 bytes |
| `empty-button-text` | error | Missing or whitespace-only `text` |
| `invalid-url` | error | URL buttons without valid `http://` or `https://` |
| `empty-row` | warning | Empty rows / consecutive `newRow()` |
| `too-many-buttons-per-row` | error | More than 8 buttons per row (Telegram limit) |
| `incompatible-button-context` | error | Pay button outside `invoice`, multiple actions on one button |
| `inconsistent-configuration` | error / warning | Invalid `style`, `buttonsPerRow`, etc. |
| `duplicate-callback-data` | warning | Same `callback_data` used twice |
| `unexpected-null-undefined` | error | Nullish required fields on buttons |
| `invalid-keyboard-structure` | error / warning | Malformed buttons or empty keyboard |

Constants exported for tooling: `RULE_IDS`, `TELEGRAM_CALLBACK_DATA_MAX_BYTES`, `TELEGRAM_MAX_BUTTONS_PER_ROW`.

### Validation API on the builder

```ts
// Manual check (tests, handlers, CI)
const result = builder.validate({ mode: "warn", contextType: "message" });
console.log(result.ok, result.errors, result.warnings);

// Validate then build — strict blocks invalid markup
const markup = builder.build({ validate: true, validationMode: "strict" });

// Plugins & rule configuration (ESLint-style)
builder
  .registerRule(myRule)
  .use(myPlugin)
  .setRules({ disabled: ["duplicate-callback-data"] })
  .setRuleSeverity("empty-row", "error")
  .setRuleEnabled("invalid-url", true)
  .setValidationContext("invoice");

// Standalone engine (no builder instance)
import { createValidationEngine } from "telegram-inline-keyboard-builder";

const engine = createValidationEngine();
engine.validate({ buttons: [...], buttonsPerRow: 2, autoWrapMaxChars: 0 });
```

**New chainable methods (v3.2.3):**

```ts
.validate(options?)
.registerRule(rule)
.use(plugin)
.setRules(config)
.setRuleEnabled(ruleId, enabled)
.setRuleSeverity(ruleId, severity)
.setValidationMode(mode)
.setValidationContext("default" | "message" | "invoice" | "edit")
```

**Updated `build()` signature:**

```ts
.build() // unchanged — no validation
.build({ validate: true, validationMode: "strict" | "warn" | "silent" })
```

### Concrete validation examples

#### Production — strict mode before sending (Telegraf)

```ts
import { InlineKeyboardBuilder, ValidationError } from "telegram-inline-keyboard-builder";

function buildMenuKeyboard() {
  const kb = new InlineKeyboardBuilder(2);
  kb.setValidationMode("strict");
  kb.setValidationContext("message");

  kb.addCallbackButtonFromParts("menu", "home", 1, "🏠 Home");
  kb.addCallbackButtonFromParts("menu", "settings", 1, "⚙️ Settings");

  try {
    return kb.build({ validate: true, validationMode: "strict" });
  } catch (e) {
    if (e instanceof ValidationError) {
      console.error(e.result.errors);
    }
    throw e;
  }
}

bot.start((ctx) => ctx.reply("Menu", buildMenuKeyboard()));
```

#### Development — warn mode + log diagnostics

```ts
const kb = new InlineKeyboardBuilder();
kb.addCallbackButton("OK", "ok");
kb.addCallbackButton("Duplicate", "ok"); // triggers duplicate-callback-data

const result = kb.validate({ mode: "warn" });
if (!result.ok) {
  for (const d of result.diagnostics) {
    console.warn(
      `[${d.severity}] ${d.ruleId} @ row ${d.location?.row}: ${d.message}`,
    );
  }
}

// Still safe to inspect markup in dev
const markup = kb.build({ validate: true, validationMode: "warn" });
```

#### Invoice keyboard — pay button context

```ts
const invoiceKb = new InlineKeyboardBuilder(1);
invoiceKb.setValidationContext("invoice");
invoiceKb.addPayButton("Pay 100 ⭐");

// ✅ valid — pay buttons allowed in invoice context
invoiceKb.validate({ contextType: "invoice" });

const messageKb = new InlineKeyboardBuilder(1);
messageKb.addPayButton("Pay now");

// ❌ incompatible-button-context — pay on normal message
messageKb.validate({ contextType: "message" });
```

#### Paginated list + validation (real-world catalog)

```ts
const kb = new InlineKeyboardBuilder(1);
kb.setValidationMode("strict");

kb.paginatedList({
  items: products,
  page: 2,
  perPage: 5,
  render: (p) => ({
    text: `🛍 ${p.name}`,
    callback_data: `product:view:${p.id}`, // keep under 64 bytes!
  }),
  pagination: {
    callback: (p) => `catalog:page:${p}`,
    hideIfSinglePage: true,
  },
});

// Catches long callback_data from render(), empty rows, row overflow
const markup = kb.build({ validate: true, validationMode: "strict" });
await ctx.editMessageReplyMarkup(markup.reply_markup);
```

#### Unit test — assert rule IDs

```ts
import { describe, it } from "node:test";
import assert from "node:assert/strict";
import { InlineKeyboardBuilder, RULE_IDS } from "telegram-inline-keyboard-builder";

it("rejects callback_data over 64 bytes", () => {
  const kb = new InlineKeyboardBuilder();
  kb.addCustomButton({ text: "Go", callback_data: "x".repeat(65) });
  const result = kb.validate();
  assert.equal(result.ok, false);
  assert.ok(
    result.errors.some((d) => d.ruleId === RULE_IDS.CALLBACK_DATA_TOO_LONG),
  );
});
```

#### Sample diagnostic output

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
      "location": { "row": 1, "column": 0, "flatIndex": 2 }
    }
  ]
}
```

### Custom plugins (ESLint-style)

```ts
import type { ValidationPlugin } from "telegram-inline-keyboard-builder";

const productionPlugin: ValidationPlugin = {
  name: "production-guards",
  setup(registry) {
    registry.registerRule({
      id: "no-debug-callback",
      defaultSeverity: "error",
      run(ctx) {
        const diagnostics = [];
        for (const { button, rowIndex, columnIndex, flatIndex } of ctx.normalized.flat) {
          if (
            "callback_data" in button &&
            button.callback_data?.startsWith("debug:")
          ) {
            diagnostics.push({
              ruleId: "no-debug-callback",
              message: "Remove debug: prefix before production",
              severity: "error",
              location: { row: rowIndex, column: columnIndex, flatIndex },
            });
          }
        }
        return diagnostics;
      },
    });
    registry.setRuleSeverity("duplicate-callback-data", "error");
  },
};

const kb = new InlineKeyboardBuilder();
kb.use(productionPlugin);
kb.setRules({ disabled: ["empty-row"] });
```

Per-rule severity override (like ESLint rule levels):

```ts
kb.setRules({
  severity: [
    { ruleId: "duplicate-callback-data", severity: "error" },
    { ruleId: "empty-row", severity: "warning" },
  ],
});
```

### Migration to 3.2.3

- **Fully backward compatible** — existing `build()` calls work unchanged.
- **Opt in** when ready: add `build({ validate: true })` or `validate()` in tests.
- **Recommended rollout:**
  1. `npm install telegram-inline-keyboard-builder@3.2.3`
  2. Add `validate()` in unit tests for critical keyboards
  3. Enable `build({ validate: true, validationMode: "warn" })` in staging
  4. Switch production to `strict` for invoice and catalog keyboards
  5. Add team `use(plugin)` for project-specific rules

> **V3.1 → V3.2.3 checklist**
>
> - [ ] Update: `npm install telegram-inline-keyboard-builder@3.2.3`
> - [ ] Call `.setValidationContext("invoice")` before keyboards with `.addPayButton()`
> - [ ] Use `build({ validate: true, validationMode: "strict" })` on production paths
> - [ ] Add custom plugins for team conventions (prefixes, max callback length policies)
> - [ ] See demo bot: `test-demo/product-catalog-bot` (`/validation` command)

---

## Version 3: Enriched builder and stronger typing

La release v3 du builder met l'accent sur la stabilité, le typage TypeScript et des helpers plus pratiques.

### Key highlights of the update

- Migration et typage TypeScript
  - signatures fortement typées pour `addCallbackButton`, `addUrlButton`, `addCallbackButtonFromParts`, `callbackDataParse`, `preview` et `addButtons`
  - meilleure autocomplétion dans l'éditeur et détection d'erreurs plus rapide
- Nouvelles fonctionnalités
  - `addCallbackButtonFromParts(scope, action, id, text, options, separator)` construit automatiquement le `callback_data`
  - `preview()` affiche la structure de chaque ligne de bouton
  - `callbackDataParse(data, separator)` décode la chaîne de callback en `{ scope, action, id }`
  - `paginatedList(options)` turns any array into an interactive paginated inline keyboard
- Corrections importantes
  - cohérence des objets `InlineKeyboardButton`
  - gestion plus fiable des nouvelles lignes et de l'auto-wrap
  - prévention des erreurs de type dans la prévisualisation

---

### `addCallbackButtonFromParts()`

Automatically builds a structured `callback_data` string from multiple parts.  
Eliminates manual string concatenation errors.

```ts
builder.addCallbackButtonFromParts(
  scope,      // string  — functional domain (e.g. "user", "product")
  action,     // string  — action to perform  (e.g. "like", "delete")
  id,         // string | number — resource identifier
  text,       // string  — label displayed on the button
  options?,   // object  — style options { style: "success" | "danger" | "primary" }
  separator?  // string  — separator between parts (default: ":")
)
```

---

### `preview()`

Prints the keyboard structure row by row in the console.  
Useful during development to verify layout before sending to Telegram.

```ts
builder.preview();
// Row 1: [Button A](callback:...) | [Button B](callback:...)
// Row 2: [Link](https://...)
```

---

### `callbackDataParse()`

Decodes a `callback_data` string into a structured `{ scope, action, id }` object.  
Useful for validating received data inside a handler or for unit tests.

```ts
builder.callbackDataParse(
  data,       // string — the callback_data string to decode
  separator?  // string — separator used at encoding time (default: ":")
)
// → { scope: string, action: string, id: string }
```

---

### `paginatedList()`

Transforms a full array into a paginated inline keyboard with built-in navigation.  
Each item is rendered as a button on its own row, followed by a navigation bar.

```ts
builder.paginatedList({
  items, // T[]                     — complete list of elements
  page, // number                  — current page (starts at 1)
  perPage, // number                  — number of items per page
  render, // (item: T) => Button     — function that maps an item to a button
  pagination, // PaginationConfig        — navigation configuration
});
```

#### PaginationConfig

| Parameter          | Type                       | Default    | Description                                                  |
| ------------------ | -------------------------- | ---------- | ------------------------------------------------------------ |
| `callback`         | `(page: number) => string` | required   | Generates the `callback_data` for a given page number.       |
| `labels.previous`  | `string`                   | `"⬅️"`     | Previous page button label.                                  |
| `labels.next`      | `string`                   | `"➡️"`     | Next page button label.                                      |
| `labels.first`     | `string`                   | `"⏮"`     | First page button label (only when `showEdgeButtons: true`). |
| `labels.last`      | `string`                   | `"⏭"`     | Last page button label (only when `showEdgeButtons: true`).  |
| `showEdgeButtons`  | `boolean`                  | `false`    | Adds ⏮ / ⏭ buttons to jump to the first / last page.       |
| `hideIfSinglePage` | `boolean`                  | `false`    | Hides the navigation bar when all items fit on one page.     |
| `counterCallback`  | `string`                   | `"ignore"` | `callback_data` for the central counter button `2/5`.        |

#### Key behaviors

- **Empty list** — returns `this` immediately without rendering anything.
- **Out-of-range page** — automatically clamped with `min(page, totalPages)`.
- **Edge navigation** — on the first page, the previous button shows `·⬅️·` with callback `"ignore"`. Same for next on the last page.
- **Validation** — throws an explicit error if `callback` is not a function or if `items` is not an array.

#### Example — product list

```js
bot.action(/^products_page_(\d+)$/, async (ctx) => {
  const page = parseInt(ctx.match[1]) || 1;
  const products = await db.getProducts();

  const keyboard = new InlineKeyboardBuilder().paginatedList({
    items: products,
    page,
    perPage: 5,
    render: (product) => ({
      text: `🛍 ${product.name} — ${product.price}€`,
      callback_data: `product_view_${product.id}`,
    }),
    pagination: {
      callback: (p) => `products_page_${p}`,
      hideIfSinglePage: true,
    },
  });

  await ctx.editMessageReplyMarkup(keyboard.build());
});
```

```
// Render (page 2/9)
[ 🛍 Shoes Nike — 89€    ]
[ 🛍 Adidas Bag — 45€    ]
[ 🛍 Casio Watch — 120€  ]
[ 🛍 Ray-Ban — 99€       ]
[ 🛍 NY Cap — 25€        ]
[  ⬅️  ][  2/9  ][  ➡️  ]
```

#### Example — user list with edge buttons

For long lists (100+ items), `showEdgeButtons` lets users jump directly to the first or last page.

```js
bot.action(/^users_page_(\d+)$/, async (ctx) => {
  const page = parseInt(ctx.match[1]) || 1;
  const users = await db.getAllUsers();

  const keyboard = new InlineKeyboardBuilder().paginatedList({
    items: users,
    page,
    perPage: 8,
    render: (user) => ({
      text: `👤 ${user.username} (${user.role})`,
      callback_data: `user_info_${user.id}`,
    }),
    pagination: {
      callback: (p) => `users_page_${p}`,
      showEdgeButtons: true,
      labels: { previous: "◀️", next: "▶️", first: "⏮", last: "⏭" },
    },
  });

  await ctx.editMessageText("👥 Users", { reply_markup: keyboard.build() });
});
```

```
// Render (page 1/13) — ⏮ and ◀️ are dimmed on the first page
[ 👤 alice (admin) ]
[ 👤 bob (user)    ]
...
[ ·⏮· ][ ·◀️· ][ 1/13 ][ ▶️ ][ ⏭ ]
```

#### Example — dynamic search results

The search query is encoded directly into the `callback_data`.

```js
bot.action(/^search_(.+)_page_(\d+)$/, async (ctx) => {
  const query = ctx.match[1];
  const page = parseInt(ctx.match[2]) || 1;
  const results = await search(query);

  if (results.length === 0) {
    return ctx.answerCbQuery("🚫 No results found");
  }

  const keyboard = new InlineKeyboardBuilder().paginatedList({
    items: results,
    page,
    perPage: 4,
    render: (result) => ({
      text: `📄 ${result.title}`,
      callback_data: `open_doc_${result.id}`,
    }),
    pagination: {
      callback: (p) => `search_${query}_page_${p}`,
      counterCallback: `search_info_${query}`,
      hideIfSinglePage: true,
    },
  });

  await ctx.editMessageText(`🔍 "${query}"`, {
    reply_markup: keyboard.build(),
  });
});
```

> ⚠️ **Telegram limit:** `callback_data` is capped at **64 bytes**.  
> If the search query can be long, encode it (e.g. truncated base64) or store it in session.

---

### Concrete v3 example

```js
const builder = new InlineKeyboardBuilder(2, 30)
  .addCallbackButtonFromParts("user", "like", 42, "Like", { style: "success" })
  .addCallbackButtonFromParts("user", "dislike", 43, "Dislike", {
    style: "danger",
  })
  .newRow()
  .addUrlButton(
    "Docs",
    "https://github.com/neoncraftx/telegram-inline-keyboard-builder",
  )
  .addCallbackButton("Cancel", "cancel_action");

console.log(builder.preview());
// Row 1: [Like](callback:user:like:42) | [Dislike](callback:user:dislike:43)
// Row 2: [Docs](https://github.com/neoncraftx/telegram-inline-keyboard-builder) | [Cancel](callback:cancel_action)

console.log(builder.callbackDataParse("user:like:42"));
// { scope: "user", action: "like", id: "42" }
```

## 🔥 New update 🔥

- Added color style for premium Telegram buttons and icons
- Builder method typing

## How does this feature work?

Simply specify a new parameter to the function to add the URL and class.

```js
addCallbackButton(text, callback_data, (options = {}));
addUrlButton(text, url, (options = {}));
```

The options must contain at least one of these parameters: either `icon_custom_emoji_id` or `style`

```js
// Example
const keyboard = new InlineKeyboardBuilder(1)
  .addCallbackButton("blue button", "click", {
    style: "primary",
  })
  .addCallbackButton("blue button with icon", "click", {
    icon_custom_emoji_id: "4963511421280192936",
    style: "primary",
  })
  .addCallbackButton("Just a icon", "click", {
    icon_custom_emoji_id: "4963511421280192936",
  });
```

> **Warning**: `icon_custom_emoji_id` only works if the bot owner has a Telegram premium subscription.

## Example Usage (telegraf)

```js
// start command
bot.start(async (ctx) => {
  const keyboard = new InlineKeyboardBuilder(1)
    .addCallbackButton("blue", "click", {
      style: "primary",
    })
    .addCallbackButton("blue with icon", "click", {
      icon_custom_emoji_id: "4963511421280192936",
      style: "primary",
    })
    .addCallbackButton("green", "click", {
      style: "success",
    })
    .addCallbackButton("green with icon", "click", {
      icon_custom_emoji_id: "4963511421280192936",
      style: "success",
    })
    .addCallbackButton("red", "danger", {
      style: "danger",
    })
    .addCallbackButton("red with icon", "click", {
      icon_custom_emoji_id: "4963511421280192936",
      style: "danger",
    })
    .addCallbackButton("Just a icon", "click", {
      icon_custom_emoji_id: "4963511421280192936",
    });
  await ctx.reply("🚀 New Button style 🔥🔥🔥", keyboard.build());
});
```

### Results

![Example results](https://i.ibb.co/1tgyYQCv/IMG-20260211-054905-332.jpg)

---

> Version 2 removes adapters and focuses on a single universal output:
> **valid `inline_keyboard` JSON as expected by Telegram API**.

---

## 🚀 Key Features

- Fluent & chainable API — library-agnostic (no adapters, no runtime dependencies)
- Produces **pure Telegram inline keyboard JSON**
- Auto-wrap, row control, `paginatedList()`, `preview()`
- **Smart Validation & Warnings (v3.2.3)** — ESLint-style rules, plugins, strict/warn/silent modes
- Zero framework coupling — works with Telegraf, node-telegram-bot-api, or any Bot API client

---

## Installation

```bash
npm install telegram-inline-keyboard-builder
```

## importation

```js
import {
  InlineKeyboardBuilder,
  ValidationError,
  ValidationEngine,
  createValidationEngine,
  RULE_IDS,
  createDiagnostic,
  normalizeKeyboard,
} from "telegram-inline-keyboard-builder";
```

Types: `ValidationResult`, `Diagnostic`, `ValidationRule`, `ValidationPlugin`, `BuildOptions`, `ValidateOptions`, `ValidationMode`, etc.

## 🧠 Core Concept

Telegram inline keyboards follow **one universal schema**.

This builder:

- generates the keyboard **directly in Telegram format**

- lets you pass the result to **any Telegram library**

```js
{ reply_markup: { inline_keyboard: [...] } }
```

- **No adapters**.
- **No wrappers**.
- **No framework coupling**.

## 🔧 Public API

### Constructor

```js
new InlineKeyboardBuilder((buttonsPerRow = 2), (autoWrapMaxChars = 0));
```

### Chainable Methods

```js
.addCallbackButton(text, callback_data, options = {})
.addCallbackButtonFromParts(scope, action, id, text, options = {}, separator = ":")
.addUrlButton(text, url, options = {})
.addPayButton(text)
.addCustomButton(buttonObject)
.addButtons(config)
.setButtonsPerRow(n)
.setAutoWrapMaxChars(n)
.newRow()
.preview()
.paginatedList(options = {})

// Validation (v3.2.3)
.validate(options = {})
.registerRule(rule)
.use(plugin)
.setRules(config)
.setRuleEnabled(ruleId, enabled)
.setRuleSeverity(ruleId, severity)
.setValidationMode("strict" | "warn" | "silent")
.setValidationContext("default" | "message" | "invoice" | "edit")

// Build
.build()
.build({ validate: true, validationMode: "strict" | "warn" | "silent" })
```

```js
const keyboard = builder.build();
// → { reply_markup: { inline_keyboard: [...] } }

const safe = builder.build({ validate: true, validationMode: "strict" });
// → throws ValidationError if errors exist
```

Fully compliant with Telegram Bot API.

## Usage Example (Telegraf)

```js
import { Telegraf } from "telegraf";

import { InlineKeyboardBuilder } from "telegram-inline-keyboard-builder";

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start((ctx) => {
  const keyboard = new InlineKeyboardBuilder(2, 24)
    .addCallbackButton("✅ OK", "OK_ACTION")
    .addUrlButton("🌍 Website", "https://example.com")
    .newRow()
    .addCallbackButton("❌ Cancel", "CANCEL_ACTION")
    .build();
  ctx.reply("Welcome 👋\nChoose an action:", keyboard);
});

bot.launch();
```

## Usage Example (node-telegram-bot-api)

```js
import TelegramBot from "node-telegram-bot-api";

import { InlineKeyboardBuilder } from "telegram-inline-keyboard-builder";

const bot = new TelegramBot(TOKEN, { polling: true });
bot.onText(/\/start/, (msg) => {
  const keyboard = new InlineKeyboardBuilder()
    .addCallbackButton("OK", "OK")
    .addUrlButton("Site", "https://example.com")
    .build();

  bot.sendMessage(msg.chat.id, "Hello", keyboard);
});
```

## 💳 Payment Buttons

### ⚠️ Telegram limitation

> [!WARNING]
> Payment buttons must only be used with:

- sendInvoice
- replyWithInvoice

They must be hidden in normal messages.

```js
.addPayButton("Pay now");
```

Using a visible payment button outside invoices will cause Telegram API errors.

## 🧯 Common Errors

**Telegram API error**

Make sure the keyboard object is passed directly:

```js
const keyboard = new InlineKeyboardBuilder(1)
.addCallbackButton("Setting","show_setting")
.build()
// telegraf
ctx.reply("Text", keyboard);

// node telegram bot api
bot.sendMessage(chatId, "Text", keyboard);

// CORRECT ✅

// OR if you want to include it in the options

const keyboard = new InlineKeyboardBuilder(1)
.addCallbackButton("Setting","show_setting")
.build()

// telegraf
ctx.reply("Text", {
reply_markup: keyboard.reply_makup, // inline keyboard
parse_mode: "HTML",
// ...
});

// node telegram bot api
bot.sendMessage(chatId, "Text", {
reply_markup: keyboard.reply_makup, // inline keyboard
parse_mode: "HTML",
// ...
);
```

## Migration to V2

- **V1**: The inline keyboard builder used **adapters** for each new API, resulting in code that was **unmaintainable** in case of **updates**.

- **V2**: Here we **simply construct an object valid for all types of APIs** without **adapting** it.

## Migration to V3.2.3

See [Version 3.2.3 — Smart Validation & Warnings](#version-323--smart-validation--warnings) for validation rollout. **No breaking changes** — validation is opt-in.

## Migration to V3

- **V3** is **fully backward compatible** with V2. No breaking changes — existing code requires no modification.

The new constructor signature accepts two explicit parameters:

```js
// V2
const builder = new InlineKeyboardBuilder();

// V3 — same, still works. New optional parameters:
const builder = new InlineKeyboardBuilder(
  buttonsPerRow, // number — buttons per row (default: 2)
  autoWrapMaxChars, // number — auto line-break threshold (default: 0)
);
```

New methods are purely additive. Adopt them progressively:

| What you had (V2)                          | What you can use now (V3)                                      |
| ------------------------------------------ | -------------------------------------------------------------- |
| Manual `callback_data` string              | `.addCallbackButtonFromParts(scope, action, id, text)`         |
| `console.log(builder.build())` to inspect  | `.preview()` — row-by-row readable output                      |
| Manual `callback_data` parsing in handlers | `.callbackDataParse(data)` → `{ scope, action, id }`           |
| Manual pagination with multiple handlers   | `.paginatedList({ items, page, perPage, render, pagination })` |

> **V2 → V3 checklist**
>
> - [ ] Update the package: `npm install telegram-inline-keyboard-builder@latest`
> - [ ] Replace manual `callback_data` concatenations with `addCallbackButtonFromParts()`
> - [ ] Replace manual pagination logic with `paginatedList()`
> - [ ] Use `preview()` during development to verify keyboard layout before send
> - [ ] (v3.2.3+) Enable `build({ validate: true })` or `validate()` in tests — see [Smart Validation](#version-323--smart-validation--warnings)

## 💜 Support This Project (Crypto)

This project is maintained in my free time.  
If it helped you, consider supporting it with a crypto donation ❤️  
It helps me maintain and improve the project.

You can send donations to the following addresses:

| Crypto                 | Address                                            |
| ---------------------- | -------------------------------------------------- |
| **USDT (TRC20)**       | `0x607c1430601989d43c9CD2eeD9E516663e0BdD1F`       |
| **USDC (Polygon/ETH)** | `0x607c1430601989d43c9CD2eeD9E516663e0BdD1F`       |
| **Ethereum (ETH)**     | `0x607c1430601989d43c9CD2eeD9E516663e0BdD1F`       |
| **Bitcoin (BTC)**      | `bc1qmysepz6eerz2mqyx5dd0yy87c3gk6hccwla5x2`       |
| **Tron (TRX)**         | `TE9RiTaDpx7DGZzCMw7qds51nzszKiyeR8`               |
| **TON**                | `UQA1NPW4GqgIVa9R6lebN_0v64Q-Sz_nHrmK9LCk-FfdjVOH` |

### 🔹 Optional QR Codes for quick mobile donation

**USDT (TRC20)**  
![USDT TRC20 QR](https://api.qrserver.com/v1/create-qr-code/?data=0x607c1430601989d43c9cd2eed9e516663e0bdd1f&size=150x150)

**USDC**  
![USDC QR](https://api.qrserver.com/v1/create-qr-code/?data=0x607c1430601989d43c9CD2eeD9E516663e0BdD1F&size=150x150)

**Ethereum (ETH)**  
![ETH QR](https://api.qrserver.com/v1/create-qr-code/?data=0x607c1430601989d43c9CD2eeD9E516663e0BdD1F&size=150x150)

**Bitcoin (BTC)**  
![BTC QR](https://api.qrserver.com/v1/create-qr-code/?data=bc1qmysepz6eerz2mqyx5dd0yy87c3gk6hccwla5x2&size=150x150)

**Tron (TRX)**  
![TRX QR](https://api.qrserver.com/v1/create-qr-code/?data=TE9RiTaDpx7DGZzCMw7qds51nzszKiyeR8&size=150x150)

**TON**  
![TON QR](https://api.qrserver.com/v1/create-qr-code/?data=UQA1NPW4GqgIVa9R6lebN_0v64Q-Sz_nHrmK9LCk-FfdjVOH&size=150x150)

## ✍️ Contribution

Contributions are welcome ❤️
Please open an issue before proposing major changes.
