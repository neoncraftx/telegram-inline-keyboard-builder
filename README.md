![Logo](https://i.ibb.co/BKVnp8dZ/20260202-141042.png)

[![npm version](https://img.shields.io/npm/v/telegram-inline-keyboard-builder?style=flat&logo=npm&logoColor=white&color=cb3837)](https://www.npmjs.com/package/telegram-inline-keyboard-builder)
[![npm downloads](https://img.shields.io/npm/dw/telegram-inline-keyboard-builder?style=flat&logo=npm&logoColor=white&color=2CA5E0)](https://www.npmjs.com/package/telegram-inline-keyboard-builder)
[![PyPI version](https://img.shields.io/pypi/v/telegram-inline-keyboard-builder?style=flat&logo=pypi&logoColor=white&color=3776AB)](https://pypi.org/project/telegram-inline-keyboard-builder/)
[![PyPI downloads](https://img.shields.io/pypi/dm/telegram-inline-keyboard-builder?style=flat&logo=python&logoColor=white&color=4B8BBE)](https://pypi.org/project/telegram-inline-keyboard-builder/)
[![Python versions](https://img.shields.io/pypi/pyversions/telegram-inline-keyboard-builder?style=flat&logo=python&logoColor=white&color=FFD43B)](https://pypi.org/project/telegram-inline-keyboard-builder/)
[![license](https://img.shields.io/npm/l/telegram-inline-keyboard-builder?style=flat&color=555555)](LICENSE)
![Telegram](https://img.shields.io/badge/Telegram-Inline%20Keyboard-2CA5E0?style=flat&logo=telegram&logoColor=white)

# Inline Keyboard Builder

Universal inline keyboard builder for Telegram bots — available for **Node.js** and **Python**.

Produces **pure Telegram Bot API compliant JSON**, compatible with any library:
Telegraf, node-telegram-bot-api, Aiogram, Pyrogram, Telebot, and more.

---

## Why this library?

Telegram inline keyboards always follow the same JSON schema regardless of the framework you use. Yet most solutions tie you to a specific library, force you to use adapters, or make you concatenate `callback_data` strings by hand.

This builder generates the keyboard **directly in Telegram format** and hands you back a plain dict — no adapters, no wrappers, no framework coupling.

```json
{ "reply_markup": { "inline_keyboard": [[...], [...]] } }
```

Pass it to any library, any bot framework, any language.

---

## Key features

- **Fluent chainable API** — compose keyboards in a single expression
- **Library-agnostic** — one output format, every framework
- **Auto-wrap & row control** — `buttonsPerRow`, `autoWrapMaxChars`, `newRow()`
- **Premium button styles** — `primary`, `success`, `danger` + custom emoji icons
- **Structured callbacks** — build and parse `scope:action:id` strings without concatenation
- **Built-in pagination** — turn any list into a paginated keyboard in one call
- **Developer tools** — `preview()` prints the keyboard layout before you send it
- **Fully typed** — TypeScript types (JS) and `TypedDict` / `Literal` annotations (Python)

---

## Installation

**Node.js**

```bash
npm install telegram-inline-keyboard-builder
```

```js
import { InlineKeyboardBuilder } from "telegram-inline-keyboard-builder";
```

**Python**

```bash
pip install telegram-inline-keyboard-builder
```

```python
from telegram_inline_keyboard_builder import InlineKeyboardBuilder
```

---

## Quick start

**Node.js / TypeScript**

```js
import { InlineKeyboardBuilder } from "telegram-inline-keyboard-builder";

const keyboard = new InlineKeyboardBuilder(2)
  .addCallbackButton("✅ Confirm", "confirm_action", { style: "success" })
  .addCallbackButton("❌ Cancel",  "cancel_action",  { style: "danger"  })
  .newRow()
  .addUrlButton("📖 Documentation", "https://anitec.gitbook.io/telegram-inline-keyboard-builder")
  .build();

// Telegraf
ctx.reply("Choose an action:", keyboard);

// node-telegram-bot-api
bot.sendMessage(chatId, "Choose an action:", keyboard);
```

**Python**

```python
from telegram_inline_keyboard_builder import InlineKeyboardBuilder

keyboard = (
    InlineKeyboardBuilder(buttons_per_row=2)
    .add_callback_button("✅ Confirm", "confirm_action", style="success")
    .add_callback_button("❌ Cancel",  "cancel_action",  style="danger")
    .new_row()
    .add_url_button("📖 Documentation", "https://anitec.gitbook.io/telegram-inline-keyboard-builder")
    .build()
)

# python-telegram-bot
await update.message.reply_text("Choose an action:", reply_markup=keyboard["reply_markup"])

# Aiogram
await message.answer("Choose an action:", reply_markup=InlineKeyboardMarkup(
    inline_keyboard=keyboard["reply_markup"]["inline_keyboard"]
))
```

---

## Documentation

Full API reference, guides, and examples are available at:

**[📚 anitec.gitbook.io/telegram-inline-keyboard-builder](https://anitec.gitbook.io/telegram-inline-keyboard-builder)**

Topics covered in the docs:

- Complete API reference for Node.js and Python
- Button types: callback, URL, pay, custom
- Premium button styles and emoji icons
- Structured `callback_data` with `addCallbackButtonFromParts` / `add_callback_button_from_parts`
- Paginated lists with `paginatedList` / `paginated_list`
- Layout controls: `buttonsPerRow`, `autoWrapMaxChars`, `newRow`
- Developer tools: `preview()`, `callbackDataParse()` / `callback_data_parse()`
- Usage examples for Telegraf, node-telegram-bot-api, Aiogram, python-telegram-bot
- Migration guides from v1 and v2

---

## 💜 Support this project

This project is maintained in my free time.
If it helped you, consider supporting it with a crypto donation ❤️

| Crypto | Address |
|--------|---------|
| **USDT (TRC20)** | `0x607c1430601989d43c9CD2eeD9E516663e0BdD1F` |
| **USDC (Polygon/ETH)** | `0x607c1430601989d43c9CD2eeD9E516663e0BdD1F` |
| **Ethereum (ETH)** | `0x607c1430601989d43c9CD2eeD9E516663e0BdD1F` |
| **Bitcoin (BTC)** | `bc1qmysepz6eerz2mqyx5dd0yy87c3gk6hccwla5x2` |
| **Tron (TRX)** | `TE9RiTaDpx7DGZzCMw7qds51nzszKiyeR8` |
| **TON** | `UQA1NPW4GqgIVa9R6lebN_0v64Q-Sz_nHrmK9LCk-FfdjVOH` |

<details>
<summary>🔹 QR codes for quick mobile donation</summary>

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

</details>

---

## ✍️ Contribution

Contributions are welcome ❤️
Please open an issue before proposing major changes.