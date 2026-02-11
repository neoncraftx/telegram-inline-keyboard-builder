/**
 * Builder class for creating Telegram inline keyboards with optional
 * custom styles, premium emojis, and automatic layout.
 */
export class InlineKeyboardBuilder {
	/**
	 * Creates a new InlineKeyboardBuilder instance.
	 *
	 * @param {number} [buttonsPerRow=2] - Number of buttons per row.
	 * @param {number} [autoWrapMaxChars=0] - Maximum characters per row before auto-wrapping. 0 = disabled.
	 */
	constructor(buttonsPerRow = 2, autoWrapMaxChars = 0) {
		this.buttonsPerRow = buttonsPerRow;
		this.autoWrapMaxChars = autoWrapMaxChars;
		this._buttons = []; // Flat list of buttons with optional row markers
	}

	// ---------- internal ----------
	/**
	 * Adds a button to the internal list.
	 * @private
	 * @param {object} btn - The button object to push.
	 * @returns {InlineKeyboardBuilder} The instance for chaining.
	 */
	_pushButton(btn) {
		this._buttons.push(btn);
		return this;
	}

	// ---------- button helpers ----------
	/**
	 * Adds a callback button with optional style or emoji.
	 *
	 * @param {string} text - Button text.
	 * @param {string} callback_data - Data sent in callback query.
	 * @param {object} [options] - Optional button options (style, icon_custom_emoji_id).
	 * @param {"primary"|"danger"|"success"} [options.style] - Optional button style.
	 * @param {string} [options.icon_custom_emoji_id] - Optional premium emoji.You need premium account for use this option
	 * @throws {Error} If text or callback_data is missing.
	 * @returns {InlineKeyboardBuilder} The instance for chaining.
	 */
	addCallbackButton(text, callback_data, options = {}) {
		if (!text || !callback_data) {
			throw new Error("Callback button requires text and callback_data");
		}

		const { style, icon_custom_emoji_id } = options;

		if (style && !["primary", "danger", "success"].includes(style)) {
			throw new Error("Invalid style. Allowed: primary, danger, success");
		}

		return this._pushButton({
			text,
			callback_data,
			style,
			icon_custom_emoji_id
		});
	}

	/**
	 * Adds a URL button with optional style or emoji.
	 *
	 * @param {string} text - Button text.
	 * @param {string} url - URL to open.
	 * @param {object} [options] - Optional button options (style, icon_custom_emoji_id).
	 * @param {"primary"|"danger"|"success"} [options.style] - Optional button style.
	 * @param {string} [options.icon_custom_emoji_id] - Optional premium emoji.You need premium account for use this option
	 * @throws {Error} If text or URL is missing.
	 * @returns {InlineKeyboardBuilder} The instance for chaining.
	 */
	addUrlButton(text, url, options = {}) {
		if (!text || !url) {
			throw new Error("URL button requires text and url");
		}

		const { style, icon_custom_emoji_id } = options;

		if (style && !["primary", "danger", "success"].includes(style)) {
			throw new Error("Invalid style. Allowed: primary, danger, success");
		}

		return this._pushButton({ text, url, style, icon_custom_emoji_id });
	}

	/**
	 * Adds a pay button.
	 *
	 * @param {string} text - Button text.
	 * @throws {Error} If text is missing.
	 * @returns {InlineKeyboardBuilder} The instance for chaining.
	 */
	addPayButton(text) {
		if (!text) {
			throw new Error("Pay button requires text");
		}
		return this._pushButton({ text, pay: true });
	}

	/**
	 * Adds a fully custom button object.
	 *
	 * @param {object} buttonObject - Must have at least a `text` property.
	 * @throws {Error} If the button object is invalid.
	 * @returns {InlineKeyboardBuilder} The instance for chaining.
	 */
	addCustomButton(buttonObject) {
		if (!buttonObject || !buttonObject.text) {
			throw new Error(
				"Custom button must be a valid InlineKeyboardButton object"
			);
		}
		return this._pushButton(buttonObject);
	}

	// ---------- layout controls ----------
	/**
	 * Sets the number of buttons per row.
	 * @param {number} n - Must be at least 1.
	 * @returns {InlineKeyboardBuilder} The instance for chaining.
	 */
	setButtonsPerRow(n) {
		this.buttonsPerRow = Math.max(1, Math.floor(n));
		return this;
	}

	/**
	 * Sets the maximum characters per row before auto-wrapping.
	 * @param {number} n - 0 disables auto-wrap.
	 * @returns {InlineKeyboardBuilder} The instance for chaining.
	 */
	setAutoWrapMaxChars(n) {
		this.autoWrapMaxChars = Math.max(0, Math.floor(n));
		return this;
	}

	/**
	 * Forces a new row in the keyboard.
	 * @returns {InlineKeyboardBuilder} The instance for chaining.
	 */
	newRow() {
		this._buttons.push({ __newRow: true });
		return this;
	}

	// ---------- config-based API ----------
	/**
	 * Adds a button from a config object.
	 * @private
	 * @param {object} btn - Button config { type, text, ... }.
	 */
	_addButtonFromConfig(btn) {
		const { type, text } = btn;
		if (!type || !text)
			throw new Error("Button must have at least { type, text }");
		switch (type) {
			case "callback":
				if (!btn.data)
					throw new Error("Callback button requires `data`");
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
				if (!btn.button)
					throw new Error("Custom button requires `button`");
				this.addCustomButton(btn.button);
				break;
			default:
				throw new Error(`Unknown button type: ${type}`);
		}
	}

	/**
	 * Adds multiple buttons from config.
	 * @param {Array|object} config - Array of button configs or grouped config.
	 * @returns {InlineKeyboardBuilder} The instance for chaining.
	 */
	addButtons(config) {
		if (Array.isArray(config)) {
			for (const btn of config) this._addButtonFromConfig(btn);
			return this;
		}
		const { type, buttons } = config;
		if (!type || !Array.isArray(buttons))
			throw new Error("addButtons: invalid config");
		for (const btn of buttons) this._addButtonFromConfig({ type, ...btn });
		return this;
	}

	// ---------- layout engine ----------
	/**
	 * Internal method that lays out buttons into rows based on configuration.
	 * @private
	 * @returns {Array<Array<object>>} Array of rows with buttons.
	 */
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
	/**
	 * Builds the final Telegram reply_markup object.
	 * @returns {object} Telegram inline_keyboard reply_markup.
	 */
	build() {
		return {
			reply_markup: {
				inline_keyboard: this._layoutButtons()
			}
		};
	}
}