from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Tuple

DATA_PATH = Path(__file__).with_name("grocery_products.json")


@dataclass
class BasketResult:
    selected_items: List[dict]
    total_cost: float
    remaining_budget: float
    estimated_savings: float
    swaps: List[str]
    message: str


def load_products(path: Path = DATA_PATH) -> List[dict]:
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def _priority_order(need: str) -> List[str]:
    if need == "basics_only":
        return ["staple", "protein", "cooking_basics", "hygiene"]
    if need == "supper_ideas":
        return ["staple", "protein", "veg", "cooking_basics", "hygiene"]
    return ["staple", "protein", "cooking_basics", "hygiene", "veg"]


def _filtered_products(products: List[dict], preference: str) -> List[dict]:
    if preference == "no_meat":
        return [p for p in products if "chicken" not in p["product_name"].lower()]
    return products


def build_basket(
    budget: float,
    household_size: int,
    preference: str,
    need: str,
    city_or_province: str | None = None,
) -> BasketResult:
    products = _filtered_products(load_products(), preference)
    by_category: Dict[str, List[dict]] = {}
    for product in products:
        by_category.setdefault(product["category"], []).append(product)

    # cheaper first in each category
    for category in by_category:
        by_category[category].sort(key=lambda item: item["price"])

    order = _priority_order(need)
    chosen: List[dict] = []
    total = 0.0
    swaps: List[str] = []
    saved = 0.0

    size_factor = 1 if household_size <= 2 else 2 if household_size <= 4 else 3

    for category in order:
        options = by_category.get(category, [])
        if not options:
            continue

        best = options[0]
        expensive = options[-1]

        qty = size_factor if category in {"staple", "protein"} else 1

        for _ in range(qty):
            if total + best["price"] <= budget:
                chosen.append(best)
                total += best["price"]

        if expensive["price"] > best["price"]:
            diff = expensive["price"] - best["price"]
            saved += diff
            swaps.append(
                f"Swap {expensive['product_name']} for {best['product_name']} and save about R{diff:.2f}."
            )

    if preference == "with_meat":
        meat_options = [p for p in products if "chicken" in p["product_name"].lower()]
        if meat_options:
            meat = sorted(meat_options, key=lambda x: x["price"])[0]
            if total + meat["price"] <= budget:
                chosen.append(meat)
                total += meat["price"]

    remaining = budget - total

    location_text = f" for {city_or_province}" if city_or_province else ""
    message = (
        f"For a household of {household_size}{location_text}, this basket costs about R{total:.2f}. "
        f"You still have R{remaining:.2f} left. Focus on staples first, then protein and basics."
    )

    return BasketResult(
        selected_items=chosen,
        total_cost=round(total, 2),
        remaining_budget=round(remaining, 2),
        estimated_savings=round(saved, 2),
        swaps=swaps[:3],
        message=message,
    )
