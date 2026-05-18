![Logo](https://i.ibb.co/BKVnp8dZ/20260202-141042.png) [![npm version](https://img.shields.io/npm/v/telegram-inline-keyboard-builder?style=flat&logo=npm&logoColor=white&color=cb3837)](https://www.npmjs.com/package/telegram-inline-keyboard-builder) [![npm downloads](https://img.shields.io/npm/dw/telegram-inline-keyboard-builder?style=flat&logo=npm&logoColor=white&color=2CA5E0)](https://www.npmjs.com/package/telegram-inline-keyboard-builder) [![license](https://img.shields.io/npm/l/telegram-inline-keyboard-builder?style=flat&color=555555)](LICENSE) ![Telegram](https://img.shields.io/badge/Telegram-Inline%20Keyboard-2CA5E0?style=flat&logo=telegram&logoColor=white)

# Inline Keyboard Builder (v3) Universal inline keyboard builder for Telegram Bots.

Produces **pure Telegram Bot API compliant JSON**, usable with **any library** (Telegraf, node-telegram-bot-api, Pyrogram, Aiogram, Puregram, Telebot…).

---

## Table of Contents

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

## other log

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

## 🚀 Key Features - Fluent & chainable API - Library-agnostic (no adapters, no dependencies)

- Produces **pure Telegram inline keyboard JSON**
- Auto-wrap & row control - Works with **any Telegram framework**
- Zero abstraction leak

---

## Installation

```bash
npm install telegram-inline-keyboard-builder
```

## importation

```js
import { InlineKeyboardBuilder } from "telegram-inline-keyboard-builder";
```

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
```

// build
.build()

const keyboard = builder.build();

// Always returns:

{ reply_markup: { inline_keyboard: [...] } }

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
> - [ ] Use `preview()` during development to verify keyboard layout before se

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
