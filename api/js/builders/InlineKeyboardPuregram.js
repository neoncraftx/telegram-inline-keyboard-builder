import { InlineKeyboardBuilder } from "../core/InlineKeyboardBuilder.js";
import { PuregramInlineAdapter } from "../adapters/puregram.adapter.js";

export class InlineKeyboardPuregram extends InlineKeyboardBuilder {
	constructor(options = {}) {
		super(
			new PuregramInlineAdapter(),
			options.buttonsPerRow,
			options.autoWrapMaxChars
		);
	}
}