![Logo](https://i.ibb.co/BKVnp8dZ/20260202-141042.png) [![npm version](https://img.shields.io/npm/v/telegram-inline-keyboard-builder?style=flat&logo=npm&logoColor=white&color=cb3837)](https://www.npmjs.com/package/telegram-inline-keyboard-builder) [![npm downloads](https://img.shields.io/npm/dw/telegram-inline-keyboard-builder?style=flat&logo=npm&logoColor=white&color=2CA5E0)](https://www.npmjs.com/package/telegram-inline-keyboard-builder) [![license](https://img.shields.io/npm/l/telegram-inline-keyboard-builder?style=flat&color=555555)](LICENSE) ![Telegram](https://img.shields.io/badge/Telegram-Inline%20Keyboard-2CA5E0?style=flat&logo=telegram&logoColor=white) 

# Inline Keyboard Builder (v2) Universal inline keyboard builder for Telegram Bots. 
Produces **pure Telegram Bot API compliant JSON**, usable with **any library** (Telegraf, node-telegram-bot-api, Pyrogram, Aiogram, Puregram, Telebot…). 

> Version 2 removes adapters and focuses on a single universal output: 
> **valid `inline_keyboard` JSON as expected by Telegram API**. 

--- 
## 🚀 Key Features - Fluent & chainable API - Library-agnostic (no adapters, no dependencies) 

- Produces **pure Telegram inline keyboard JSON** 
- Auto-wrap & row control - Works with **any Telegram framework** 
- Zero abstraction leak

--- 

##  Installation

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

* generates the keyboard **directly in Telegram format**

* lets you pass the result to **any Telegram library**
```js
{ reply_markup: { inline_keyboard: [...] } } 
```
- **No adapters**.
- **No wrappers**.
- **No framework coupling**.

## 🔧 Public API

### Constructor

```js
new InlineKeyboardBuilder({ buttonsPerRow = 2, autoWrapMaxChars = 0 }) 

//Chainable Methods

.addCallbackButton(text, callback_data, hide = false) 
.addUrlButton(text, url, hide = false) 
.addPayButton(text, options = {}) 
.addCustomButton(buttonObject) 
.addButtons(config) 
.setButtonsPerRow(n) 
.setAutoWrapMaxChars(n) 
.newRow() 

// build
.build() 

const keyboard = builder.build(); 

// Always returns:

{ reply_markup: { inline_keyboard: [...] } } 
```
Fully compliant with Telegram Bot API.

<<<<<<< HEAD
**Telegraf adapte** → Markup.inlineKeyboard(rows) (Markup object) 

**Node‑Telegram adapt** → { reply_markup: { inline_keyboard: rows } }



> [!WARNING]
> To use `addPayButton`  only in **sendInvoice** or **replyWithInvoice** (telegraf).We set **hide** to **true** in the **options** 

``` js
 addPayButton("My pay button :D",{hide: true});
```


---

## 🧩 Usage Example (Telegraf)
=======
##  Usage Example (Telegraf)
>>>>>>> 46cb63a (Refactor: remove adapter to builder in JS folder + update README)

```js
import { Telegraf } from "telegraf";

import { InlineKeyboardBuilder } from "telegram-inline-keyboard-builder"; 

const bot = new Telegraf(process.env.BOT_TOKEN); 

bot.start(ctx => {
 const keyboard = new InlineKeyboardBuilder({ buttonsPerRow: 2, autoWrapMaxChars: 24 }) 
.addCallbackButton("✅ OK", "OK_ACTION")
.addUrlButton("🌍 Website", "https://example.com") 
.newRow() 
.addCallbackButton("❌ Cancel", "CANCEL_ACTION") 
.build(); 
ctx.reply("Welcome 👋\nChoose an action:", keyboard); }); 

bot.launch(); 

```
## Usage Example (node-telegram-bot-api)

```js
import TelegramBot from "node-telegram-bot-api"; 

import { InlineKeyboardBuilder } from "telegram-inline-keyboard-builder"; 

const bot = new TelegramBot(TOKEN, { polling: true }); 
bot.onText(/\/start/, msg => { 
const keyboard = new InlineKeyboardBuilder() 
.addCallbackButton("OK", "OK") 
.addUrlButton("Site", "https://example.com") 
.build(); 

bot.sendMessage(msg.chat.id, "Hello", keyboard); }); 
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

<<<<<<< HEAD
> [!ERROR]
> **ReferenceError**: Markup is not defined → you are still using Markup in the core; move button creation into the adapter. 
=======
**Telegram API error**
>>>>>>> 46cb63a (Refactor: remove adapter to builder in JS folder + update README)

Make sure the keyboard object is passed directly:

<<<<<<< HEAD
> [!ERROR]
> **Missing adapter** → the core constructor must receive a valid adapter: new InlineKeyboardBuilder(adapter).

> [!ERROR]
> **Library not installed** (e.g., telegraf missing) → adapter should detect and throw a clear error: npm install telegraf.


> [!ERROR]
> **Invalide inlinekeyboard**: This error can occur when the payment button function is called and **hide** is set to **false**, which is the **default**. 
=======
```js
const keyboard = new InlineKeyboardBuilder(1)
.addCallbackButton("Setting","show_setting")
.build()
// telegraf
ctx.reply("Text", keyboard);

// node telegram bot api
bot.sendMessage(chatId, "Text", keyboard); 

// CORRECT ✅
>>>>>>> 46cb63a (Refactor: remove adapter to builder in JS folder + update README)

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

## 💜 Support This Project (Crypto)

This project is maintained in my free time.  
If it helped you, consider supporting it with a crypto donation ❤️  
It helps me maintain and improve the project.

You can send donations to the following addresses:

| Crypto | Address |
|--------|---------|
| **USDT (TRC20)** | `0x607c1430601989d43c9CD2eeD9E516663e0BdD1F` |
| **USDC (Polygon/ETH)** | `0x607c1430601989d43c9CD2eeD9E516663e0BdD1F` |
| **Ethereum (ETH)** | `0x607c1430601989d43c9CD2eeD9E516663e0BdD1F` |
| **Bitcoin (BTC)** | `bc1qmysepz6eerz2mqyx5dd0yy87c3gk6hccwla5x2` |
| **Tron (TRX)** | `TE9RiTaDpx7DGZzCMw7qds51nzszKiyeR8` |
| **TON** | `UQA1NPW4GqgIVa9R6lebN_0v64Q-Sz_nHrmK9LCk-FfdjVOH` |

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

Everyone are welcome. Open an issue to discuss a feature before implementing major changes.
---
Contributions are welcome ❤️
Please open an issue before proposing major changes.

