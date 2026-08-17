import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="IN Rate Calculator",
    page_icon="📊",
    layout="wide"
)

st.title("📊 IN Rate / Risk Rate Calculator")
st.caption("Backend-driven calculator based on the handwritten rate-calculation workflow.")

# -----------------------------
# Sidebar: Backend assumptions
# -----------------------------
st.sidebar.header("⚙️ Backend Configuration")

rate_type = st.sidebar.selectbox(
    "Rate Type",
    ["IN Rate", "Risk Rate"]
)

coa_rate = st.sidebar.number_input(
    "COA Rate (%)",
    min_value=0.0,
    max_value=100.0,
    value=5.0,
    step=0.1,
    help="COA percentage added to the insurer/base rate."
)

amount_per_lakh = st.sidebar.number_input(
    "Amount per Lakh (₹)",
    min_value=0.0,
    value=100.0,
    step=1.0,
    help="Backend amount used to convert the calculated rate into an amount."
)

payout_rate = st.sidebar.number_input(
    "Payout Rate (%)",
    min_value=0.0,
    max_value=100.0,
    value=100.0,
    step=0.5,
    help="Percentage of the final calculated amount used for payout."
)

st.sidebar.divider()
st.sidebar.info(
    "The handwritten notes indicate that the rate is fixed in the backend "
    "with COA and Amount per Lakh, then payout is decided on the resulting amount."
)

# -----------------------------
# Main input
# -----------------------------
st.subheader("1. Input Received from Client")

col1, col2, col3 = st.columns(3)

with col1:
    client_input = st.number_input(
        "Client Input / Sum Insured (₹)",
        min_value=0.0,
        value=1_000_000.0,
        step=10_000.0
    )

with col2:
    insurer_rate = st.number_input(
        "Insurer Rate (%)",
        min_value=0.0,
        max_value=100.0,
        value=21.0,
        step=0.1
    )

with col3:
    insurer_amount = st.number_input(
        "Insurer Amount (₹)",
        min_value=0.0,
        value=0.0,
        step=100.0,
        help="Optional. Enter this if the insurer has supplied an absolute amount."
    )

# -----------------------------
# Calculation
# -----------------------------
# Based on the handwritten workflow:
# 1) Receive input
# 2) Calculate using insurer input/rate
# 3) Add COA
# 4) Treat resulting rate as % of input
# 5) Decide payout %
#
# Example reflected in notes: 5 + 21 = 26.

combined_rate = insurer_rate + coa_rate

# Rate-based amount
rate_amount = client_input * combined_rate / 100

# Amount-per-lakh conversion
number_of_lakhs = client_input / 100_000
backend_amount = number_of_lakhs * amount_per_lakh

# Optional insurer absolute amount comparison
if insurer_amount > 0:
    insurer_effective_rate = (insurer_amount / client_input) * 100 if client_input else 0
    difference_amount = rate_amount - insurer_amount
else:
    insurer_effective_rate = 0
    difference_amount = 0

# Payout
payout_amount = rate_amount * payout_rate / 100

# -----------------------------
# Results
# -----------------------------
st.subheader("2. Calculation Result")

m1, m2, m3, m4 = st.columns(4)

m1.metric("Insurer Rate", f"{insurer_rate:.2f}%")
m2.metric("COA Rate", f"{coa_rate:.2f}%")
m3.metric("Final / IN Rate", f"{combined_rate:.2f}%")
m4.metric("Payout Rate", f"{payout_rate:.2f}%")

st.success(
    f"Calculation: **{insurer_rate:.2f}% + {coa_rate:.2f}% = {combined_rate:.2f}%**"
)

r1, r2, r3 = st.columns(3)

r1.metric(
    "Calculated Amount",
    f"₹{rate_amount:,.2f}"
)

r2.metric(
    "Backend Amount / Lakh",
    f"₹{backend_amount:,.2f}"
)

r3.metric(
    "Final Payout",
    f"₹{payout_amount:,.2f}"
)

# -----------------------------
# Detailed calculation
# -----------------------------
st.subheader("3. Detailed Calculation")

calculation_rows = [
    ["Client Input", f"₹{client_input:,.2f}"],
    ["Insurer Rate", f"{insurer_rate:.2f}%"],
    ["COA Rate", f"{coa_rate:.2f}%"],
    ["Final / IN Rate", f"{combined_rate:.2f}%"],
    ["Calculated Amount", f"₹{rate_amount:,.2f}"],
    ["Amount per Lakh", f"₹{amount_per_lakh:,.2f}"],
    ["Number of Lakhs", f"{number_of_lakhs:,.2f}"],
    ["Backend Amount", f"₹{backend_amount:,.2f}"],
    ["Payout Rate", f"{payout_rate:.2f}%"],
    ["Payout Amount", f"₹{payout_amount:,.2f}"],
]

df = pd.DataFrame(calculation_rows, columns=["Parameter", "Value"])
st.dataframe(df, use_container_width=True, hide_index=True)

# -----------------------------
# Optional insurer comparison
# -----------------------------
if insurer_amount > 0:
    st.subheader("4. Insurer Amount Comparison")

    c1, c2, c3 = st.columns(3)
    c1.metric("Insurer Amount", f"₹{insurer_amount:,.2f}")
    c2.metric("Effective Insurer Rate", f"{insurer_effective_rate:.2f}%")
    c3.metric("Difference vs Calculated", f"₹{difference_amount:,.2f}")

# -----------------------------
# Formula reference
# -----------------------------
st.divider()
st.subheader("Formula Reference")

st.markdown(
    """
**Step 1 — Final / IN Rate**

`Final Rate = Insurer Rate + COA Rate`

**Step 2 — Calculated Amount**

`Calculated Amount = Client Input × Final Rate ÷ 100`

**Step 3 — Backend Amount**

`Backend Amount = (Client Input ÷ 1,00,000) × Amount per Lakh`

**Step 4 — Payout**

`Payout Amount = Calculated Amount × Payout Rate ÷ 100`

> Example from the notes: **5% + 21% = 26%**.
"""
)

st.warning(
    "Important: The handwritten note is partially ambiguous. The app keeps "
    "COA %, Amount/Lakh and Payout % as backend-configurable fields so the "
    "exact business rules can be changed without rewriting the calculator."
)

# -----------------------------
# Export
# -----------------------------
export_df = pd.DataFrame({
    "Client Input": [client_input],
    "Insurer Rate %": [insurer_rate],
    "COA Rate %": [coa_rate],
    "Final IN Rate %": [combined_rate],
    "Amount per Lakh": [amount_per_lakh],
    "Calculated Amount": [rate_amount],
    "Backend Amount": [backend_amount],
    "Payout Rate %": [payout_rate],
    "Payout Amount": [payout_amount],
})

csv_data = export_df.to_csv(index=False)

st.download_button(
    "⬇️ Download Calculation CSV",
    data=csv_data,
    file_name="in_rate_calculation.csv",
    mime="text/csv"
)
