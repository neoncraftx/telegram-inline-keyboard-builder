
import { InlineKeyboardBuilder } from "../core/InlineKeyboardBuilder.js";
import { NodeTelegramInlineAdapter } from "../adapters/node-telegram.adapter.js";

export class InlineKeyboardNodeTelegram extends InlineKeyboardBuilder {
	constructor(options = {}) {
		super(
			new NodeTelegramInlineAdapter(),
			options.buttonsPerRow,
			options.autoWrapMaxChars
		);
	}
}