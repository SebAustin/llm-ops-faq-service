"""Contract tests for the shipped product catalog in data/products/.

Every file must pass the same schema the inbox watcher enforces, and
product_ids must be unique: Chroma upserts on product_id, so a duplicate
silently overwrites an existing product instead of adding a new one.
"""

import json
from pathlib import Path

import pytest

from src.ingestion import validate_product

PRODUCTS_DIR = Path(__file__).resolve().parents[2] / "data" / "products"
PRODUCT_FILES = sorted(PRODUCTS_DIR.glob("*.json"))
SEED_CATALOG_SIZE = 30
MIN_NEW_PRODUCTS = 5


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def test_catalog_includes_at_least_five_products_beyond_seed():
    assert len(PRODUCT_FILES) >= SEED_CATALOG_SIZE + MIN_NEW_PRODUCTS


@pytest.mark.parametrize("path", PRODUCT_FILES, ids=lambda p: p.name)
def test_product_file_passes_ingestion_schema(path):
    assert validate_product(_load(path)) is None


@pytest.mark.parametrize("path", PRODUCT_FILES, ids=lambda p: p.name)
def test_product_price_is_positive_number(path):
    price = _load(path)["price"]
    assert isinstance(price, (int, float)) and price > 0


@pytest.mark.parametrize("path", PRODUCT_FILES, ids=lambda p: p.name)
def test_filename_starts_with_product_id(path):
    assert path.name.startswith(_load(path)["product_id"])


def test_product_ids_are_unique():
    ids = [_load(p)["product_id"] for p in PRODUCT_FILES]
    assert len(ids) == len(set(ids))
