export class NodeTelegramInlineAdapter {
	createCallback(text, data) {
		return { text, callback_data: data };
	}

	createUrl(text, url) {
		return { text, url };
	}

	createPay(text) {
		return { text, pay: true };
	}

	buildKeyboard(rows) {
		return {
			reply_markup: {
				inline_keyboard: rows
			}
		};
	}
}