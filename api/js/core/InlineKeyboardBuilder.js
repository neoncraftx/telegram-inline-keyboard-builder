export class InlineKeyboardBuilder {
	constructor(adapter, buttonsPerRow = 2, autoWrapMaxChars = 0) {
		if (!adapter) {
			throw new Error("InlineKeyboardBuilder requires an adapter");
		}
		this.adapter = adapter;
		this.buttonsPerRow = buttonsPerRow;
		this.autoWrapMaxChars = autoWrapMaxChars;
		this._buttons = [];
	}

	_pushButton(btn) {
		this._buttons.push(btn);
		return this;
	}

	addCallbackButton(text, callback_data, hide = false) {
		return this._pushButton(
			this.adapter.createCallback(text, callback_data, hide)
		);
	}

	addUrlButton(text, url, hide = false) {
		return this._pushButton(
			this.adapter.createUrl(text, url, hide)
		);
	}

	addPayButton(text, options = {}) {
		const hide = options.hide ?? false;
		return this._pushButton(
			this.adapter.createPay(text, hide)
		);
	}

	addCustomButton(btnObj) {
		return this._pushButton(btnObj);
	}

	newRow() {
		this._buttons.push({ __newRow: true });
		return this;
	}
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
			if (b && b.__newRow) {
				pushRow();
				continue;
			}

			const text = b?.text || "";
			const len = String(text).length || 0;

			if (
				this.autoWrapMaxChars > 0 &&
				row.length > 0 &&
				rowChars + len > this.autoWrapMaxChars
			) {
				pushRow();
			}

			if (row.length >= this.buttonsPerRow) {
				pushRow();
			}

			row.push(b);
			rowChars += len;
		}

		pushRow();
		return rows;
	}

	build() {
		return this.adapter.buildKeyboard(this._layoutButtons());
	}
}