![Logo](https://i.ibb.co/BKVnp8dZ/20260202-141042.png) [![PyPI version](https://img.shields.io/pypi/v/telegram-inline-keyboard-builder?style=flat&logo=pypi&logoColor=white&color=3776AB)](https://pypi.org/project/telegram-inline-keyboard-builder/)
[![Downloads](https://img.shields.io/pypi/dm/telegram-inline-keyboard-builder?style=flat&logo=python&logoColor=white&color=4B8BBE)](https://pypi.org/project/telegram-inline-keyboard-builder/)
[![Python versions](https://img.shields.io/pypi/pyversions/telegram-inline-keyboard-builder?style=flat&logo=python&logoColor=white&color=FFD43B)](https://pypi.org/project/telegram-inline-keyboard-builder/) [![license](https://img.shields.io/npm/l/telegram-inline-keyboard-builder?style=flat&color=555555)](LICENSE) ![Telegram](https://img.shields.io/badge/Telegram-Inline%20Keyboard-2CA5E0?style=flat&logo=telegram&logoColor=white) 

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
pip install telegram-inline-keyboard-builder
```
## importation
```python
from telegram_inline_keyboard_builder import InlineKeyboardBuilder 
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

```python

InlineKeyboardBuilder(buttons_per_row=2, auto_wrap_max_chars=20)
# Chainable Methods

.add_callback_button(text, callback_data, hide = false) 
.add_url_button(text, url, hide = false) 
.add_pay_button(text) 
.add_custom_button(buttonObject) 
.add_buttons(config) 
.set_buttons_per_row(n) 
.set_auto_wrap_max_chars(n) 
.new_row() 

# build
.build() 

keyboard = builder.build(); 

# Always returns:

# { reply_markup: { inline_keyboard: [...] } } 
```
Fully compliant with Telegram Bot API.

##  Usage Example (python-telegram-bot)

```python
import asyncio
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    CallbackQueryHandler,
)
from telegram_inline_keyboard_builder import InlineKeyboardBuilder

TOKEN = ""


# ---------- Command /start ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # Keyboard Builder 
    keyboard = (
        InlineKeyboardBuilder(buttons_per_row=2, auto_wrap_max_chars=20)
        .add_callback_button("✅ Confirm", "CONFIRM_ACTION")
        .add_url_button("🌍 Website", "https://example.com")
        .build()
    )

    await update.message.reply_text(
        "Welcome 👋\nChoose an option:",
        reply_markup=keyboard["reply_markup"],
    )


# ---------- Callback handler ----------
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "CONFIRM_ACTION":
        await query.edit_message_text("You pressed Confirm ✅")


# ---------- Main ----------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))

    print("Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()


```

---

## 💳 Payment Buttons

### ⚠️ Telegram limitation

> [!WARNING]
> Payment buttons must only be used with:
- sendInvoice 

They must be hidden in normal messages.

```python
.add_pay_button("Pay now"); 
```

Using a visible payment button outside invoices will cause Telegram API errors.

## 🧯 Common Errors

**Telegram API error**

Make sure the keyboard object is passed directly:

```python

# python-telegram-bot 
keyboard = (
        InlineKeyboardBuilder(buttons_per_row=2, auto_wrap_max_chars=20)
        .add_callback_button("✅ Confirm", "CONFIRM_ACTION")
        .add_url_button("🌍 Website", "https://example.com")
        .build()
    )

    await update.message.reply_text(
        "Welcome 👋\nChoose an option:",
       //here
 reply_markup=keyboard["reply_markup"],
    ) 
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

Contributions are welcome ❤️
Please open an issue before proposing major changes.
