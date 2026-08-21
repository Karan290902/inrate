import streamlit as st

# -------------------------------------------------
# PAGE CONFIG
# -------------------------------------------------
st.set_page_config(
    page_title="PA Rate & Payout Calculator",
    page_icon="🛡️",
    layout="wide"
)

# -------------------------------------------------
# CUSTOM CSS
# -------------------------------------------------
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #f5f7fa 0%, #e8edf3 100%);
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #13294B;
    margin-bottom: 0px;
}

.sub-title {
    font-size: 18px;
    color: #6B7280;
    margin-bottom: 30px;
}

.section-title {
    font-size: 20px;
    font-weight: 700;
    color: #13294B;
    margin-bottom: 10px;
}

.info-card {
    background: white;
    padding: 20px;
    border-radius: 16px;
    border-left: 5px solid #2563EB;
    box-shadow: 0px 4px 15px rgba(0,0,0,0.08);
    margin-bottom: 15px;
}

.output-card {
    background: linear-gradient(135deg, #13294B, #1E40AF);
    padding: 25px;
    border-radius: 18px;
    color: white;
    box-shadow: 0px 8px 20px rgba(0,0,0,0.15);
    text-align: center;
}

.metric-label {
    font-size: 16px;
    opacity: 0.85;
}

.metric-value {
    font-size: 34px;
    font-weight: 800;
    margin-top: 8px;
}

.small-note {
    font-size: 13px;
    color: #6B7280;
}

div[data-testid="stNumberInput"] input {
    border-radius: 10px;
}

</style>
""", unsafe_allow_html=True)


# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown(
    '<div class="main-title">🛡️ PA Rate & Payout Calculator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">Calculate Payout & Retention Amount per ₹1 Lakh Sum Assured</div>',
    unsafe_allow_html=True
)


# -------------------------------------------------
# BACKEND VALUES
# -------------------------------------------------
RISK_RATE_EXCL_GST = 24.00
GST_PERCENT = 18
RISK_RATE_INCL_GST = 28.32
COA_PERCENT = 25

COA_AMOUNT = RISK_RATE_EXCL_GST * (COA_PERCENT / 100)

SUM_ASSURED = 100000


# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
with st.sidebar:

    st.header("⚙️ Product Details")

    st.success("Personal Accident (PA)")

    st.write(f"**Sum Assured:** ₹{SUM_ASSURED:,.0f}")
    st.write(f"**Risk Rate (Excl. GST):** ₹{RISK_RATE_EXCL_GST:.2f}")
    st.write(f"**GST:** {GST_PERCENT}%")
    st.write(f"**Risk Rate (Incl. GST):** ₹{RISK_RATE_INCL_GST:.2f}")
    st.write(f"**COA:** {COA_PERCENT}%")
    st.write(f"**COA Amount:** ₹{COA_AMOUNT:.2f}")

    st.caption("These values are fixed in the backend.")


# -------------------------------------------------
# INPUT SECTION
# -------------------------------------------------
st.markdown('<div class="section-title">📥 Enter Rate Details</div>', unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    in_rate = st.number_input(
        "In Rate (₹ per Lakh)",
        min_value=0.0,
        value=40.0,
        step=1.0
    )

with col2:
    loading = st.number_input(
        "Loading (₹ per Lakh)",
        min_value=0.0,
        value=0.0,
        step=1.0
    )

with col3:
    payout_percent = st.slider(
        "Payout %",
        min_value=0,
        max_value=100,
        value=50,
        step=1
    )


# -------------------------------------------------
# CALCULATIONS
# -------------------------------------------------

final_rate = in_rate + loading

available_margin = (
    final_rate
    - RISK_RATE_INCL_GST
    - COA_AMOUNT
)

payout_amount = available_margin * (payout_percent / 100)

retention_amount = available_margin - payout_amount


# -------------------------------------------------
# RATE BREAKDOWN
# -------------------------------------------------
st.markdown("---")

st.markdown(
    '<div class="section-title">📊 Rate Breakdown</div>',
    unsafe_allow_html=True
)

b1, b2, b3, b4 = st.columns(4)

b1.metric(
    "In Rate",
    f"₹{in_rate:.2f}"
)

b2.metric(
    "Loading",
    f"₹{loading:.2f}"
)

b3.metric(
    "Final Rate",
    f"₹{final_rate:.2f}",
    f"+₹{loading:.2f}"
)

b4.metric(
    "Available Margin",
    f"₹{available_margin:.2f}"
)


# -------------------------------------------------
# FINAL OUTPUT
# -------------------------------------------------
st.markdown("---")

st.markdown(
    '<div class="section-title">💰 Payout & Retention</div>',
    unsafe_allow_html=True
)

out1, out2 = st.columns(2)

with out1:
    st.markdown(
        f"""
        <div class="output-card">
            <div class="metric-label">
                PAYOUT AMOUNT ({payout_percent}%)
            </div>
            <div class="metric-value">
                ₹{payout_amount:.2f}
            </div>
            <div class="metric-label">
                Per ₹1 Lakh Sum Assured
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with out2:

    retention_percent = 100 - payout_percent

    st.markdown(
        f"""
        <div class="output-card">
            <div class="metric-label">
                RETENTION AMOUNT ({retention_percent}%)
            </div>
            <div class="metric-value">
                ₹{retention_amount:.2f}
            </div>
            <div class="metric-label">
                Per ₹1 Lakh Sum Assured
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# -------------------------------------------------
# DETAILED CALCULATION
# -------------------------------------------------
st.markdown("---")

st.markdown(
    '<div class="section-title">🧮 Detailed Calculation</div>',
    unsafe_allow_html=True
)

calculation_data = {
    "Particular": [
        "In Rate",
        "Loading",
        "Final Rate",
        "Less: Risk Rate (Incl. GST)",
        "Less: COA Amount",
        "Available Margin",
        f"Payout Amount ({payout_percent}%)",
        f"Retention Amount ({100 - payout_percent}%)"
    ],
    "Amount (₹)": [
        in_rate,
        loading,
        final_rate,
        -RISK_RATE_INCL_GST,
        -COA_AMOUNT,
        available_margin,
        payout_amount,
        retention_amount
    ]
}

st.dataframe(
    calculation_data,
    use_container_width=True,
    hide_index=True
)


# -------------------------------------------------
# WARNING
# -------------------------------------------------
if available_margin < 0:
    st.error(
        "⚠️ Negative Margin! The Final Rate is lower than the combined Risk Rate and COA."
    )

elif available_margin == 0:
    st.warning(
        "⚠️ No margin available for payout or retention."
    )

else:
    st.success(
        "✅ Calculation successful. Margin is available for Payout and Retention."
    )


# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.markdown("---")

st.caption(
    "Trial Version | Personal Accident Calculator | Rates calculated per ₹1 Lakh Sum Assured"
)
