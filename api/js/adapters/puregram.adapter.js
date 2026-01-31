import { InlineKeyboard } from "puregram";

export class PuregramInlineAdapter {
	createCallback(text, data) {
		return InlineKeyboard.textButton({ text, payload: data });
	}
	createUrl(text, url) {
		return InlineKeyboard.urlButton({ text, url });
	}
	createPay(text) {
		return InlineKeyboard.payButton({ text });
	}
	buildKeyboard(rows) {
		// maps array of rows of buttons en structure puregram 
		return InlineKeyboard.keyboard(rows.map(r => r.map(btn => btn)));
	}
}
