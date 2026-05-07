import pytest

from sheets_airtable_sync.transforms import (
    apply_transform,
    norm_currency,
    norm_date,
    norm_email,
    norm_multiselect,
)


def test_core_transforms() -> None:
    assert norm_email(" USER@Example.COM ") == "user@example.com"
    assert norm_currency("$1,200") == "1200.00"
    assert norm_date("05/02/2026") == "2026-05-02"
    assert norm_multiselect("a; b, c") == ["a", "b", "c"]


def test_unsafe_formula_rejected() -> None:
    with pytest.raises(ValueError):
        apply_transform("=IMPORTXML('x')", "text")
