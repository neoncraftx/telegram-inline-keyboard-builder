import type { InlineKeyboardButton } from "./buttons.js";

export interface PaginationLabels {
  /**
   * Label for the "previous page" button.
   */
  previous?: string;

  /**
   * Label for the "next page" button.
   */
  next?: string;

  /**
   * Label for the "first page" button.
   */
  first?: string;

  /**
   * Label for the "last page" button.
   */
  last?: string;
}

export interface PaginatedListOptions<T> {
  /** 
   * Array of items to display in the paginated list.
   */
  items: T[];

  /** 
   * Current page number (starting from 1).
   */
  page: number;

  /** 
   * Number of items displayed per page.
   */
  perPage: number;

  /** 
   * Function used to transform an item into an InlineKeyboardButton.
   */
  render: (item: T) => InlineKeyboardButton;

  pagination: {
    /** 
     * Function that generates the callback data for a given page.
     */
    callback: (page: number) => string;

    /** 
     * Custom labels for pagination buttons (previous, next, etc.).
     */
    labels?: PaginationLabels;

    /** 
     * Whether to display edge navigation buttons
     * (first page ⏮ and last page ⏭).
     */
    showEdgeButtons?: boolean;

    /** 
     * Hides pagination controls when there is only one page.
     * @default false
     */
    hideIfSinglePage?: boolean;

    /** 
     * Callback data used for the center counter button.
     * @default "ignore"
     */
    counterCallback?: string;
  };
}