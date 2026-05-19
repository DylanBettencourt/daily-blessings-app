from basket_logic import build_basket


def test_basket_stays_within_budget():
    result = build_basket(
        budget=300,
        household_size=3,
        preference="anything_cheap",
        need="full_week",
    )
    assert result.total_cost <= 300
    assert len(result.selected_items) > 0


def test_no_meat_preference_excludes_chicken():
    result = build_basket(
        budget=500,
        household_size=4,
        preference="no_meat",
        need="full_week",
    )
    names = [item["product_name"].lower() for item in result.selected_items]
    assert all("chicken" not in name for name in names)


def test_swap_suggestions_present():
    result = build_basket(
        budget=200,
        household_size=2,
        preference="anything_cheap",
        need="basics_only",
    )
    assert len(result.swaps) >= 1
    assert result.estimated_savings > 0
