class InlineKeyboardBuilder:
    def __init__(self, adapter, buttons_per_row=2, auto_wrap_max_chars=0):
        if adapter is None:
            raise ValueError("Adapter is required")

        self.adapter = adapter
        self.buttons_per_row = buttons_per_row
        self.auto_wrap_max_chars = auto_wrap_max_chars
        self._buttons = []

    def _push(self, btn):
        self._buttons.append(btn)
        return self

    def add_callback_button(self, text, data, hide=False):
        return self._push(self.adapter.create_callback(text, data, hide))

    def add_url_button(self, text, url, hide=False):
        return self._push(self.adapter.create_url(text, url, hide))

    def add_pay_button(self, text, hide=False):
        return self._push(self.adapter.create_pay(text, hide))

    def add_custom_button(self, btn):
        return self._push(btn)

    def new_row(self):
        self._buttons.append({"__new_row": True})
        return self

    def _layout(self):
        rows = []
        row = []
        row_chars = 0

        def push_row():
            nonlocal row, row_chars
            if row:
                rows.append(row)
                row = []
                row_chars = 0

        for btn in self._buttons:
            if isinstance(btn, dict) and btn.get("__new_row"):
                push_row()
                continue

            text = getattr(btn, "text", "") or btn.get("text", "")
            length = len(str(text))

            if (
                self.auto_wrap_max_chars > 0
                and row
                and row_chars + length > self.auto_wrap_max_chars
            ):
                push_row()

            if len(row) >= self.buttons_per_row:
                push_row()

            row.append(btn)
            row_chars += length

        push_row()
        return rows

    def build(self):
        rows = self._layout()
        return self.adapter.build_keyboard(rows)