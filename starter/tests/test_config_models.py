"""Fail-fast validation of routing model names.

An unpriced model used to surface only *after* the paid LLM call, as a
KeyError in compute_cost (HTTP 500, tokens spent but never logged) or a
silent $0 on the streaming path. Settings now reject unpriced models at
startup, and a blank MODEL_BUDGET disables the budget tier.
"""

import pytest
from pydantic import ValidationError

from src.config import Settings


@pytest.mark.parametrize("field", ["model_budget", "model_simple", "model_complex"])
def test_unpriced_routing_model_is_rejected_at_startup(field):
    with pytest.raises(ValidationError, match="MODEL_PRICING"):
        Settings(**{field: "gpt-4.1-mini-typo"})


@pytest.mark.parametrize("blank", ["", "   ", "\t"])
def test_blank_budget_model_disables_tier(blank):
    assert Settings(model_budget=blank).model_budget == ""


def test_routing_model_names_are_stripped():
    assert Settings(model_simple=" gpt-4o-mini ").model_simple == "gpt-4o-mini"


def test_blank_simple_model_is_rejected():
    with pytest.raises(ValidationError):
        Settings(model_simple="  ")
