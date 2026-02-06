class InlineKeyboardBuilder:
    def __init__(self, buttons_per_row: int = 2, auto_wrap_max_chars: int = 0):
        self.buttons_per_row = max(1, int(buttons_per_row))
        self.auto_wrap_max_chars = max(0, int(auto_wrap_max_chars))
        self._buttons = []  # flat list of buttons + row markers

    # ---------- internal ----------
    def _push_button(self, button: dict):
        self._buttons.append(button)
        return self

    # ---------- button helpers ----------
    def add_callback_button(self, text: str, callback_data: str):
        if not text or not callback_data:
            raise ValueError("Callback button requires text and callback_data")

        return self._push_button({
            "text": text,
            "callback_data": callback_data
        })

    def add_url_button(self, text: str, url: str):
        if not text or not url:
            raise ValueError("URL button requires text and url")

        return self._push_button({
            "text": text,
            "url": url
        })

    def add_pay_button(self, text: str):
        if not text:
            raise ValueError("Pay button requires text")

        return self._push_button({
            "text": text,
            "pay": True
        })

    def add_custom_button(self, button_object: dict):
        if not button_object or "text" not in button_object:
            raise ValueError("Custom button must be a valid InlineKeyboardButton object")

        return self._push_button(button_object)

    # ---------- layout controls ----------
    def set_buttons_per_row(self, n: int):
        self.buttons_per_row = max(1, int(n))
        return self

    def set_auto_wrap_max_chars(self, n: int):
        self.auto_wrap_max_chars = max(0, int(n))
        return self

    def new_row(self):
        self._buttons.append({"__newRow": True})
        return self

    # ---------- config-based API ----------
    def _add_button_from_config(self, btn: dict):
        button_type = btn.get("type")
        text = btn.get("text")

        if not button_type or not text:
            raise ValueError("Button must have at least { type, text }")

        if button_type == "callback":
            if "data" not in btn:
                raise ValueError("Callback button requires `data`")
            self.add_callback_button(text, btn["data"])

        elif button_type == "url":
            if "url" not in btn:
                raise ValueError("URL button requires `url`")
            self.add_url_button(text, btn["url"])

        elif button_type == "pay":
            self.add_pay_button(text)

        elif button_type == "custom":
            if "button" not in btn:
                raise ValueError("Custom button requires `button`")
            self.add_custom_button(btn["button"])

        else:
            raise ValueError(f"Unknown button type: {button_type}")

    def add_buttons(self, config):
        # Case 1: list of buttons
        if isinstance(config, list):
            for btn in config:
                self._add_button_from_config(btn)
            return self

        # Case 2: grouped config
        button_type = config.get("type")
        buttons = config.get("buttons")

        if not button_type or not isinstance(buttons, list):
            raise ValueError("add_buttons: invalid config")

        for btn in buttons:
            merged = {"type": button_type, **btn}
            self._add_button_from_config(merged)

        return self

    # ---------- layout engine ----------
    def _layout_buttons(self):
        rows = []
        row = []
        row_chars = 0

        def push_row():
            nonlocal row, row_chars
            if row:
                rows.append(row)
                row = []
                row_chars = 0

        for b in self._buttons:
            if "__newRow" in b:
                push_row()
                continue

            text_length = len(str(b.get("text", "")))

            if (
                self.auto_wrap_max_chars > 0
                and row
                and row_chars + text_length > self.auto_wrap_max_chars
            ):
                push_row()

            if len(row) >= self.buttons_per_row:
                push_row()

            row.append(b)
            row_chars += text_length

        push_row()
        return rows

    # ---------- final output ----------
    def build(self):
        return {
            "reply_markup": {
                "inline_keyboard": self._layout_buttons()
            }
        }