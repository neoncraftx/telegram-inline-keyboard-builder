![Logo](https://i.ibb.co/BKVnp8dZ/20260202-141042.png) [![PyPI version](https://img.shields.io/pypi/v/telegram-inline-keyboard-builder?style=flat&logo=pypi&logoColor=white&color=3776AB)](https://pypi.org/project/telegram-inline-keyboard-builder/)
[![Downloads](https://img.shields.io/pypi/dm/telegram-inline-keyboard-builder?style=flat&logo=python&logoColor=white&color=4B8BBE)](https://pypi.org/project/telegram-inline-keyboard-builder/)
[![Python versions](https://img.shields.io/pypi/pyversions/telegram-inline-keyboard-builder?style=flat&logo=python&logoColor=white&color=FFD43B)](https://pypi.org/project/telegram-inline-keyboard-builder/) [![license](https://img.shields.io/npm/l/telegram-inline-keyboard-builder?style=flat&color=555555)](LICENSE) ![Telegram](https://img.shields.io/badge/Telegram-Inline%20Keyboard-2CA5E0?style=flat&logo=telegram&logoColor=white)

# Inline Keyboard Builder (v3) — Python

Universal inline keyboard builder for Telegram bots.
Produces **pure Telegram Bot API compliant JSON**, usable with **any library**
(python-telegram-bot, Aiogram, Pyrogram, Telebot…).

> Version 3 brings full feature parity with the JavaScript/TypeScript edition:
> `add_callback_button_from_parts()`, `callback_data_parse()`, `preview()`,
> `paginated_list()`, and strongly typed interfaces throughout.

---

## Table of Contents

- [Installation](#installation)
- [Import](#import)
- [Package structure](#package-structure)
- [Core concept](#core-concept)
- [Public API](#public-api)
  - [Constructor](#constructor)
  - [add_callback_button()](#add_callback_button)
  - [add_callback_button_from_parts()](#add_callback_button_from_parts)
  - [add_url_button()](#add_url_button)
  - [add_pay_button()](#add_pay_button)
  - [add_custom_button()](#add_custom_button)
  - [add_buttons()](#add_buttons)
  - [callback_data()](#callback_data)
  - [callback_data_parse()](#callback_data_parse)
  - [preview()](#preview)
  - [paginated_list()](#paginated_list)
  - [set_buttons_per_row() / set_auto_wrap_max_chars()](#layout-controls)
  - [new_row()](#new_row)
  - [build()](#build)
- [Usage examples](#usage-examples)
  - [python-telegram-bot](#python-telegram-bot)
  - [Aiogram](#aiogram)
  - [Paginated product list](#paginated-product-list)
  - [Paginated user list with edge buttons](#paginated-user-list-with-edge-buttons)
  - [Dynamic search results](#dynamic-search-results)
- [Premium button styles](#premium-button-styles)
- [Payment buttons](#payment-buttons)
- [Common errors](#common-errors)
- [Migration to v3](#migration-to-v3)
- [Support this project](#support-this-project)
- [Contribution](#contribution)

---

## Installation

```bash
pip install telegram-inline-keyboard-builder
```

## Import

```python
from telegram_inline_keyboard_builder import InlineKeyboardBuilder

# Optional: import type hints for your own type-annotated code
from telegram_inline_keyboard_builder.types import (
    PaginatedListOptions,
    PaginationConfig,
    PaginationLabels,
    ButtonConfig,
)
```

---

## Package structure

```
telegram_inline_keyboard_builder/
├── __init__.py          # public exports
├── builder.py           # InlineKeyboardBuilder class
└── types/
    ├── __init__.py
    ├── buttons.py        # ButtonStyle, CallbackButton, UrlButton …
    └── utils.py          # PaginationLabels, PaginationConfig, PaginatedListOptions
```

---

## Core concept

Telegram inline keyboards follow one universal schema.  
This builder generates the keyboard **directly in Telegram format** and lets
you pass the result to **any Telegram library** — no adapters, no wrappers,
no framework coupling.

```python
keyboard = builder.build()
# Always returns:
# { "reply_markup": { "inline_keyboard": [[...], [...]] } }
```

---

## Public API

### Constructor

```python
InlineKeyboardBuilder(buttons_per_row: int = 2, auto_wrap_max_chars: int = 0)
```

| Parameter             | Type  | Default | Description                                                         |
| --------------------- | ----- | ------- | ------------------------------------------------------------------- |
| `buttons_per_row`     | `int` | `2`     | Maximum buttons per row. Minimum `1`.                               |
| `auto_wrap_max_chars` | `int` | `0`     | Auto line-break when a row exceeds this char count. `0` = disabled. |

---

### `add_callback_button()`

Adds an inline button that triggers a callback query.

```python
builder.add_callback_button(
    text: str,
    callback_data: str,
    *,
    style: Literal["primary", "danger", "success"] | None = None,
    icon_custom_emoji_id: str | None = None,
) -> InlineKeyboardBuilder
```

```python
builder.add_callback_button("✅ Confirm", "confirm:action")
builder.add_callback_button("🗑 Delete", "delete:42", style="danger")
```

---

### `add_callback_button_from_parts()`

Builds a structured `callback_data` from `scope`, `action`, and `id` — no
manual string concatenation.

```python
builder.add_callback_button_from_parts(
    scope: str,
    action: str,
    id: str | int,
    text: str,
    *,
    style: str | None = None,
    icon_custom_emoji_id: str | None = None,
    separator: str = ":",
) -> InlineKeyboardBuilder
```

```python
builder.add_callback_button_from_parts("post", "like", 101, "👍 Like", style="success")
# callback_data → "post:like:101"
```

---

### `add_url_button()`

Adds an inline button that opens an external URL.

```python
builder.add_url_button(
    text: str,
    url: str,
    *,
    style: str | None = None,
    icon_custom_emoji_id: str | None = None,
) -> InlineKeyboardBuilder
```

```python
builder.add_url_button("📖 Documentation", "https://example.com")
```

---

### `add_pay_button()`

Adds a Telegram payment button. **Must only be used inside `send_invoice`.**

```python
builder.add_pay_button(text: str) -> InlineKeyboardBuilder
```

---

### `add_custom_button()`

Adds a fully custom button dict for Telegram button types not covered by this
library (e.g. `switch_inline_query`).

```python
builder.add_custom_button(button_object: dict) -> InlineKeyboardBuilder
```

```python
builder.add_custom_button({
    "text": "🔔 Share",
    "switch_inline_query": "hello",
})
```

---

### `add_buttons()`

Add multiple buttons at once from a declarative list or grouped config.

```python
# Flat list
builder.add_buttons([
    {"type": "callback", "text": "Yes", "data": "answer:yes"},
    {"type": "callback", "text": "No",  "data": "answer:no"},
])

# Grouped config (shared type)
builder.add_buttons({
    "type": "callback",
    "buttons": [
        {"text": "👍", "data": "vote:up"},
        {"text": "👎", "data": "vote:down"},
    ],
})
```

---

### `callback_data()`

Build a `callback_data` string without adding a button.

```python
data = builder.callback_data("user", "ban", 42)
# → "user:ban:42"
```

---

### `callback_data_parse()`

Decode a `callback_data` string into its parts.  
Useful inside callback handlers or unit tests.

```python
builder.callback_data_parse(data: str, separator: str = ":") -> dict[str, str]
# → {"scope": str, "action": str, "id": str}
```

```python
result = builder.callback_data_parse("post:like:101")
# → {"scope": "post", "action": "like", "id": "101"}
```

Raises `ValueError` if the string has fewer than three parts.

---

### `preview()`

Returns a readable row-by-row representation of the keyboard — handy during
development to verify layout before sending to Telegram.

```python
print(builder.preview())
# Row 1: [👍 Like](callback:post:like:101) | [👎 Dislike](callback:post:dislike:101)
# Row 2: [📖 Docs](https://example.com)
```

---

### `paginated_list()`

Transforms a complete list into a paginated inline keyboard with built-in
navigation controls.

```python
builder.paginated_list(options: PaginatedListOptions) -> InlineKeyboardBuilder
```

#### `PaginatedListOptions`

| Key          | Type                  |          | Description                                      |
| ------------ | --------------------- | -------- | ------------------------------------------------ |
| `items`      | `list[T]`             | required | Complete unsliced list of items.                 |
| `page`       | `int`                 | required | Current page number (starts at `1`).             |
| `per_page`   | `int`                 | required | Items displayed per page.                        |
| `render`     | `Callable[[T], dict]` | required | Maps one item to an `InlineKeyboardButton` dict. |
| `pagination` | `PaginationConfig`    | required | Navigation bar configuration.                    |

#### `PaginationConfig`

| Key                   | Type                   | Default    | Description                                                  |
| --------------------- | ---------------------- | ---------- | ------------------------------------------------------------ |
| `callback`            | `Callable[[int], str]` | required   | Returns `callback_data` for a given page number.             |
| `labels`              | `PaginationLabels`     | —          | Custom labels for navigation buttons.                        |
| `show_edge_buttons`   | `bool`                 | `False`    | Show ⏮ / ⏭ to jump to the first and last page.             |
| `hide_if_single_page` | `bool`                 | `False`    | Hide the navigation bar when `total_pages == 1`.             |
| `counter_callback`    | `str`                  | `"ignore"` | `callback_data` for the central counter button (e.g. `2/5`). |

#### `PaginationLabels`

| Key        | Default | Description                 |
| ---------- | ------- | --------------------------- |
| `previous` | `"⬅️"`  | Previous page button label. |
| `next`     | `"➡️"`  | Next page button label.     |
| `first`    | `"⏮"`  | First page button label.    |
| `last`     | `"⏭"`  | Last page button label.     |

#### Key behaviours

- **Empty list** — returns `self` immediately; nothing is rendered.
- **Page overflow** — page is silently clamped to `total_pages`.
- **Edge navigation** — on page 1 the ⬅️ button shows `·⬅️·` with `callback_data="ignore"`. Same for ➡️ on the last page.
- **Validation** — raises `ValueError` if `items` is not a list or `callback` is not callable.

---

### Layout controls

```python
builder.set_buttons_per_row(n: int)       -> InlineKeyboardBuilder
builder.set_auto_wrap_max_chars(n: int)   -> InlineKeyboardBuilder
```

Both can be called at any point in the chain to change layout for subsequent buttons.

---

### `new_row()`

Force a row break at the current position.

```python
builder.new_row() -> InlineKeyboardBuilder
```

---

### `build()`

Build and return the final Telegram `reply_markup` object.

```python
keyboard = builder.build()
# → {"reply_markup": {"inline_keyboard": [[...], [...]]}}
```

---

## Usage examples

### python-telegram-bot

```python
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from telegram_inline_keyboard_builder import InlineKeyboardBuilder

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = (
        InlineKeyboardBuilder(buttons_per_row=2)
        .add_callback_button("✅ Confirm", "confirm_action", style="success")
        .add_url_button("🌍 Website", "https://example.com")
        .new_row()
        .add_callback_button("❌ Cancel", "cancel_action", style="danger")
        .build()
    )

    await update.message.reply_text(
        "Welcome 👋 Choose an option:",
        reply_markup=keyboard["reply_markup"],
    )
```

---

### Aiogram

```python
from aiogram import Bot, Dispatcher, Router
from aiogram.filters import CommandStart
from aiogram.types import Message, InlineKeyboardMarkup
from telegram_inline_keyboard_builder import InlineKeyboardBuilder

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    raw = (
        InlineKeyboardBuilder(buttons_per_row=2)
        .add_callback_button_from_parts("post", "like",    1, "👍 Like",    style="success")
        .add_callback_button_from_parts("post", "dislike", 1, "👎 Dislike", style="danger")
        .new_row()
        .add_url_button("📖 Docs", "https://example.com")
        .build()
    )
    # Aiogram expects an InlineKeyboardMarkup object
    markup = InlineKeyboardMarkup(inline_keyboard=raw["reply_markup"]["inline_keyboard"])
    await message.answer("Choose:", reply_markup=markup)
```

---

### Paginated product list

```python
from telegram.ext import CallbackQueryHandler
from telegram_inline_keyboard_builder import InlineKeyboardBuilder

async def show_products(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query    = update.callback_query
    page     = int(query.data.split("_")[-1])          # e.g. "products_page_2"
    products = await db.get_all_products()              # full list

    keyboard = (
        InlineKeyboardBuilder()
        .paginated_list({
            "items":    products,
            "page":     page,
            "per_page": 5,
            "render":   lambda p: {
                "text":          f"🛍 {p.name} — {p.price}€",
                "callback_data": f"product_view_{p.id}",
            },
            "pagination": {
                "callback":            lambda p: f"products_page_{p}",
                "hide_if_single_page": True,
            },
        })
        .build()
    )

    await query.edit_message_reply_markup(
        reply_markup=keyboard["reply_markup"]
    )

# Register the handler
app.add_handler(CallbackQueryHandler(show_products, pattern=r"^products_page_\d+$"))
```

```
# Render — page 2/9
[ 🛍 Shoes Nike — 89€   ]
[ 🛍 Adidas Bag — 45€   ]
[ 🛍 Casio Watch — 120€ ]
[ 🛍 Ray-Ban — 99€      ]
[ 🛍 NY Cap — 25€       ]
[  ⬅️  ][  2/9  ][  ➡️  ]
```

---

### Paginated user list with edge buttons

For long lists (100+ items), `show_edge_buttons` lets users jump directly to the first or last page.

```python
async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    page  = int(query.data.split("_")[-1])
    users = await db.get_all_users()

    keyboard = (
        InlineKeyboardBuilder()
        .paginated_list({
            "items":    users,
            "page":     page,
            "per_page": 8,
            "render":   lambda u: {
                "text":          f"👤 {u.username} ({u.role})",
                "callback_data": f"user_info_{u.id}",
            },
            "pagination": {
                "callback":          lambda p: f"users_page_{p}",
                "show_edge_buttons": True,
                "labels": {
                    "previous": "◀️",
                    "next":     "▶️",
                    "first":    "⏮",
                    "last":     "⏭",
                },
            },
        })
        .build()
    )

    await query.edit_message_text(
        "👥 Users",
        reply_markup=keyboard["reply_markup"],
    )

app.add_handler(CallbackQueryHandler(show_users, pattern=r"^users_page_\d+$"))
```

```
# Render — page 1/13, ⏮ and ◀️ are dimmed
[ 👤 alice (admin) ]
[ 👤 bob (user)    ]
...
[ ·⏮· ][ ·◀️· ][ 1/13 ][ ▶️ ][ ⏭ ]
```

---

### Dynamic search results

The search query is encoded directly in `callback_data`.

```python
import re

async def show_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query  = update.callback_query
    match  = re.match(r"^search_(.+)_page_(\d+)$", query.data)
    term   = match.group(1)
    page   = int(match.group(2))
    results = await search(term)

    if not results:
        await query.answer("🚫 No results found")
        return

    keyboard = (
        InlineKeyboardBuilder()
        .paginated_list({
            "items":    results,
            "page":     page,
            "per_page": 4,
            "render":   lambda r: {
                "text":          f"📄 {r.title}",
                "callback_data": f"open_doc_{r.id}",
            },
            "pagination": {
                "callback":            lambda p: f"search_{term}_page_{p}",
                "counter_callback":    f"search_info_{term}",
                "hide_if_single_page": True,
            },
        })
        .build()
    )

    await query.edit_message_text(
        f'🔍 Results for "{term}"',
        reply_markup=keyboard["reply_markup"],
    )

app.add_handler(CallbackQueryHandler(show_search, pattern=r"^search_.+_page_\d+$"))
```

> ⚠️ **Telegram limit:** `callback_data` is capped at **64 bytes**.
> If the search term can be long, store it in the conversation context
> (`context.user_data["query"]`) and encode only an ID in `callback_data`.

---

## Premium button styles

Requires a Telegram Premium subscription for the bot owner.

```python
keyboard = (
    InlineKeyboardBuilder(buttons_per_row=1)
    .add_callback_button("🔵 Primary", "action_1", style="primary")
    .add_callback_button("🟢 Success", "action_2", style="success")
    .add_callback_button("🔴 Danger",  "action_3", style="danger")
    .add_callback_button("Icon only",  "action_4", icon_custom_emoji_id="4963511421280192936")
    .add_callback_button("Icon + style", "action_5",
        style="success",
        icon_custom_emoji_id="4963511421280192936",
    )
    .build()
)
```

> `icon_custom_emoji_id` only works when the bot owner has an active Telegram
> Premium subscription.

---

## Payment buttons

### ⚠️ Telegram limitation

> [!WARNING]
> Payment buttons must only be used with `send_invoice`.
> They must not appear in regular messages.

```python
builder.add_pay_button("💳 Pay now")
```

Using a payment button outside an invoice causes a Telegram API error.

---

## Common errors

### Passing `reply_markup` incorrectly

```python
keyboard = (
    InlineKeyboardBuilder()
    .add_callback_button("⚙️ Settings", "show_settings")
    .build()
)

# ✅ Correct — pass the inner reply_markup value
await update.message.reply_text("Menu:", reply_markup=keyboard["reply_markup"])

# ✅ Also correct — spread into options dict
await update.message.reply_text("Menu:", **{
    "reply_markup": keyboard["reply_markup"],
    "parse_mode": "HTML",
})

# ❌ Wrong — passes the outer wrapper dict
await update.message.reply_text("Menu:", reply_markup=keyboard)
```

---

## Migration to v3

**v3 is fully backward compatible with v2.** Existing code requires no changes.

All new features are opt-in. The constructor signature is unchanged.

| What you did in v2                  | What you can use now (v3)                            |
| ----------------------------------- | ---------------------------------------------------- |
| Manual `callback_data` strings      | `add_callback_button_from_parts(scope, action, id)`  |
| `print(builder.build())` to inspect | `builder.preview()` — row-by-row readable output     |
| Parsing `callback_data` by hand     | `callback_data_parse(data)` → `{scope, action, id}`  |
| Manual pagination + handler code    | `paginated_list({items, page, per_page, render, …})` |

**v3 migration checklist**

- [ ] `pip install telegram-inline-keyboard-builder --upgrade`
- [ ] Replace manual `callback_data` concatenations with `add_callback_button_from_parts()`
- [ ] Replace hand-rolled pagination logic with `paginated_list()`
- [ ] Use `preview()` during development to verify keyboard layout
- [ ] Optionally add type hints using the exported types from `telegram_inline_keyboard_builder.types`

---

## Support this project

This project is maintained in my free time.
If it helped you, consider supporting it with a crypto donation ❤️

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

---

## Contribution

Contributions are welcome ❤️
Please open an issue before proposing major changes.
