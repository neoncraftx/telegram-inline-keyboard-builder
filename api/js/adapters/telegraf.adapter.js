import { Markup } from "telegraf";

export class TelegrafInlineAdapter {
	createCallback(text, data, hide = false) {
		return Markup.button.callback(text, data, hide);
	}

	createUrl(text, url, hide = false) {
		return Markup.button.url(text, url, hide);
	}

	createPay(text, hide = false) {
		return Markup.button.pay(text, hide);
	}

	buildKeyboard(rows) {
		return Markup.inlineKeyboard(rows);
	}
}