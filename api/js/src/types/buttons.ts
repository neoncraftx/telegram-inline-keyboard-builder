/**
 * Represents a Telegram custom emoji identifier.
 */
export type customEmojiId = string;

/**
 * Available visual styles for a button.
 */
export type buttonStyle = "primary" | "danger" | "success";

/**
 * Additional custom styling options for a button.
 */
export type customStyleButton = {
  /**
   * Visual style applied to the button.
   */
  style?: buttonStyle;

  /**
   * Custom emoji ID displayed as the button icon.
   */
  icon_custom_emoji_id?: customEmojiId;
};

/**
 * Base button structure shared across all button types.
 */
interface Button {
  /**
   * Text displayed on the button.
   */
  text: string;

  /**
   * Optional visual style of the button.
   */
  style?: buttonStyle;

  /**
   * Optional custom emoji icon identifier.
   */
  icon_custom_emoji_id?: customEmojiId;

  /**
   * Indicates that the button should start on a new row.
   */
  __newRow?: boolean;
}

/**
 * Button triggering a callback query.
 */
interface CallbackButton extends Button {
  /**
   * Callback data sent when the button is pressed.
   */
  callback_data: string;
}

/**
 * Button opening an external URL.
 */
interface UrlButton extends Button {
  /**
   * URL opened when the button is pressed.
   */
  url: string;
}

/**
 * Telegram payment button.
 */
interface PayButton extends Button {
  /**
   * Enables Telegram payment behavior for the button.
   */
  pay: boolean;
}

/**
 * Generic custom button without predefined behavior.
 */
interface CustomButton extends Button {}

/**
 * Supported button configuration types.
 */
type ButtonConfigTypes = "callback" | "url" | "pay" | "custom";

/**
 * Configuration object describing a single button.
 */
export interface buttonConfig {
  /**
   * Type of the button behavior.
   */
  type: ButtonConfigTypes;

  /**
   * Text displayed on the button.
   */
  text: string;

  /**
   * Optional callback or custom data associated with the button.
   */
  data?: string;

  /**
   * Optional URL used for URL buttons.
   */
  url?: string;

  /**
   * Final generated InlineKeyboardButton instance.
   */
  button: InlineKeyboardButton;
}

/**
 * Configuration object grouping multiple buttons together.
 */
export interface groupedButtonConfig {
  /**
   * Shared type for all grouped buttons.
   */
  type: ButtonConfigTypes;

  /**
   * List of buttons inside the group.
   */
  buttons: buttonConfig[];
}

/**
 * Represents any supported inline keyboard button type.
 */
export type InlineKeyboardButton =
  | CallbackButton
  | UrlButton
  | PayButton
  | CustomButton;