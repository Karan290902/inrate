```python
import streamlit as st

# ============================================================
# PA RATE / PAYOUT / LOADING CALCULATOR
# ============================================================

st.set_page_config(
    page_title="Insurance Payout Calculator",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# BACKEND PRODUCT CONFIGURATION
# ============================================================
# All product pricing remains in the backend.
# Future products and insurers can be added here.

PRODUCT_CONFIG = {
    "PA": {
        "Manipal Cigna": {
            "base_rate": 28.32,              # Amount payable to insurer
            "risk_rate_excl_gst": 24.00,
            "gst_percent": 18,
            "coa_percent": 25,
            "coa_amount": 6.00,             # Received later from insurer
            "sum_assured": 100000
        }
    }
}


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* Main Background */
    .stApp {
        background:
            radial-gradient(circle at top left, #e0f2fe 0%, transparent 30%),
            radial-gradient(circle at bottom right, #dbeafe 0%, transparent 30%),
            #f8fafc;
    }

    .block-container {
        max-width: 1150px;
        padding-top: 2.5rem;
        padding-bottom: 2rem;
    }

    /* Header */
    .hero {
        background: linear-gradient(135deg, #0f172a 0%, #1e3a8a 55%, #2563eb 100%);
        padding: 32px 38px;
        border-radius: 24px;
        color: white;
        margin-bottom: 28px;
        box-shadow: 0 16px 40px rgba(30, 58, 138, 0.20);
    }

    .hero-title {
        font-size: 38px;
        font-weight: 800;
        letter-spacing: -1px;
        margin-bottom: 6px;
    }

    .hero-subtitle {
        font-size: 16px;
        opacity: 0.80;
    }

    /* Section Card */
    .input-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        box-shadow: 0 8px 30px rgba(15, 23, 42, 0.07);
        border: 1px solid #e2e8f0;
        margin-bottom: 24px;
    }

    .section-heading {
        font-size: 20px;
        font-weight: 750;
        color: #0f172a;
        margin-bottom: 18px;
    }

    /* Result Cards */
    .result-card {
        padding: 28px;
        border-radius: 22px;
        min-height: 190px;
        color: white;
        box-shadow: 0 14px 30px rgba(15, 23, 42, 0.12);
    }

    .loading-card {
        background: linear-gradient(135deg, #7c2d12, #ea580c);
    }

    .rate-card {
        background: linear-gradient(135deg, #312e81, #6366f1);
    }

    .payout-card {
        background: linear-gradient(135deg, #065f46, #10b981);
    }

    .retention-card {
        background: linear-gradient(135deg, #0f172a, #334155);
    }

    .card-label {
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 0.8px;
        opacity: 0.82;
        margin-bottom: 14px;
    }

    .card-value {
        font-size: 38px;
        font-weight: 850;
        letter-spacing: -1px;
    }

    .card-note {
        font-size: 13px;
        margin-top: 12px;
        opacity: 0.75;
        line-height: 1.4;
    }

    /* Flow Card */
    .flow-card {
        background: white;
        padding: 26px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 8px 25px rgba(15, 23, 42, 0.06);
        margin-top: 24px;
    }

    .flow-title {
        font-size: 19px;
        font-weight: 750;
        color: #0f172a;
        margin-bottom: 18px;
    }

    .formula-box {
        background: #f8fafc;
        border-left: 4px solid #2563eb;
        padding: 16px;
        border-radius: 10px;
        color: #334155;
        font-size: 14px;
        margin-top: 12px;
    }

    /* Input styling */
    div[data-testid="stSelectbox"] > div > div,
    div[data-testid="stNumberInput"] input {
        border-radius: 10px;
    }

    /* Hide Streamlit Branding */
    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="hero">
    <div class="hero-title">🛡️ Insurance Payout Calculator</div>
    <div class="hero-subtitle">
        Calculate the required loading while safeguarding insurer payment and your COA retention.
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# PRODUCT SELECTION
# ============================================================

st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">📋 Product Configuration</div>', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    product = st.selectbox(
        "Product",
        options=list(PRODUCT_CONFIG.keys())
    )

with col2:
    insurer = st.selectbox(
        "Insurer",
        options=list(PRODUCT_CONFIG[product].keys())
    )

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# FETCH BACKEND CONFIG
# ============================================================

config = PRODUCT_CONFIG[product][insurer]

BASE_RATE = config["base_rate"]
COA_AMOUNT = config["coa_amount"]
SUM_ASSURED = config["sum_assured"]


# ============================================================
# USER INPUT
# ============================================================

st.markdown('<div class="input-card">', unsafe_allow_html=True)
st.markdown('<div class="section-heading">🎯 Payout Requirement</div>', unsafe_allow_html=True)

payout_percent = st.number_input(
    "Required Payout Percentage (%)",
    min_value=0.0,
    max_value=95.0,
    value=20.0,
    step=1.0,
    help="Enter the payout percentage requested by the client."
)

st.caption(
    "The calculator automatically calculates the loading required. "
    "Insurer payment and your COA retention remain safeguarded."
)

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# CALCULATIONS
# ============================================================

payout_decimal = payout_percent / 100

# Prevent division by zero
if payout_decimal < 1:

    # Final rate required to provide requested payout
    # Formula:
    # Final Rate = Base Insurer Rate / (1 - Payout %)
    final_client_rate = BASE_RATE / (1 - payout_decimal)

    # Additional amount to be loaded
    required_loading = final_client_rate - BASE_RATE

    # Amount paid as payout
    payout_amount = final_client_rate * payout_decimal

    # Insurer payment remains fully protected
    insurer_payment = BASE_RATE

    # COA is received separately/later from insurer
    retention_amount = COA_AMOUNT

else:
    final_client_rate = 0
    required_loading = 0
    payout_amount = 0
    insurer_payment = 0
    retention_amount = 0


# ============================================================
# RESULT HEADER
# ============================================================

st.markdown("### 📊 Calculation Results")

# ============================================================
# TOP RESULT CARDS
# ============================================================

r1, r2, r3, r4 = st.columns(4)

with r1:
    st.markdown(
        f"""
        <div class="result-card loading-card">
            <div class="card-label">REQUIRED LOADING</div>
            <div class="card-value">₹{required_loading:.2f}</div>
            <div class="card-note">
                Additional rate required per ₹1 lakh SA
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with r2:
    st.markdown(
        f"""
        <div class="result-card rate-card">
            <div class="card-label">FINAL CLIENT RATE</div>
            <div class="card-value">₹{final_client_rate:.2f}</div>
            <div class="card-note">
                Base rate + calculated loading
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with r3:
    st.markdown(
        f"""
        <div class="result-card payout-card">
            <div class="card-label">PAYOUT AMOUNT</div>
            <div class="card-value">₹{payout_amount:.2f}</div>
            <div class="card-note">
                {payout_percent:.2f}% of final client rate
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


with r4:
    st.markdown(
        f"""
        <div class="result-card retention-card">
            <div class="card-label">AMOUNT RETAINED BY US</div>
            <div class="card-value">₹{retention_amount:.2f}</div>
            <div class="card-note">
                COA received separately from insurer
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PAYMENT FLOW
# ============================================================

st.markdown("""
<div class="flow-card">
    <div class="flow-title">🔄 Premium & Payment Flow</div>
</div>
""", unsafe_allow_html=True)

f1, f2, f3, f4 = st.columns(4)

with f1:
    st.metric(
        "Client Pays",
        f"₹{final_client_rate:.2f}"
    )

with f2:
    st.metric(
        "Payout Given",
        f"₹{payout_amount:.2f}",
        f"{payout_percent:.2f}%"
    )

with f3:
    st.metric(
        "Paid to Insurer",
        f"₹{insurer_payment:.2f}"
    )

with f4:
    st.metric(
        "COA Retained by Us",
        f"₹{retention_amount:.2f}"
    )


# ============================================================
# VALIDATION
# ============================================================

difference = final_client_rate - payout_amount - insurer_payment

if abs(difference) < 0.01:
    st.success(
        "✓ Calculation is balanced. Insurer payment is fully safeguarded, "
        "and the COA remains separately retained by us."
    )
else:
    st.warning(
        "Please review the calculation."
    )


# ============================================================
# OPTIONAL BACKEND DETAILS
# ============================================================

with st.expander("🔒 Backend Product Details"):

    st.write(f"**Product:** {product}")
    st.write(f"**Insurer:** {insurer}")
    st.write(f"**Sum Assured:** ₹{SUM_ASSURED:,.0f}")
    st.write(f"**Base Rate Payable to Insurer:** ₹{BASE_RATE:.2f}")
    st.write(f"**COA Received Later:** ₹{COA_AMOUNT:.2f}")

    st.info(
        "Backend rates can be expanded later by adding more products "
        "and insurers to PRODUCT_CONFIG."
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Trial Version • PA | Manipal Cigna • All calculations shown per ₹1 Lakh Sum Assured"
)
```
