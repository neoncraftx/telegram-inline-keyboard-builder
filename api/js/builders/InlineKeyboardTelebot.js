import { InlineKeyboardBuilder } from "../core/InlineKeyboardBuilder.js";
import { TelebotInlineAdapter } from "../adapters/telebot.adapter.js";

export class InlineKeyboardTelebot extends InlineKeyboardBuilder {
	constructor(options = {}) {
		super(
			new TelebotInlineAdapter(),
			options.buttonsPerRow,
			options.autoWrapMaxChars
		);
	}
}