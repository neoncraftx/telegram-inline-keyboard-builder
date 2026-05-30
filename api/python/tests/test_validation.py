"""Smart Validation & Warnings — parity with api/js/test/validation.test.mjs"""

from __future__ import annotations

import pytest

from telegram_inline_keyboard_builder import (
    InlineKeyboardBuilder,
    RULE_IDS,
    ValidationError,
    ValidationRule,
    create_validation_engine,
)


def test_validate_ok_for_valid_keyboard() -> None:
    kb = InlineKeyboardBuilder()
    kb.add_callback_button("Yes", "ok:yes:1")
    result = kb.validate()
    assert result["ok"] is True
    assert len(result["errors"]) == 0


def test_detects_callback_data_exceeding_64_bytes() -> None:
    kb = InlineKeyboardBuilder()
    kb.add_custom_button({"text": "Go", "callback_data": "x" * 65})
    result = kb.validate()
    assert result["ok"] is False
    assert any(
        d["rule_id"] == RULE_IDS.CALLBACK_DATA_TOO_LONG for d in result["errors"]
    )


def test_detects_empty_button_text() -> None:
    kb = InlineKeyboardBuilder()
    kb.add_custom_button({"text": "   ", "callback_data": "a"})
    result = kb.validate()
    assert any(
        d["rule_id"] == RULE_IDS.EMPTY_BUTTON_TEXT for d in result["diagnostics"]
    )


def test_detects_invalid_url() -> None:
    kb = InlineKeyboardBuilder()
    kb.add_url_button("Site", "not-a-url")
    result = kb.validate()
    assert any(d["rule_id"] == RULE_IDS.INVALID_URL for d in result["errors"])


def test_warns_on_duplicate_callback_data() -> None:
    kb = InlineKeyboardBuilder()
    kb.add_callback_button("A", "dup")
    kb.add_callback_button("B", "dup")
    result = kb.validate()
    assert any(
        d["rule_id"] == RULE_IDS.DUPLICATE_CALLBACK_DATA for d in result["warnings"]
    )


def test_detects_pay_button_outside_invoice_context() -> None:
    kb = InlineKeyboardBuilder()
    kb.add_pay_button("Pay")
    result = kb.validate({"context_type": "message"})
    assert any(
        d["rule_id"] == RULE_IDS.INCOMPATIBLE_BUTTON_CONTEXT
        for d in result["errors"]
    )


def test_build_strict_raises_validation_error() -> None:
    kb = InlineKeyboardBuilder()
    kb.add_url_button("Bad", "ftp://bad")
    with pytest.raises(ValidationError):
        kb.build(validate=True, validation_mode="strict")


def test_build_warn_does_not_raise() -> None:
    kb = InlineKeyboardBuilder()
    kb.add_url_button("Bad", "ftp://bad")
    markup = kb.build(validate=True, validation_mode="warn")
    assert len(markup["reply_markup"]["inline_keyboard"]) > 0


def test_register_rule_custom() -> None:
    kb = InlineKeyboardBuilder()

    def _run(_ctx):
        return [
            {
                "rule_id": "no-test-label",
                "message": "Avoid TEST labels in production",
                "severity": "warning",
            }
        ]

    kb.register_rule(
        ValidationRule(id="no-test-label", run=_run, default_severity="warning")
    )
    kb.add_callback_button("TEST", "x")
    result = kb.validate()
    assert any(d["rule_id"] == "no-test-label" for d in result["warnings"])


def test_use_plugin() -> None:
    kb = InlineKeyboardBuilder()

    def _always_info(_ctx):
        return [
            {
                "rule_id": "always-info",
                "message": "Plugin attached",
                "severity": "info",
            }
        ]

    kb.use(
        {
            "name": "demo-plugin",
            "rules": [
                ValidationRule(
                    id="always-info",
                    run=_always_info,
                    default_severity="info",
                )
            ],
        }
    )
    result = kb.validate()
    assert any(d["rule_id"] == "always-info" for d in result["diagnostics"])


def test_set_rules_disables_rule() -> None:
    kb = InlineKeyboardBuilder()
    kb.add_url_button("Bad", "not-valid")
    kb.set_rules({"disabled": [RULE_IDS.INVALID_URL]})
    result = kb.validate()
    assert not any(d["rule_id"] == RULE_IDS.INVALID_URL for d in result["errors"])


def test_too_many_buttons_per_row() -> None:
    kb = InlineKeyboardBuilder(10)
    for i in range(9):
        kb.add_callback_button(f"B{i}", f"btn:{i}")
    result = kb.validate()
    assert any(
        d["rule_id"] == RULE_IDS.TOO_MANY_BUTTONS_PER_ROW for d in result["errors"]
    )


def test_consecutive_new_row_markers() -> None:
    kb = InlineKeyboardBuilder()
    kb.new_row()
    kb.new_row()
    kb.add_callback_button("Only", "x")
    result = kb.validate()
    assert any(d["rule_id"] == RULE_IDS.EMPTY_ROW for d in result["warnings"])


def test_standalone_validation_engine() -> None:
    engine = create_validation_engine()
    result = engine.validate(
        {
            "buttons": [{"text": "X", "callback_data": "a"}],
            "buttons_per_row": 2,
            "auto_wrap_max_chars": 0,
        }
    )
    assert result["ok"] is True
