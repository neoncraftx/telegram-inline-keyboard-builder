import { layoutButtons } from "./layout.js";
import type {
  InlineKeyboardButton,
  buttonConfig,
  customStyleButton,
  groupedButtonConfig,
} from "./types/buttons.js";
import type { PaginatedListOptions } from "./types/utils.js";
import {
  ValidationEngine,
  ValidationError,
  type BuildOptions,
  type DiagnosticSeverity,
  type RulesConfig,
  type ValidateOptions,
  type ValidationMode,
  type ValidationPlugin,
  type ValidationResult,
  type ValidationRule,
} from "./validator/index.js";

/**
 * Builder class for creating Telegram inline keyboards with optional
 * custom styles, premium emojis, and automatic layout.
 */
export class InlineKeyboardBuilder {
  /** Number of buttons per row. */
  buttonsPerRow: number;
  /** Maximum characters per row before auto-wrapping. 0 = disabled. */
  autoWrapMaxChars: number;
  /** Flat list of buttons with optional row markers. */
  buttons: InlineKeyboardButton[];
  /** Validation engine (rules, plugins, modes). */
  private readonly _validation: ValidationEngine;
  /**
   * Creates a new InlineKeyboardBuilder instance.
   *
   * @param  buttonsPerRow - Number of buttons per row. default is 2. Minimum is 1.
   * @param autoWrapMaxChars- Maximum characters per row before auto-wrapping. 0 = disabled.
   */
  constructor(buttonsPerRow = 2, autoWrapMaxChars = 0) {
    this.buttonsPerRow = buttonsPerRow;
    this.autoWrapMaxChars = autoWrapMaxChars;
    this.buttons = []; // Flat list of buttons with optional row markers
    this._validation = new ValidationEngine();
  }

  // ---------- internal ----------
  /**
   * Adds a button to the internal list.
   * @param btn - The button object to push.
   */
  private _pushButton(btn: InlineKeyboardButton): InlineKeyboardBuilder {
    this.buttons.push(btn);
    return this;
  }

  // ---------- button helpers ----------
  /**
   * Adds a callback button with optional style or emoji.
   *
   * @param text - Button text.
   * @param callback_data - Data sent in callback query.
   * @param options - Optional button options (style, icon_custom_emoji_id).
   * @param options.style - Optional button style.
   * @param options.icon_custom_emoji_id - Optional premium emoji.You need premium account for use this option
   * @throws {Error} If text or callback_data is missing.
   * @returns The instance for chaining.
   */
  addCallbackButton(
    text: string,
    callback_data: string,
    options: customStyleButton = {},
  ): InlineKeyboardBuilder {
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
      ...(style && { style }),
      ...(icon_custom_emoji_id && { icon_custom_emoji_id }),
    });
  }

  /**
   * Adds a callback button by callback data parts.
   *
   * @param scope - Callback scope.
   * @param action - Callback action.
   * @param id - Callback identifier.
   * @param text - Button text.
   * @param options - Optional button options (style, icon_custom_emoji_id).
   * @param separator - Separator between parts. Default is ":".
   * @returns The instance for chaining.
   */
  addCallbackButtonFromParts(
    scope: string,
    action: string,
    id: string | number,
    text: string,
    options: customStyleButton = {},
    separator = ":",
  ): InlineKeyboardBuilder {
    const callback_data = `${scope}${separator}${action}${separator}${id}`;
    return this.addCallbackButton(text, callback_data, options);
  }

  /**
   * Adds a URL button with optional style or emoji.
   *
   * @param text - Button text.
   * @param url - URL to open.
   * @param options - Optional button options (style, icon_custom_emoji_id).
   * @param options.style - Optional button style.
   * @param options.icon_custom_emoji_id - Optional premium emoji.You need premium account for use this option
   * @throws {Error} If text or URL is missing.
   * @returns The instance for chaining.
   */
  addUrlButton(
    text: string,
    url: string,
    options: customStyleButton = {},
  ): InlineKeyboardBuilder {
    if (!text || !url) {
      throw new Error("URL button requires text and url");
    }

    const { style, icon_custom_emoji_id } = options;

    if (style && !["primary", "danger", "success"].includes(style)) {
      throw new Error("Invalid style. Allowed: primary, danger, success");
    }

    return this._pushButton({
      text,
      url,
      ...(style && { style }),
      ...(icon_custom_emoji_id && { icon_custom_emoji_id }),
    });
  }

  /**
   * Adds a pay button.
   *
   * @param text - Button text.
   * @throws {Error} If text is missing.
   * @returns The instance for chaining.
   */
  addPayButton(text: string): InlineKeyboardBuilder {
    if (!text) {
      throw new Error("Pay button requires text");
    }
    return this._pushButton({ text, pay: true });
  }

  /**
   * Adds a fully custom button object.
   *
   * @param buttonObject - Must have at least a `text` property.
   * @throws {Error} If the button object is invalid.
   * @returns The instance for chaining.
   */
  addCustomButton(buttonObject: InlineKeyboardButton): InlineKeyboardBuilder {
    if (!buttonObject || !buttonObject.text) {
      throw new Error(
        "Custom button must be a valid InlineKeyboardButton object",
      );
    }
    return this._pushButton(buttonObject);
  }

  // ---------- layout controls ----------
  /**
   * Sets the number of buttons per row.
   * @param {number} n - Must be at least 1.
   * @returns The instance for chaining.
   */
  setButtonsPerRow(n: number) {
    this.buttonsPerRow = Math.max(1, Math.floor(n));
    return this;
  }

  /**
   * Sets the maximum characters per row before auto-wrapping.
   * @param n - 0 disables auto-wrap.
   * @returns The instance for chaining.
   */
  setAutoWrapMaxChars(n: number) {
    this.autoWrapMaxChars = Math.max(0, Math.floor(n));
    return this;
  }

  /**
   * Forces a new row in the keyboard.
   * @returns The instance for chaining.
   */
  newRow() {
    this.buttons.push({ __newRow: true } as InlineKeyboardButton);
    return this;
  }

  // ---------- config-based API ----------
  /**
   * Adds a button from a config object.
   * @param btn - Button config { type, text, ... }.
   */
  private _addButtonFromConfig(btn: buttonConfig): void {
    const { type, text } = btn;
    if (!type || !text)
      throw new Error("Button must have at least { type, text }");
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

  /**
   * Adds multiple buttons from config.
   * @param config - Array of button configs or grouped config.
   * @returns The instance for chaining.
   */
  addButtons(config: buttonConfig[] | groupedButtonConfig) {
    if (Array.isArray(config)) {
      for (const btn of config) this._addButtonFromConfig(btn);
      return this;
    }
    const { type, buttons } = config;
    if (!type || !Array.isArray(buttons))
      throw new Error("addButtons: invalid config");
    for (const btn of buttons) this._addButtonFromConfig(btn);
    return this;
  }

  /**
   * Creates a callback button config.
   * @param scope - The scope of the callback.
   * @param action - The action to trigger.
   * @param id - The ID of the callback.
   * @param separator - The separator to use between parts. Default is ":".
   * @returns The callback button config.
   */
  callbackData(
    scope: string,
    action: string,
    id: string | number,
    separator = ":",
  ) {
    return {
      type: "callback",
      text: `${scope}${separator}${action}${separator}${id}`,
    };
  }
  /**
   * Parses callback data into its components.
   * @param data - The callback data string to parse.
   * @param separator - The separator used in the callback data. Default is ":".
   * @returns An object with scope, action, and id properties.
   * @throws {Error} If the callback data format is invalid.
   */
  callbackDataParse(data: string, separator = ":") {
    const parts = data.split(separator);
    if (parts.length < 3) {
      throw new Error("Invalid callback data format");
    }
    const [scope, action, ...idParts] = parts;
    const id = idParts.join(separator);
    return { scope, action, id };
  }

  /**
   * Generates a readable preview of the current keyboard layout.
   *
   * Each row is displayed with its buttons and associated action type
   * (callback, URL, payment, or custom action).
   *
   * @returns A formatted string representation of the keyboard layout.
   */
  preview() {
    const buttonRows = this._layoutButtons();

    // Return a fallback message if no buttons exist
    if (buttonRows.length === 0) {
      return "No buttons added";
    }

    return buttonRows
      .map((row, rowIndex) => {
        const rowText = row
          .map((btn) => {
            // Callback button preview
            if ("callback_data" in btn) {
              return `[${btn.text}](callback:${btn.callback_data})`;
            }

            // URL button preview
            if ("url" in btn) {
              return `[${btn.text}](${btn.url})`;
            }

            // Payment button preview
            if ("pay" in btn) {
              return `[${btn.text}](pay)`;
            }

            // Generic custom button preview
            return `[${btn.text}](custom)`;
          })
          .join(" | ");

        // Prefix each row with its index
        return `Row ${rowIndex + 1}: ${rowText}`;
      })
      .join("\n");
  }

  /**
   * Renders a paginated list of items as inline keyboard buttons
   * and automatically appends pagination controls.
   *
   * The method:
   * - Splits items into pages
   * - Renders only items for the current page
   * - Adds navigation buttons (previous, next, first, last)
   * - Optionally hides pagination if only one page exists
   *
   * @typeParam T - Type of items in the list.
   * @param options - Configuration object for pagination behavior and item rendering.
   * @returns The current keyboard builder instance for chaining.
   */
  paginatedList<T>(options: PaginatedListOptions<T>): this {
    const { items, page, perPage, render, pagination } = options;

    // Ensure items is a valid array
    if (!Array.isArray(items)) {
      throw new Error("paginatedList: items must be an array");
    }

    // Ensure pagination callback exists
    if (typeof pagination?.callback !== "function") {
      throw new Error("paginatedList: pagination.callback must be a function");
    }

    // Normalize current page value
    const currentPage = Math.max(1, Math.floor(page));

    // Normalize items per page
    const per = Math.max(1, Math.floor(perPage) || 1);

    // Calculate total number of pages
    const totalPages = Math.max(1, Math.ceil(items.length / per));

    // Prevent page overflow
    const safePage = Math.min(currentPage, totalPages);

    // Calculate slice start index
    const start = (safePage - 1) * per;

    // Extract items for the current page
    const paginatedItems = items.slice(start, start + per);

    // Do nothing if no items exist
    if (paginatedItems.length === 0) {
      return this;
    }

    // Render paginated items as buttons
    for (const item of paginatedItems) {
      this._pushButton(render(item));
      this.newRow();
    }

    // Determine pagination state
    const isFirstPage = safePage === 1;
    const isLastPage = safePage === totalPages;

    // Hide pagination controls if only one page exists
    if (totalPages === 1 && pagination.hideIfSinglePage) {
      return this;
    }

    // Resolve button labels with defaults
    const labels = pagination.labels ?? {};
    const prevLabel = labels.previous ?? "⬅️";
    const nextLabel = labels.next ?? "➡️";
    const firstLabel = labels.first ?? "⏮";
    const lastLabel = labels.last ?? "⏭";

    // Callback used for the center counter button
    const counterCb = pagination.counterCallback ?? "ignore";

    // Start pagination controls on a new row
    this.newRow();

    // First page button
    if (pagination.showEdgeButtons) {
      this.addCallbackButton(
        isFirstPage ? `·${firstLabel}·` : firstLabel,
        isFirstPage ? "ignore" : pagination.callback(1),
      );
    }

    // Previous page button
    this.addCallbackButton(
      isFirstPage ? `·${prevLabel}·` : prevLabel,
      isFirstPage ? "ignore" : pagination.callback(safePage - 1),
    );

    // Current page counter button
    this.addCallbackButton(`${safePage}/${totalPages}`, counterCb);

    // Next page button
    this.addCallbackButton(
      isLastPage ? `·${nextLabel}·` : nextLabel,
      isLastPage ? "ignore" : pagination.callback(safePage + 1),
    );

    // Last page button
    if (pagination.showEdgeButtons) {
      this.addCallbackButton(
        isLastPage ? `·${lastLabel}·` : lastLabel,
        isLastPage ? "ignore" : pagination.callback(totalPages),
      );
    }

    // End pagination row
    this.newRow();

    return this;
  }
  // ---------- layout engine ----------
  /**
   * Internal method that lays out buttons into rows based on configuration.
   * @returns Array of rows with buttons.
   */
  private _layoutButtons() {
    return layoutButtons(
      this.buttons,
      this.buttonsPerRow,
      this.autoWrapMaxChars,
    );
  }

  // ---------- validation ----------
  /**
   * Runs validation rules against the current keyboard state.
   * @param options - Mode and context overrides.
   */
  validate(options: ValidateOptions = {}): ValidationResult {
    return this._validation.validate(this._keyboardInput(), options);
  }

  /**
   * Registers a custom validation rule.
   */
  registerRule(rule: ValidationRule): InlineKeyboardBuilder {
    this._validation.registerRule(rule);
    return this;
  }

  /**
   * Loads a validation plugin (rules + setup hook).
   */
  use(plugin: ValidationPlugin): InlineKeyboardBuilder {
    this._validation.use(plugin);
    return this;
  }

  /**
   * Enables/disables rules and overrides severities.
   */
  setRules(config: RulesConfig): InlineKeyboardBuilder {
    this._validation.setRules(config);
    return this;
  }

  /**
   * Sets the default validation mode for build({ validate: true }).
   */
  setValidationMode(mode: ValidationMode): InlineKeyboardBuilder {
    this._validation.setDefaultMode(mode);
    return this;
  }

  /**
   * Sets the default validation context (message, invoice, etc.).
   */
  setValidationContext(
    contextType: ValidateOptions["contextType"],
  ): InlineKeyboardBuilder {
    if (contextType !== undefined) {
      this._validation.setContextType(contextType);
    }
    return this;
  }

  setRuleEnabled(ruleId: string, enabled: boolean): InlineKeyboardBuilder {
    this._validation.setRuleEnabled(ruleId, enabled);
    return this;
  }

  setRuleSeverity(
    ruleId: string,
    severity: DiagnosticSeverity,
  ): InlineKeyboardBuilder {
    this._validation.setRuleSeverity(ruleId, severity);
    return this;
  }

  private _keyboardInput() {
    return {
      buttons: this.buttons,
      buttonsPerRow: this.buttonsPerRow,
      autoWrapMaxChars: this.autoWrapMaxChars,
    };
  }

  private _applyValidationOnBuild(options?: BuildOptions): ValidationResult | null {
    if (!options?.validate) {
      return null;
    }
    const validateOptions: ValidateOptions = {};
    if (options.validationMode !== undefined) {
      validateOptions.mode = options.validationMode;
    }
    const result = this.validate(validateOptions);
    const mode = result.mode;
    if (mode === "strict" && !result.ok) {
      throw new ValidationError(result);
    }
    return result;
  }

  // ---------- final output ----------
  /**
   * Builds the final Telegram reply_markup object.
   * @param options - Optional validation before returning markup.
   * @returns Telegram inline_keyboard reply_markup.
   */
  build(options?: BuildOptions) {
    this._applyValidationOnBuild(options);
    return {
      reply_markup: {
        inline_keyboard: this._layoutButtons(),
      },
    };
  }
}

export {
  ValidationEngine,
  ValidationError,
  createValidationEngine,
  createDiagnostic,
  normalizeKeyboard,
  builtinRules,
  RULE_IDS,
} from "./validator/index.js";

export type {
  BuildOptions,
  Diagnostic,
  DiagnosticLocation,
  DiagnosticSeverity,
  RulesConfig,
  ValidateOptions,
  ValidationContextType,
  ValidationMode,
  ValidationPlugin,
  ValidationResult,
  ValidationRule,
} from "./validator/index.js";
