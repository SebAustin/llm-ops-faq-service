"""Tests for src.pricing — every routable model must have a price."""

import pytest

from src.config import settings
from src.models import TokenUsage
from src.pricing import MODEL_PRICING, compute_cost


@pytest.mark.parametrize("attr", ["model_budget", "model_simple", "model_complex"])
def test_every_default_routing_tier_is_priced(attr):
    assert getattr(settings, attr) in MODEL_PRICING


def test_budget_tier_is_cheapest_per_token():
    usage = TokenUsage(prompt_tokens=1_000, completion_tokens=200)
    costs = {
        attr: compute_cost(getattr(settings, attr), usage)
        for attr in ("model_budget", "model_simple", "model_complex")
    }
    assert costs["model_budget"] < costs["model_simple"] < costs["model_complex"]


def test_gpt_41_nano_cost_matches_published_rate():
    # $0.10 / 1M input, $0.40 / 1M output (OpenAI public pricing)
    usage = TokenUsage(prompt_tokens=1_000_000, completion_tokens=1_000_000)
    assert compute_cost("gpt-4.1-nano", usage) == pytest.approx(0.50)
