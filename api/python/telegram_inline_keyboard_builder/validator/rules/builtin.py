from .callback_data_too_long import callback_data_too_long_rule
from .duplicate_callback_data import duplicate_callback_data_rule
from .empty_button_text import empty_button_text_rule
from .empty_row import empty_row_rule
from .incompatible_button_context import incompatible_button_context_rule
from .inconsistent_configuration import inconsistent_configuration_rule
from .invalid_keyboard_structure import invalid_keyboard_structure_rule
from .invalid_url import invalid_url_rule
from .too_many_buttons_per_row import too_many_buttons_per_row_rule
from .unexpected_null_undefined import unexpected_null_undefined_rule

builtin_rules = [
    callback_data_too_long_rule,
    empty_button_text_rule,
    invalid_url_rule,
    empty_row_rule,
    too_many_buttons_per_row_rule,
    incompatible_button_context_rule,
    inconsistent_configuration_rule,
    duplicate_callback_data_rule,
    unexpected_null_undefined_rule,
    invalid_keyboard_structure_rule,
]

__all__ = ["builtin_rules"]
