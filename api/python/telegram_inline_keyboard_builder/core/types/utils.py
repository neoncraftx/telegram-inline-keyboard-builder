"""
Utility type definitions — pagination configuration.

Mirrors the TypeScript types in utils.ts.
"""

from __future__ import annotations
from typing import Callable, Generic, TypeVar
from typing_extensions import TypedDict, NotRequired

from .buttons import InlineKeyboardButton

T = TypeVar("T")


class PaginationLabels(TypedDict, total=False):
    """
    Custom labels for the four pagination navigation buttons.

    All fields are optional — unset labels fall back to their defaults.

    Example::

        labels: PaginationLabels = {
            "previous": "◀️",
            "next":     "▶️",
            "first":    "⏮",
            "last":     "⏭",
        }
    """

    previous: str
    """Label for the *previous page* button. Default: ``"⬅️"``."""

    next: str
    """Label for the *next page* button. Default: ``"➡️"``."""

    first: str
    """Label for the *first page* button. Default: ``"⏮"``.
    Only rendered when ``show_edge_buttons=True``."""

    last: str
    """Label for the *last page* button. Default: ``"⏭"``.
    Only rendered when ``show_edge_buttons=True``."""


class PaginationConfig(TypedDict, total=False):
    """
    Full configuration for the pagination navigation bar.

    Example::

        config: PaginationConfig = {
            "callback":           lambda p: f"products_page_{p}",
            "hide_if_single_page": True,
            "show_edge_buttons":   False,
            "labels": {"previous": "◀️", "next": "▶️"},
        }
    """

    callback: Callable[[int], str]
    """
    **Required.** Function that receives a page number and returns the
    ``callback_data`` string for that page's navigation button.

    Example::

        "callback": lambda p: f"items_page_{p}"
    """

    labels: NotRequired[PaginationLabels]
    """Custom labels for the navigation buttons."""

    show_edge_buttons: NotRequired[bool]
    """
    When ``True``, adds ⏮ and ⏭ buttons to jump directly to the
    first and last page. Default: ``False``.
    """

    hide_if_single_page: NotRequired[bool]
    """
    When ``True``, the navigation bar is completely hidden if all items
    fit on a single page. Default: ``False``.
    """

    counter_callback: NotRequired[str]
    """
    ``callback_data`` sent when the user taps the central counter button
    (e.g. ``"2/5"``). Default: ``"ignore"``.
    """


class PaginatedListOptions(TypedDict, Generic[T]):
    """
    Full configuration object passed to
    :meth:`~builder.InlineKeyboardBuilder.paginated_list`.

    Example::

        options: PaginatedListOptions[Product] = {
            "items":      all_products,
            "page":       current_page,
            "per_page":   5,
            "render":     lambda p: {"text": p.name, "callback_data": f"product_{p.id}"},
            "pagination": {"callback": lambda p: f"products_page_{p}"},
        }
    """

    items: list[T]
    """Complete (unsliced) list of items to paginate."""

    page: int
    """Current page number — starts at ``1``."""

    per_page: int
    """Number of items displayed per page."""

    render: Callable[[T], InlineKeyboardButton]
    """
    Function that converts a single item into an
    :data:`~types.buttons.InlineKeyboardButton` dict.
    """

    pagination: PaginationConfig
    """Navigation bar configuration."""
