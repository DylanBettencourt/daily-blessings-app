import streamlit as st

st.set_page_config(
    page_title="Salary Stretch Calculator",
    page_icon="💸",
    layout="centered",
)

# ── Dark theme & typography override ────────────────────────────────────────
st.markdown(
    """
    <style>
      /* Force dark background everywhere */
      html, body, [data-testid="stAppViewContainer"],
      [data-testid="stMain"], .main, section.main {
          background-color: #0d0d0d !important;
          color: #f0f0f0 !important;
      }
      [data-testid="stSidebar"] { background-color: #111 !important; }

      /* Hide default Streamlit padding clutter */
      .block-container { padding-top: 2rem !important; }

      /* Slider track & thumb */
      .stSlider [data-baseweb="slider"] div[role="slider"] {
          background-color: #ff4444 !important;
      }

      /* Number input */
      input[type="number"] {
          background: #1a1a1a !important;
          color: #ffffff !important;
          border: 1px solid #333 !important;
          border-radius: 6px !important;
          font-size: 1.3rem !important;
          font-weight: 700 !important;
      }

      /* Labels */
      label, .stSlider label {
          color: #aaaaaa !important;
          font-size: 0.85rem !important;
          letter-spacing: 0.05em !important;
          text-transform: uppercase !important;
      }

      /* Expense row card */
      .expense-row {
          background: #1a1a1a;
          border-left: 4px solid #333;
          border-radius: 6px;
          padding: 12px 16px;
          margin-bottom: 6px;
          display: flex;
          justify-content: space-between;
          align-items: center;
      }
      .expense-label { font-size: 1rem; color: #cccccc; }
      .expense-cost  { font-size: 1.05rem; font-weight: 700; color: #888888; }

      /* Balance bar */
      .balance-card {
          border-radius: 10px;
          padding: 18px 22px;
          margin: 8px 0;
          display: flex;
          justify-content: space-between;
          align-items: center;
      }
      .balance-label { font-size: 0.9rem; letter-spacing: 0.08em; text-transform: uppercase; }
      .balance-amount { font-size: 2rem; font-weight: 900; letter-spacing: -0.02em; }

      /* Verdict box */
      .verdict {
          border-radius: 12px;
          padding: 22px;
          text-align: center;
          margin-top: 18px;
      }
      .verdict-emoji { font-size: 3rem; }
      .verdict-msg   { font-size: 1.25rem; font-weight: 700; margin-top: 8px; line-height: 1.4; }
      .verdict-sub   { font-size: 0.9rem; color: #aaa; margin-top: 6px; }

      /* Section headers */
      .section-title {
          font-size: 0.75rem;
          letter-spacing: 0.15em;
          text-transform: uppercase;
          color: #555;
          margin: 24px 0 10px;
          border-bottom: 1px solid #222;
          padding-bottom: 6px;
      }

      /* Hide streamlit footer */
      footer { visibility: hidden; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ── Header ───────────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style='text-align:center; padding: 10px 0 4px;'>
      <div style='font-size:2.6rem; font-weight:900; letter-spacing:-0.03em; color:#ffffff;'>
        SALARY STRETCH
      </div>
      <div style='font-size:2.6rem; font-weight:900; letter-spacing:-0.03em; color:#ff4444;'>
        CALCULATOR
      </div>
      <div style='color:#555; font-size:0.85rem; margin-top:6px; letter-spacing:0.1em;'>
        SOUTH AFRICA · 2024 REAL COSTS
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<br>", unsafe_allow_html=True)

# ── Monthly take-home input ──────────────────────────────────────────────────
st.markdown(
    "<div class='section-title'>Your monthly take-home pay</div>",
    unsafe_allow_html=True,
)
take_home = st.number_input(
    "Monthly take-home pay (R)",
    min_value=0,
    max_value=200_000,
    value=8_500,
    step=500,
    label_visibility="collapsed",
)

st.markdown(
    f"<div style='font-size:3.2rem; font-weight:900; color:#ffffff; text-align:center; "
    f"padding:6px 0 2px; letter-spacing:-0.03em;'>R {take_home:,.0f}</div>"
    f"<div style='text-align:center; color:#444; font-size:0.8rem; "
    f"letter-spacing:0.12em; margin-bottom:4px;'>PER MONTH</div>",
    unsafe_allow_html=True,
)

# ── Expense definitions (2024 SA averages) ──────────────────────────────────
EXPENSES = [
    {
        "key": "rent",
        "icon": "🏠",
        "label": "Rent / Bond",
        "note": "1-bed in affordable township or flat",
        "default": 4_500,
        "min": 1_500,
        "max": 20_000,
        "step": 250,
    },
    {
        "key": "food",
        "icon": "🛒",
        "label": "Groceries & Food",
        "note": "Monthly shop for 1 person",
        "default": 2_800,
        "min": 800,
        "max": 10_000,
        "step": 100,
    },
    {
        "key": "transport",
        "icon": "🚌",
        "label": "Transport",
        "note": "Taxi / bus / train commute",
        "default": 1_200,
        "min": 200,
        "max": 6_000,
        "step": 100,
    },
    {
        "key": "electricity",
        "icon": "💡",
        "label": "Electricity",
        "note": "Prepaid units (Eskom / municipal)",
        "default": 650,
        "min": 100,
        "max": 3_000,
        "step": 50,
    },
    {
        "key": "airtime",
        "icon": "📱",
        "label": "Airtime & Data",
        "note": "Monthly bundle / prepaid top-ups",
        "default": 350,
        "min": 50,
        "max": 2_000,
        "step": 50,
    },
]

st.markdown(
    "<div class='section-title'>Monthly expenses</div>", unsafe_allow_html=True
)
st.markdown(
    "<div style='color:#444; font-size:0.78rem; margin-bottom:12px;'>"
    "Drag the sliders to match your actual spending.</div>",
    unsafe_allow_html=True,
)

# ── Collect slider values ────────────────────────────────────────────────────
user_costs = {}
for exp in EXPENSES:
    col_label, col_slider, col_val = st.columns([0.28, 0.52, 0.20])
    with col_label:
        st.markdown(
            f"<div style='padding-top:28px; color:#cccccc; font-size:0.95rem;'>"
            f"{exp['icon']} {exp['label']}</div>",
            unsafe_allow_html=True,
        )
    with col_slider:
        val = st.slider(
            exp["label"],
            min_value=exp["min"],
            max_value=exp["max"],
            value=exp["default"],
            step=exp["step"],
            label_visibility="collapsed",
            key=f"slider_{exp['key']}",
        )
    with col_val:
        st.markdown(
            f"<div style='padding-top:28px; text-align:right; font-size:1.0rem; "
            f"font-weight:700; color:#888888;'>R{val:,}</div>",
            unsafe_allow_html=True,
        )
    user_costs[exp["key"]] = val

# ── Breakdown ────────────────────────────────────────────────────────────────
st.markdown(
    "<div class='section-title'>The brutal breakdown</div>", unsafe_allow_html=True
)

balance = float(take_home)


def _color(amount: float) -> str:
    """Return a hex colour based on how comfortable the balance is."""
    if amount <= 0:
        return "#ff2222"
    pct = amount / max(take_home, 1)
    if pct > 0.35:
        return "#22cc88"  # green
    if pct > 0.20:
        return "#f0c040"  # amber
    if pct > 0.08:
        return "#ff8800"  # orange
    return "#ff2222"      # red


def _bg(amount: float) -> str:
    col = _color(amount)
    opacity = "22"  # hex alpha ~14 %
    return col + opacity


for exp in EXPENSES:
    cost = user_costs[exp["key"]]
    balance -= cost
    color = _color(balance)
    bg = _bg(balance)

    st.markdown(
        f"""
        <div style='background:#1a1a1a; border-left:4px solid #2a2a2a;
                    border-radius:6px; padding:10px 16px; margin-bottom:4px;'>
          <div style='display:flex; justify-content:space-between; align-items:center;'>
            <div style='color:#999; font-size:0.9rem;'>
              {exp['icon']} {exp['label']}
              <span style='color:#444; font-size:0.75rem; margin-left:8px;'>
                − R{cost:,}
              </span>
            </div>
            <div style='font-size:0.75rem; color:#555;'>{exp['note']}</div>
          </div>
        </div>
        <div style='background:{bg}; border-left:4px solid {color};
                    border-radius:6px; padding:12px 16px; margin-bottom:10px;
                    display:flex; justify-content:space-between; align-items:center;'>
          <div style='color:{color}; font-size:0.78rem; letter-spacing:0.1em;
                      text-transform:uppercase; font-weight:600;'>
            Remaining after {exp['label'].lower()}
          </div>
          <div style='color:{color}; font-size:1.9rem; font-weight:900;
                      letter-spacing:-0.02em;'>
            R {balance:,.0f}
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

# ── Final verdict ─────────────────────────────────────────────────────────────
total_expenses = sum(user_costs.values())
pct_left = (balance / take_home * 100) if take_home > 0 else 0

if balance <= 0:
    verdict_bg = "#2a0000"
    verdict_border = "#ff2222"
    emoji = "🚨"
    headline = "You're already in the red."
    sub = (
        f"Your expenses exceed your income by R{abs(balance):,.0f}. "
        "Something has to give — or debt fills the gap."
    )
elif pct_left < 8:
    verdict_bg = "#1e0a00"
    verdict_border = "#ff6600"
    emoji = "😰"
    headline = f"Only R{balance:,.0f} left. That's {pct_left:.0f}% of your salary."
    sub = "One taxi fare. One school fee. One load-shedding surge bill. Gone."
elif pct_left < 20:
    verdict_bg = "#1c1800"
    verdict_border = "#f0c040"
    emoji = "😬"
    headline = f"R{balance:,.0f} left — thin ice."
    sub = (
        f"That's {pct_left:.0f}% of your take-home. No buffer for emergencies, "
        "medical, or clothing."
    )
elif pct_left < 40:
    verdict_bg = "#001a10"
    verdict_border = "#22cc88"
    emoji = "😌"
    headline = f"R{balance:,.0f} left — workable, but tight."
    sub = (
        f"{pct_left:.0f}% remaining. You can save a little, but lifestyle shocks "
        "can still derail you."
    )
else:
    verdict_bg = "#001a10"
    verdict_border = "#22cc88"
    emoji = "✅"
    headline = f"R{balance:,.0f} left — you have breathing room."
    sub = f"{pct_left:.0f}% of your income free. Build that emergency fund."

st.markdown(
    f"""
    <div style='background:{verdict_bg}; border:2px solid {verdict_border};
                border-radius:12px; padding:24px 22px; text-align:center; margin-top:18px;'>
      <div style='font-size:3rem;'>{emoji}</div>
      <div style='font-size:1.3rem; font-weight:900; color:#ffffff;
                  margin-top:8px; line-height:1.4;'>
        {headline}
      </div>
      <div style='font-size:0.9rem; color:#aaaaaa; margin-top:8px; line-height:1.5;'>
        {sub}
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

# ── Summary stats ────────────────────────────────────────────────────────────
st.markdown("<br>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)

for col, label, value, color in [
    (col1, "Total out", f"R{total_expenses:,.0f}", "#ff4444"),
    (col2, "Remaining", f"R{max(balance, 0):,.0f}", _color(balance)),
    (col3, "% free", f"{max(pct_left, 0):.0f}%", _color(balance)),
]:
    with col:
        st.markdown(
            f"""
            <div style='background:#111; border:1px solid #222; border-radius:8px;
                        padding:14px; text-align:center;'>
              <div style='font-size:0.72rem; color:#555; letter-spacing:0.12em;
                          text-transform:uppercase; margin-bottom:4px;'>{label}</div>
              <div style='font-size:1.7rem; font-weight:900; color:{color};
                          letter-spacing:-0.02em;'>{value}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

# ── Context note ─────────────────────────────────────────────────────────────
st.markdown(
    """
    <div style='margin-top:28px; padding:14px; background:#111; border-radius:8px;
                border:1px solid #1e1e1e;'>
      <div style='font-size:0.75rem; color:#444; line-height:1.7;'>
        <strong style='color:#333;'>DATA SOURCES</strong><br>
        Rent: StatsSA Housing Survey 2023 · Food: PMBEJD Basic Food Basket Dec 2024 ·
        Transport: SANTACO fare surveys 2024 · Electricity: Eskom tariff increase Apr 2024 ·
        Data: MyBroadband SA pricing index 2024. Defaults represent a single adult in a
        Gauteng township or affordable suburb.
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)
