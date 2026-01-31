import { InlineKeyboardBuilder } from "../core/InlineKeyboardBuilder.js";
import { TelegrafInlineAdapter } from "../adapters/telegraf.adapter.js";

export class InlineKeyboardTelegraf extends InlineKeyboardBuilder {
	constructor(options = {}) {
		super(
			new TelegrafInlineAdapter(),
			options.buttonsPerRow,
			options.autoWrapMaxChars
		);
	}
}