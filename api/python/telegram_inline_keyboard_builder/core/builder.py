"""
Core builder module — InlineKeyboardBuilder.

Produces pure Telegram Bot API compliant JSON usable with any Python
Telegram library (python-telegram-bot, Aiogram, Pyrogram, Telebot…).
"""

from __future__ import annotations
from typing import Union, TypeVar

from .types.buttons import (
    ButtonStyle,
    ButtonConfig,
    GroupedButtonConfig,
    InlineKeyboardButton,
    CallbackButton,
    UrlButton,
    PayButton
)
from .types.utils import PaginatedListOptions
from .layout import layout_buttons
from ..validator import ValidationEngine, ValidationError
from ..validator.types import (
    DiagnosticSeverity,
    KeyboardInput,
    RulesConfig,
    ValidateOptions,
    ValidationContextType,
    ValidationMode,
    ValidationPlugin,
    ValidationResult,
    ValidationRule,
)

T = TypeVar("T")

_VALID_STYLES: frozenset[ButtonStyle] = frozenset({"primary", "danger", "success"})


class InlineKeyboardBuilder:
    """
    Fluent builder for Telegram inline keyboards.

    Produces a ``reply_markup`` dict fully compliant with the Telegram Bot API,
    passable directly to any Python Telegram library.

    Args:
        buttons_per_row:    Maximum buttons per row. Minimum ``1``. Default ``2``.
        auto_wrap_max_chars: Auto line-break when a row exceeds this character
                            count. ``0`` disables auto-wrap. Default ``0``.

    Example::

        from telegram_inline_keyboard_builder import InlineKeyboardBuilder

        keyboard = (
            InlineKeyboardBuilder(buttons_per_row=2)
            .add_callback_button("✅ OK",     "ok_action")
            .add_url_button("🌍 Website", "https://example.com")
            .new_row()
            .add_callback_button("❌ Cancel", "cancel_action")
            .build()
        )
    """

    # ------------------------------------------------------------------
    # Construction
    # ------------------------------------------------------------------

    def __init__(
        self,
        buttons_per_row: int = 2,
        auto_wrap_max_chars: int = 0,
    ) -> None:
        self.buttons_per_row: int    = max(1, int(buttons_per_row))
        self.auto_wrap_max_chars: int = max(0, int(auto_wrap_max_chars))
        self._buttons: list[InlineKeyboardButton] = []
        self._validation = ValidationEngine()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _push_button(self, button: InlineKeyboardButton) -> "InlineKeyboardBuilder":
        """Append a button to the internal flat list."""
        self._buttons.append(button)
        return self

    @staticmethod
    def _validate_style(style: str | None) -> None:
        """Raise ValueError if *style* is set but not a recognized value."""
        if style and style not in _VALID_STYLES:
            raise ValueError(
                f"Invalid style '{style}'. Allowed: {', '.join(sorted(_VALID_STYLES))}"
            )

    # ------------------------------------------------------------------
    # Button helpers
    # ------------------------------------------------------------------

    def add_callback_button(
        self,
        text: str,
        callback_data: str,
        *,
        style: ButtonStyle | None = None,
        icon_custom_emoji_id: str | None = None,
    ) -> "InlineKeyboardBuilder":
        """
        Add an inline button that triggers a callback query.

        Args:
            text:                 Label displayed on the button.
            callback_data:        Data sent in the callback query (max 64 bytes).
            style:                Optional premium button colour
                                  (``"primary"``, ``"danger"``, ``"success"``).
            icon_custom_emoji_id: Optional premium emoji icon (requires bot-owner
                                  Telegram Premium subscription).

        Raises:
            ValueError: If *text* or *callback_data* is empty.
            ValueError: If *style* is not a recognised value.

        Returns:
            The builder instance for chaining.

        Example::

            builder.add_callback_button("👍 Like", "post:like:42", style="success")
        """
        if not text or not callback_data:
            raise ValueError("Callback button requires text and callback_data")
        self._validate_style(style)

        btn: CallbackButton = {"text": text, "callback_data": callback_data}
        if style:
            btn["style"] = style
        if icon_custom_emoji_id:
            btn["icon_custom_emoji_id"] = icon_custom_emoji_id

        return self._push_button(btn)

    def add_callback_button_from_parts(
        self,
        scope: str,
        action: str,
        id: str | int,
        text: str,
        *,
        style: ButtonStyle | None = None,
        icon_custom_emoji_id: str | None = None,
        separator: str = ":",
    ) -> "InlineKeyboardBuilder":
        """
        Build a structured ``callback_data`` from parts and add the button.

        Eliminates manual string concatenation and reduces typos in
        ``callback_data`` strings.

        Args:
            scope:                Functional domain (e.g. ``"user"``, ``"product"``).
            action:               Action to perform (e.g. ``"like"``, ``"delete"``).
            id:                   Resource identifier.
            text:                 Label displayed on the button.
            style:                Optional premium button colour.
            icon_custom_emoji_id: Optional premium emoji icon.
            separator:            Separator between parts. Default ``":"``.

        Returns:
            The builder instance for chaining.

        Example::

            builder.add_callback_button_from_parts("post", "like", 101, "👍 Like")
            # callback_data → "post:like:101"
        """
        callback_data = f"{scope}{separator}{action}{separator}{id}"
        return self.add_callback_button(
            text,
            callback_data,
            style=style,
            icon_custom_emoji_id=icon_custom_emoji_id,
        )

    def add_url_button(
        self,
        text: str,
        url: str,
        *,
        style: ButtonStyle | None = None,
        icon_custom_emoji_id: str | None = None,
    ) -> "InlineKeyboardBuilder":
        """
        Add an inline button that opens an external URL.

        Args:
            text:                 Label displayed on the button.
            url:                  URL to open when the button is pressed.
            style:                Optional premium button colour.
            icon_custom_emoji_id: Optional premium emoji icon.

        Raises:
            ValueError: If *text* or *url* is empty.

        Returns:
            The builder instance for chaining.

        Example::

            builder.add_url_button("📖 Docs", "https://example.com")
        """
        if not text or not url:
            raise ValueError("URL button requires text and url")
        self._validate_style(style)

        btn: UrlButton = {"text": text, "url": url}
        if style:
            btn["style"] = style
        if icon_custom_emoji_id:
            btn["icon_custom_emoji_id"] = icon_custom_emoji_id

        return self._push_button(btn)

    def add_pay_button(self, text: str) -> "InlineKeyboardBuilder":
        """
        Add a Telegram payment button.

        .. warning::
            Must only be used inside ``send_invoice`` / ``reply_with_invoice``.
            Using it in regular messages causes a Telegram API error.

        Args:
            text: Label displayed on the button.

        Raises:
            ValueError: If *text* is empty.

        Returns:
            The builder instance for chaining.
        """
        if not text:
            raise ValueError("Pay button requires text")
        btn: PayButton = {"text": text, "pay": True}
        return self._push_button(btn)

    def add_custom_button(
        self, button_object: InlineKeyboardButton
    ) -> "InlineKeyboardBuilder":
        """
        Add a fully custom button dict.

        Use for Telegram button types not explicitly covered by this library
        (e.g. ``switch_inline_query``, ``switch_inline_query_current_chat``).

        Args:
            button_object: A valid ``InlineKeyboardButton`` dict with at least
                           a ``"text"`` key.

        Raises:
            ValueError: If *button_object* is ``None`` or missing ``"text"``.

        Returns:
            The builder instance for chaining.

        Example::

            builder.add_custom_button({
                "text": "🔔 Share",
                "switch_inline_query": "hello",
            })
        """
        if not button_object or "text" not in button_object:
            raise ValueError(
                "Custom button must be a valid InlineKeyboardButton with at least 'text'"
            )
        return self._push_button(button_object)

    # ------------------------------------------------------------------
    # Layout controls
    # ------------------------------------------------------------------

    def set_buttons_per_row(self, n: int) -> "InlineKeyboardBuilder":
        """
        Change the maximum number of buttons per row at any point in the chain.

        Args:
            n: Must be at least ``1``.

        Returns:
            The builder instance for chaining.
        """
        self.buttons_per_row = max(1, int(n))
        return self

    def set_auto_wrap_max_chars(self, n: int) -> "InlineKeyboardBuilder":
        """
        Change the auto-wrap character threshold at any point in the chain.

        Args:
            n: ``0`` disables auto-wrap.

        Returns:
            The builder instance for chaining.
        """
        self.auto_wrap_max_chars = max(0, int(n))
        return self

    def new_row(self) -> "InlineKeyboardBuilder":
        """
        Force a row break in the keyboard at the current position.

        Returns:
            The builder instance for chaining.

        Example::

            builder
                .add_callback_button("A", "a")
                .add_callback_button("B", "b")
                .new_row()
                .add_callback_button("C", "c")   # starts a new row
        """
        self._buttons.append({"__newRow": True})  # type: ignore[arg-type]
        return self

    # ------------------------------------------------------------------
    # Config-based API
    # ------------------------------------------------------------------

    def _add_button_from_config(self, btn: ButtonConfig) -> None:
        """Process a single ButtonConfig dict and dispatch to the right method."""
        btn_type = btn.get("type")
        text = btn.get("text")

        if not btn_type or not text:
            raise ValueError("Button config must have at least { type, text }")

        if btn_type == "callback":
            data = btn.get("data")
            if not data:
                raise ValueError("Callback button config requires 'data'")
            self.add_callback_button(text, data)

        elif btn_type == "url":
            url = btn.get("url")
            if not url:
                raise ValueError("URL button config requires 'url'")
            self.add_url_button(text, url)

        elif btn_type == "pay":
            self.add_pay_button(text)

        elif btn_type == "custom":
            button = btn.get("button")
            if not button:
                raise ValueError("Custom button config requires 'button'")
            self.add_custom_button(button)

        else:
            raise ValueError(f"Unknown button type: '{btn_type}'")

    def add_buttons(
        self,
        config: Union[list[ButtonConfig], GroupedButtonConfig],
    ) -> "InlineKeyboardBuilder":
        """
        Add multiple buttons from a declarative configuration.

        Accepts either a flat list of :class:`~types.buttons.ButtonConfig`
        dicts, or a single :class:`~types.buttons.GroupedButtonConfig` that
        shares a ``type`` across all its buttons.

        Args:
            config: List of button configs, or a grouped config object.

        Returns:
            The builder instance for chaining.

        Example — flat list::

            builder.add_buttons([
                {"type": "callback", "text": "Yes", "data": "answer:yes"},
                {"type": "callback", "text": "No",  "data": "answer:no"},
            ])

        Example — grouped config::

            builder.add_buttons({
                "type": "callback",
                "buttons": [
                    {"text": "👍", "data": "vote:up"},
                    {"text": "👎", "data": "vote:down"},
                ],
            })
        """
        if isinstance(config, list):
            for btn in config:
                self._add_button_from_config(btn)
            return self

        btn_type = config.get("type")
        buttons  = config.get("buttons")
        
        if not btn_type or type(buttons) != list:
            raise ValueError("add_buttons: invalid grouped config")

        for btn in buttons:
            merged: ButtonConfig = {"type": btn_type, **btn}  # type: ignore[misc]
            self._add_button_from_config(merged)

        return self

    # ------------------------------------------------------------------
    # Callback data helpers
    # ------------------------------------------------------------------

    def callback_data(
        self,
        scope: str,
        action: str,
        id: str | int,
        separator: str = ":",
    ) -> str:
        """
        Build a structured ``callback_data`` string from parts.

        Args:
            scope:     Functional domain.
            action:    Action identifier.
            id:        Resource identifier.
            separator: Separator between parts. Default ``":"``.

        Returns:
            A ``callback_data`` string, e.g. ``"user:like:42"``.

        Example::

            data = builder.callback_data("user", "like", 42)
            # → "user:like:42"
        """
        return f"{scope}{separator}{action}{separator}{id}"

    def callback_data_parse(
        self,
        data: str,
        separator: str = ":",
    ) -> dict[str, str]:
        """
        Decode a ``callback_data`` string into its component parts.

        Args:
            data:      The ``callback_data`` string to decode.
            separator: Separator used during encoding. Default ``":"``.

        Raises:
            ValueError: If *data* does not contain at least three parts.

        Returns:
            A dict with keys ``scope``, ``action``, and ``id``.

        Example::

            result = builder.callback_data_parse("post:like:101")
            # → {"scope": "post", "action": "like", "id": "101"}
        """
        parts = data.split(separator)
        if len(parts) < 3:
            raise ValueError(
                f"Invalid callback_data format: '{data}' "
                f"(expected at least 3 parts separated by '{separator}')"
            )
        scope, action, *id_parts = parts
        return {"scope": scope, "action": action, "id": separator.join(id_parts)}

    # ------------------------------------------------------------------
    # Preview
    # ------------------------------------------------------------------

    def preview(self) -> str:
        """
        Return a human-readable representation of the current keyboard layout.

        Each row is printed on its own line, prefixed with its index.
        Useful during development to verify layout before sending to Telegram.

        Returns:
            A multi-line string, or ``"No buttons added"`` if empty.

        Example::

            print(builder.preview())
            # Row 1: [👍 Like](callback:post:like:101) | [👎 Dislike](callback:post:dislike:101)
            # Row 2: [📖 Docs](https://example.com)
        """
        button_rows = self._layout_buttons()

        if not button_rows:
            return "No buttons added"

        lines: list[str] = []
        for row_index, row in enumerate(button_rows, start=1):
            parts: list[str] = []
            for btn in row:
                if "callback_data" in btn:
                    parts.append(f"[{btn['text']}](callback:{btn['callback_data']})")
                elif "url" in btn:
                    parts.append(f"[{btn['text']}]({btn['url']})")
                elif btn.get("pay"):
                    parts.append(f"[{btn['text']}](pay)")
                else:
                    parts.append(f"[{btn['text']}](custom)")
            lines.append(f"Row {row_index}: {' | '.join(parts)}")

        return "\n".join(lines)

    # ------------------------------------------------------------------
    # Paginated list
    # ------------------------------------------------------------------

    def paginated_list(self, options: PaginatedListOptions[T]) -> "InlineKeyboardBuilder":
        """
        Render a paginated list of items as inline keyboard buttons with
        automatic navigation controls.

        Each item is rendered on its own row using the provided *render*
        function.  A navigation bar (previous / counter / next) is appended
        below the items.

        Args:
            options: A :class:`~types.utils.PaginatedListOptions` dict.

        Raises:
            ValueError: If ``items`` is not a list.
            ValueError: If ``pagination.callback`` is not callable.

        Returns:
            The builder instance for chaining.

        Behaviour highlights:

        - **Empty list** — returns ``self`` immediately, nothing is rendered.
        - **Page overflow** — page is silently clamped to ``total_pages``.
        - **Edge buttons** — on page 1 the ⬅️ button shows ``·⬅️·`` with
          ``callback_data="ignore"``. Same for ➡️ on the last page.
        - **Single page** — navigation bar is hidden when
          ``hide_if_single_page=True``.

        Example::

            keyboard = (
                InlineKeyboardBuilder()
                .paginated_list({
                    "items":    products,
                    "page":     current_page,
                    "per_page": 5,
                    "render":   lambda p: {
                        "text":          f"🛍 {p.name} — {p.price}€",
                        "callback_data": f"product_{p.id}",
                    },
                    "pagination": {
                        "callback":            lambda p: f"products_page_{p}",
                        "hide_if_single_page": True,
                    },
                })
                .build()
            )
        """
        items      = options["items"]
        page       = options["page"]
        per_page   = options["per_page"]
        render     = options["render"]
        pagination = options["pagination"]

        # ── Validation ──────────────────────────────────────────────
        if type(items) != list:
            raise ValueError("paginated_list: 'items' must be a list")

        callback = pagination.get("callback")
        if not callable(callback):
            raise ValueError("paginated_list: 'pagination.callback' must be callable")

        # ── Calculations ─────────────────────────────────────────────
        current_page = max(1, int(page))
        per          = max(1, int(per_page) or 1)
        total_pages  = max(1, -(-len(items) // per))          # ceiling division
        safe_page    = min(current_page, total_pages)
        start        = (safe_page - 1) * per
        page_items   = items[start : start + per]

        # ── Empty guard ───────────────────────────────────────────────
        if not page_items:
            return self

        # ── Render items ─────────────────────────────────────────────
        for item in page_items:
            self._push_button(render(item))
            self.new_row()

        # ── Pagination state ─────────────────────────────────────────
        is_first = safe_page == 1
        is_last  = safe_page == total_pages

        if total_pages == 1 and pagination.get("hide_if_single_page"):
            return self

        # ── Labels ───────────────────────────────────────────────────
        labels     = pagination.get("labels") or {}
        prev_label  = labels.get("previous", "⬅️")
        next_label  = labels.get("next",     "➡️")
        first_label = labels.get("first",    "⏮")
        last_label  = labels.get("last",     "⏭")
        counter_cb  = pagination.get("counter_callback", "ignore")

        # ── Navigation row ────────────────────────────────────────────
        self.new_row()

        if pagination.get("show_edge_buttons"):
            self.add_callback_button(
                f"·{first_label}·" if is_first else first_label,
                "ignore" if is_first else callback(1),
            )

        self.add_callback_button(
            f"·{prev_label}·" if is_first else prev_label,
            "ignore" if is_first else callback(safe_page - 1),
        )

        self.add_callback_button(f"{safe_page}/{total_pages}", counter_cb)

        self.add_callback_button(
            f"·{next_label}·" if is_last else next_label,
            "ignore" if is_last else callback(safe_page + 1),
        )

        if pagination.get("show_edge_buttons"):
            self.add_callback_button(
                f"·{last_label}·" if is_last else last_label,
                "ignore" if is_last else callback(total_pages),
            )

        self.new_row()
        return self

    # ------------------------------------------------------------------
    # Layout engine
    # ------------------------------------------------------------------

    def _layout_buttons(self) -> list[list[InlineKeyboardButton]]:
        """
        Arrange the internal flat button list into rows.

        Respects :attr:`buttons_per_row`, :attr:`auto_wrap_max_chars`,
        and explicit ``new_row()`` markers.

        Returns:
            A 2-D list of button dicts (rows → buttons).
        """
        return layout_buttons(
            self._buttons,
            self.buttons_per_row,
            self.auto_wrap_max_chars,
        )

    # ------------------------------------------------------------------
    # Validation (v3.2.3)
    # ------------------------------------------------------------------

    def validate(self, options: ValidateOptions | None = None) -> ValidationResult:
        """Run all enabled validation rules against the current keyboard state."""
        return self._validation.validate(self._keyboard_input(), options)

    def register_rule(self, rule: ValidationRule) -> "InlineKeyboardBuilder":
        self._validation.register_rule(rule)
        return self

    def use(self, plugin: ValidationPlugin) -> "InlineKeyboardBuilder":
        self._validation.use(plugin)
        return self

    def set_rules(self, config: RulesConfig) -> "InlineKeyboardBuilder":
        self._validation.set_rules(config)
        return self

    def set_rule_enabled(
        self, rule_id: str, enabled: bool
    ) -> "InlineKeyboardBuilder":
        self._validation.set_rule_enabled(rule_id, enabled)
        return self

    def set_rule_severity(
        self, rule_id: str, severity: DiagnosticSeverity
    ) -> "InlineKeyboardBuilder":
        self._validation.set_rule_severity(rule_id, severity)
        return self

    def set_validation_mode(self, mode: ValidationMode) -> "InlineKeyboardBuilder":
        self._validation.set_default_mode(mode)
        return self

    def set_validation_context(
        self, context_type: ValidationContextType
    ) -> "InlineKeyboardBuilder":
        self._validation.set_context_type(context_type)
        return self

    def _keyboard_input(self) -> KeyboardInput:
        return {
            "buttons": self._buttons,
            "buttons_per_row": self.buttons_per_row,
            "auto_wrap_max_chars": self.auto_wrap_max_chars,
        }

    def _apply_validation_on_build(
        self,
        *,
        validate: bool,
        validation_mode: ValidationMode | None,
    ) -> ValidationResult | None:
        if not validate:
            return None
        opts: ValidateOptions = {}
        if validation_mode is not None:
            opts["mode"] = validation_mode
        result = self.validate(opts)
        if result["mode"] == "strict" and not result["ok"]:
            raise ValidationError(result)
        return result

    # ------------------------------------------------------------------
    # Final output
    # ------------------------------------------------------------------

    def build(
        self,
        *,
        validate: bool = False,
        validation_mode: ValidationMode | None = None,
    ) -> dict[str, dict[str, list[list[InlineKeyboardButton]]]]:
        """
        Build and return the final Telegram ``reply_markup`` object.

        Args:
            validate:           When ``True``, run validation before returning markup.
            validation_mode:    ``strict`` raises :class:`ValidationError` on errors;
                                ``warn`` / ``silent`` never raise.

        Returns:
            A dict of the form ``{"reply_markup": {"inline_keyboard": [...]}}``
            fully compliant with the Telegram Bot API.

        Example::

            keyboard = builder.build()
            await message.reply("Choose:", reply_markup=keyboard["reply_markup"])

            keyboard = builder.build(validate=True, validation_mode="strict")
        """
        self._apply_validation_on_build(
            validate=validate,
            validation_mode=validation_mode,
        )
        return {
            "reply_markup": {
                "inline_keyboard": self._layout_buttons(),
            }
        }
