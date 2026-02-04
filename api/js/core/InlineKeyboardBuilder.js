
export class InlineKeyboardBuilder {
  constructor(buttonsPerRow = 2, autoWrapMaxChars = 0) {
    this.buttonsPerRow = buttonsPerRow;
    this.autoWrapMaxChars = autoWrapMaxChars; // 0 = disabled
    this._buttons = []; // flat list of buttons + row markers
  }

  // ---------- internal ----------
  _pushButton(btn) {
    this._buttons.push(btn);
    return this;
  }

  // ---------- button helpers ----------
  addCallbackButton(text, callback_data) {
    if (!text || !callback_data) {
      throw new Error("Callback button requires text and callback_data");
    }

    return this._pushButton({
      text,
      callback_data,
    });
  }

  addUrlButton(text, url) {
    if (!text || !url) {
      throw new Error("URL button requires text and url");
    }

    return this._pushButton({
      text,
      url,
    });
  }

  addPayButton(text) {
    if (!text) {
      throw new Error("Pay button requires text");
    }

    return this._pushButton({
      text,
      pay: true,
    });
  }

  addCustomButton(buttonObject) {
    if (!buttonObject || !buttonObject.text) {
      throw new Error("Custom button must be a valid InlineKeyboardButton object");
    }

    return this._pushButton(buttonObject);
  }

  // ---------- layout controls ----------
  setButtonsPerRow(n) {
    this.buttonsPerRow = Math.max(1, Math.floor(n));
    return this;
  }

  setAutoWrapMaxChars(n) {
    this.autoWrapMaxChars = Math.max(0, Math.floor(n));
    return this;
  }

  newRow() {
    this._buttons.push({ __newRow: true });
    return this;
  }

  // ---------- config-based API ----------
  _addButtonFromConfig(btn) {
    const { type, text } = btn;

    if (!type || !text) {
      throw new Error("Button must have at least { type, text }");
    }

    switch (type) {
      case "callback":
        if (!btn.data) throw new Error("Callback button requires `data`");
        this.addCallbackButton(text, btn.data);
        break;

      case "url":
        if (!btn.url) throw new Error("URL button requires `url`");
        this.addUrlButton(text, btn.url);
        break;

      case "pay":
        this.addPayButton(text);
        break;

      case "custom":
        if (!btn.button) throw new Error("Custom button requires `button`");
        this.addCustomButton(btn.button);
        break;

      default:
        throw new Error(`Unknown button type: ${type}`);
    }
  }

  addButtons(config) {
    // Case 1: array of buttons
    if (Array.isArray(config)) {
      for (const btn of config) {
        this._addButtonFromConfig(btn);
      }
      return this;
    }

    // Case 2: grouped config
    const { type, buttons } = config;
    if (!type || !Array.isArray(buttons)) {
      throw new Error("addButtons: invalid config");
    }

    for (const btn of buttons) {
      this._addButtonFromConfig({ type, ...btn });
    }

    return this;
  }

  // ---------- layout engine ----------
  _layoutButtons() {
    const rows = [];
    let row = [];
    let rowChars = 0;

    const pushRow = () => {
      if (row.length > 0) {
        rows.push(row);
        row = [];
        rowChars = 0;
      }
    };

    for (const b of this._buttons) {
      if (b.__newRow) {
        pushRow();
        continue;
      }

      const textLength = String(b.text || "").length;

      if (
        this.autoWrapMaxChars > 0 &&
        row.length > 0 &&
        rowChars + textLength > this.autoWrapMaxChars
      ) {
        pushRow();
      }

      if (row.length >= this.buttonsPerRow) {
        pushRow();
      }

      row.push(b);
      rowChars += textLength;
    }

    pushRow();
    return rows;
  }

  // ---------- final output ----------
  build() {
    return {
      reply_markup: {
        inline_keyboard: this._layoutButtons(),
      },
    };
  }
}