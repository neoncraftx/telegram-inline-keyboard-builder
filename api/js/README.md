### Inline Keyboard Builder

Small inline button builder for Telegram, designed to be library-agnostic (Telegraf, node-telegram-bot-api, Aiogram, Pyrogram...).

> Principle: a central logic core handles button creation and placement. Adapters transform the neutral structure into the format expected by the target API.




---

## 🚀 Key Features

- Fluent, chainable API

- Core independent of any Telegram library

- Easy-to-write adapters (Telegraf, node-telegram-bot-api, Aiogram...)

- Auto-wrap / control of buttons per row



---

##  Installation

If the package is published on npm:

```bash
npm install telegram-inline-keyboard-builder
```
Then in your project:

```js
import { InlineKeyboardTelegraf } from "telegram-inline-keyboard-builder";
```

---

## Quick Concepts

- **Core**: InlineKeyboardBuilder (placement logic, chainable API). Does not know any Telegram library.

- **Adapter**: object responsible for creating buttons (callback/url/pay/custom) and producing the final structure (reply_markup/Markup depending on the library).

- **Facade Builder**: ready-to-use classes that inject an adapter (e.g., InlineKeyboardTelegraf, InlineKeyboardNodeTelegram).



---

## 🔧 Public Interface (API)

### Constructors
```js
// Core (internal)

new InlineKeyboardBuilder(adapter, buttonsPerRow = 2, autoWrapMaxChars = 0)

// Facade (exposed to users, encapsulates core + adapter)
new InlineKeyboardTelegraf({ buttonsPerRow = 2, autoWrapMaxChars = 0 })
new InlineKeyboardNodeTelegram({ ... })

Chainable Methods

.addCallbackButton(text, callback_data, hide = false)
.addUrlButton(text, url, hide = false)
.addPayButton(text, options = {})
.addCustomButton(btnObj)
.addButtons(config) // array or { type, buttons: [...] }
.setButtonsPerRow(n)
.setAutoWrapMaxChars(n)
.newRow() // forces a new row
.build() // returns the keyboard formatted by the adapter
```
**Return of build()**: depends on the adapter.

**Telegraf adapte** → Markup.inlineKeyboard(rows) (Markup object) 

**Node‑Telegram adapt** → { reply_markup: { inline_keyboard: rows } }



---

## 🧩 Usage Example (Telegraf)

```js
import { Telegraf } from "telegraf";
import { InlineKeyboardTelegraf } from "telegram-inline-keyboard-builder";

const bot = new Telegraf(process.env.BOT_TOKEN);

bot.start(ctx => {
  const keyboard = new InlineKeyboardTelegraf({ buttonsPerRow: 2, autoWrapMaxChars: 24 })
    .addCallbackButton("✅ OK", "OK_ACTION")
    .addUrlButton("🌍 Site", "https://example.com")
    .newRow()
    .addCallbackButton("❌ Cancel", "CANCEL_ACTION")
    .build();

  ctx.reply("Welcome 👋\nChoose an action:", keyboard);
});

bot.launch();
```

## 🧾 Usage Example (node-telegram-bot-api)

```js
import TelegramBot from "node-telegram-bot-api";
import { InlineKeyboardNodeTelegram } from "telegram-inline-keyboard-builder";

const bot = new TelegramBot(TOKEN, { polling: true });

bot.onText(/\/start/, (msg) => {
  const kb = new InlineKeyboardNodeTelegram()
    .addCallbackButton("OK", "OK")
    .addUrlButton("Site", "https://example.com")
    .build();

  // kb === { reply_markup: { inline_keyboard: [...] } }
  bot.sendMessage(msg.chat.id, "Hello", kb);
});

```
---

## 🛠️ Writing an Adapter (expected interface)

A simple adapter must expose:

```js
// create a button
adapter.createCallback(text, data, hide = false)
adapter.createUrl(text, url, hide = false)
adapter.createPay(text, hide = false)

// build the final keyboard from rows (rows = array of array of buttons)
adapter.buildKeyboard(rows)

Minimal Example (node-telegram-bot-api)

export class NodeTelegramInlineAdapter {
  createCallback(text, data) {
    return { text, callback_data: data };
  }

  createUrl(text, url) {
    return { text, url };
  }

  createPay(text) {
    return { text, pay: true };
  }

  buildKeyboard(rows) {
    return { reply_markup: { inline_keyboard: rows } };
  }
}
```
---
##  ✅ API supported
- Telegraf
- Purgram
- Node-telegram-bot-api
- Telebot
---

## 🧯 Common Errors & Debug

**ReferenceError**: Markup is not defined → you are still using Markup in the core; move button creation into the adapter.

**Missing adapter** → the core constructor must receive a valid adapter: new InlineKeyboardBuilder(adapter).

**Library not installed** (e.g., telegraf missing) → adapter should detect and throw a clear error: npm install telegraf.


---

✍️ Contribution

Everyone are welcome. Open an issue to discuss a feature before implementing major changes.


---
