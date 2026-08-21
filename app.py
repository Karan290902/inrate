import streamlit as st

# =================================================
# PAGE CONFIG
# =================================================
st.set_page_config(
    page_title="Insurance Payout Calculator",
    page_icon="🛡️",
    layout="wide"
)

# =================================================
# BACKEND PRODUCT CONFIGURATION
# =================================================
PRODUCT_CONFIG = {
    "PA": {
        "Manipal Cigna": {
            "sum_assured": 100000,
            "risk_rate_excl_gst": 24.00,
            "gst_percent": 18,
            "risk_rate_incl_gst": 28.32,
            "coa_percent": 25
        }
    }
}


# =================================================
# CUSTOM CSS
# =================================================
st.markdown("""
<style>

.stApp {
    background: linear-gradient(135deg, #f4f7fb 0%, #e9eef7 100%);
}

.main-container {
    max-width: 1100px;
    margin: auto;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    color: #12263f;
    margin-bottom: 5px;
}

.subtitle {
    font-size: 17px;
    color: #64748b;
    margin-bottom: 35px;
}

.section-card {
    background: white;
    padding: 28px;
    border-radius: 20px;
    box-shadow: 0px 8px 25px rgba(15, 23, 42, 0.08);
    margin-bottom: 25px;
}

.result-card {
    padding: 30px;
    border-radius: 22px;
    text-align: center;
    box-shadow: 0px 10px 25px rgba(15, 23, 42, 0.12);
    color: white;
    min-height: 190px;
}

.payout-card {
    background: linear-gradient(135deg, #0f766e, #14b8a6);
}

.retention-card {
    background: linear-gradient(135deg, #1e3a8a, #2563eb);
}

.result-label {
    font-size: 17px;
    opacity: 0.9;
    font-weight: 600;
    margin-bottom: 15px;
}

.result-value {
    font-size: 42px;
    font-weight: 800;
}

.result-subtext {
    font-size: 14px;
    opacity: 0.8;
    margin-top: 10px;
}

.footer-text {
    text-align: center;
    color: #94a3b8;
    font-size: 13px;
    margin-top: 30px;
}

div[data-testid="stNumberInput"] input {
    border-radius: 10px;
}

div[data-testid="stSelectbox"] {
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# =================================================
# HEADER
# =================================================
st.markdown('<div class="main-container">', unsafe_allow_html=True)

st.markdown(
    '<div class="main-title">🛡️ Insurance Payout Calculator</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">Calculate payout percentage and retention amount instantly</div>',
    unsafe_allow_html=True
)


# =================================================
# PRODUCT & INSURER SELECTION
# =================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)

st.subheader("Product Details")

col1, col2 = st.columns(2)

with col1:
    product = st.selectbox(
        "Select Product",
        options=list(PRODUCT_CONFIG.keys())
    )

with col2:
    insurer = st.selectbox(
        "Select Insurer",
        options=list(PRODUCT_CONFIG[product].keys())
    )

st.markdown('</div>', unsafe_allow_html=True)


# =================================================
# FETCH BACKEND CONFIG
# =================================================
config = PRODUCT_CONFIG[product][insurer]

SUM_ASSURED = config["sum_assured"]
RISK_RATE_EXCL_GST = config["risk_rate_excl_gst"]
GST_PERCENT = config["gst_percent"]
RISK_RATE_INCL_GST = config["risk_rate_incl_gst"]
COA_PERCENT = config["coa_percent"]

# COA is calculated only on Risk Rate excluding GST
COA_AMOUNT = RISK_RATE_EXCL_GST * (COA_PERCENT / 100)


# =================================================
# INPUT SECTION
# =================================================
st.markdown('<div class="section-card">', unsafe_allow_html=True)

st.subheader("Rate Input")

loading = st.number_input(
    "Enter Loading Amount (₹ per ₹1 Lakh SA)",
    min_value=0.0,
    value=0.0,
    step=1.0,
    help="Enter the additional loading required by the client."
)

st.caption("All insurer rates, GST and COA calculations are configured in the backend.")

st.markdown('</div>', unsafe_allow_html=True)


# =================================================
# CALCULATIONS
# =================================================

# Base risk rate + loading charged to client
final_rate = RISK_RATE_INCL_GST + loading

# Total margin available after insurer cost and COA
available_margin = (
    final_rate
    - RISK_RATE_INCL_GST
    - COA_AMOUNT
)

# For now, payout percentage is based on margin distribution
# The full available margin is treated as payout potential
payout_percent = (
    (available_margin / final_rate) * 100
    if final_rate > 0
    else 0
)

# Amount paid out
payout_amount = available_margin

# Amount retained by company
retention_amount = 0.0


# =================================================
# OUTPUT
# =================================================
st.markdown("### 💰 Calculation Result")

out1, out2 = st.columns(2)

with out1:
    st.markdown(
        f"""
        <div class="result-card payout-card">
            <div class="result-label">PAYOUT PERCENTAGE</div>
            <div class="result-value">{payout_percent:.2f}%</div>
            <div class="result-subtext">
                Payout available from the calculated margin
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with out2:
    st.markdown(
        f"""
        <div class="result-card retention-card">
            <div class="result-label">AMOUNT RETAINED BY US</div>
            <div class="result-value">₹{retention_amount:.2f}</div>
            <div class="result-subtext">
                Per ₹1 Lakh Sum Assured
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# =================================================
# INTERNAL CALCULATION EXPANDER
# =================================================
with st.expander("🔒 Internal Calculation Details"):
    st.write(f"Risk Rate Excl. GST: ₹{RISK_RATE_EXCL_GST:.2f}")
    st.write(f"Risk Rate Incl. GST: ₹{RISK_RATE_INCL_GST:.2f}")
    st.write(f"COA Amount: ₹{COA_AMOUNT:.2f}")
    st.write(f"Final Rate After Loading: ₹{final_rate:.2f}")
    st.write(f"Available Margin: ₹{available_margin:.2f}")
    st.write(f"Potential Payout Amount: ₹{payout_amount:.2f}")


# =================================================
# FOOTER
# =================================================
st.markdown(
    '<div class="footer-text">Trial Version • Insurance Rate & Payout Calculator</div>',
    unsafe_allow_html=True
)

st.markdown('</div>', unsafe_allow_html=True)
