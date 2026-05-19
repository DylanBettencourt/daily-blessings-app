import streamlit as st
from basket_logic import build_basket

st.set_page_config(page_title="Siza Basket Doctor", layout="centered")
st.title("🧺 Siza Basket Doctor")
st.caption("Low-data grocery planner for Scrolla/Siza Khula users.")

with st.form("basket_form"):
    budget = st.number_input("Budget amount (R)", min_value=50.0, value=500.0, step=10.0)
    household_size = st.number_input("Household size", min_value=1, max_value=15, value=4, step=1)
    location = st.text_input("Province or city (optional)")
    preference = st.selectbox(
        "Preference",
        options=["anything_cheap", "no_meat", "with_meat"],
        format_func=lambda p: {
            "anything_cheap": "Anything cheap",
            "no_meat": "No meat",
            "with_meat": "With meat",
        }[p],
    )
    need = st.selectbox(
        "Need",
        options=["full_week", "supper_ideas", "basics_only"],
        format_func=lambda n: {
            "full_week": "Full week",
            "supper_ideas": "Supper ideas",
            "basics_only": "Basics only",
        }[n],
    )
    submitted = st.form_submit_button("Build my basket")

if submitted:
    result = build_basket(
        budget=budget,
        household_size=int(household_size),
        preference=preference,
        need=need,
        city_or_province=location.strip() or None,
    )

    st.subheader("Recommended basket")
    st.write(f"Estimated total: **R{result.total_cost:.2f}**")
    st.write(f"Estimated savings from swaps: **R{result.estimated_savings:.2f}**")

    for item in result.selected_items:
        st.write(
            f"- {item['product_name']} ({item['size']}) — R{item['price']:.2f} at {item['retailer']}"
        )

    st.subheader("Cheaper swap ideas")
    for swap in result.swaps:
        st.write(f"- {swap}")

    st.subheader("Siza Khula answer")
    st.info(result.message)
