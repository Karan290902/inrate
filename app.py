import streamlit as st

# ============================================================
# PAGE CONFIG
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
# Add more products and insurers here in the future.

PRODUCT_CONFIG = {
    "PA": {
        "Manipal Cigna": {
            "insurer_rate": 28.32,   # Amount payable to insurer
            "coa_amount": 6.00,      # Received later from insurer
            "sum_assured": 100000
        }
    }
}


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

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

/* HERO */
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
    margin-bottom: 6px;
}

.hero-subtitle {
    font-size: 16px;
    opacity: 0.82;
}

/* INPUT CARD */
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

/* RESULT CARDS */
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
}

.card-note {
    font-size: 13px;
    margin-top: 12px;
    opacity: 0.78;
    line-height: 1.4;
}

/* FLOW CARD */
.flow-card {
    background: white;
    padding: 25px;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 8px 25px rgba(15, 23, 42, 0.06);
    margin-top: 24px;
}

/* INPUT STYLING */
div[data-testid="stSelectbox"] > div > div,
div[data-testid="stNumberInput"] input {
    border-radius: 10px;
}

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
        Calculate the required loading to provide the requested payout
        while safeguarding the insurer payment and your COA.
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# PRODUCT & INSURER
# ============================================================

st.markdown('<div class="input-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="section-heading">📋 Product Configuration</div>',
    unsafe_allow_html=True
)

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
# BACKEND VALUES
# ============================================================

config = PRODUCT_CONFIG[product][insurer]

INSURER_RATE = config["insurer_rate"]
COA_AMOUNT = config["coa_amount"]
SUM_ASSURED = config["sum_assured"]


# ============================================================
# PAYOUT INPUT
# ============================================================

st.markdown('<div class="input-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="section-heading">🎯 Client Payout Requirement</div>',
    unsafe_allow_html=True
)

payout_percent = st.number_input(
    "Requested Payout (%)",
    min_value=0.0,
    max_value=95.0,
    value=20.0,
    step=1.0,
    help="Enter the payout percentage requested by the client."
)

st.caption(
    "The required loading is automatically calculated. "
    "Insurer payment and COA are kept protected."
)

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# CALCULATIONS
# ============================================================

payout_decimal = payout_percent / 100

# Formula:
# Final Client Rate = Insurer Rate / (1 - Payout %)

final_client_rate = INSURER_RATE / (1 - payout_decimal)

# Additional loading required above insurer rate
required_loading = final_client_rate - INSURER_RATE

# Payout amount
payout_amount = final_client_rate * payout_decimal

# Insurer payment remains fixed
insurer_payment = INSURER_RATE

# COA received later from insurer
retention_amount = COA_AMOUNT


# ============================================================
# RESULTS
# ============================================================

st.markdown("## 📊 Calculation Results")

r1, r2, r3, r4 = st.columns(4)


# REQUIRED LOADING
with r1:
    st.markdown(
        f"""
        <div class="result-card loading-card">
            <div class="card-label">REQUIRED LOADING</div>
            <div class="card-value">₹{required_loading:.2f}</div>
            <div class="card-note">
                Additional rate required per ₹1 Lakh SA
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# FINAL CLIENT RATE
with r2:
    st.markdown(
        f"""
        <div class="result-card rate-card">
            <div class="card-label">FINAL CLIENT RATE</div>
            <div class="card-value">₹{final_client_rate:.2f}</div>
            <div class="card-note">
                Total rate charged to the client
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# PAYOUT
with r3:
    st.markdown(
        f"""
        <div class="result-card payout-card">
            <div class="card-label">PAYOUT AMOUNT</div>
            <div class="card-value">₹{payout_amount:.2f}</div>
            <div class="card-note">
                {payout_percent:.2f}% payout per ₹1 Lakh SA
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# RETENTION
with r4:
    st.markdown(
        f"""
        <div class="result-card retention-card">
            <div class="card-label">AMOUNT RETAINED BY US</div>
            <div class="card-value">₹{retention_amount:.2f}</div>
            <div class="card-note">
                COA received later from the insurer
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# PAYMENT FLOW
# ============================================================

st.markdown('<div class="flow-card">', unsafe_allow_html=True)

st.markdown("### 🔄 Payment Flow")

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
        f"{payout_percent:.0f}%"
    )

with f3:
    st.metric(
        "Paid to Insurer",
        f"₹{insurer_payment:.2f}"
    )

with f4:
    st.metric(
        "COA Received Later",
        f"₹{retention_amount:.2f}"
    )

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# VALIDATION
# ============================================================

balance_check = final_client_rate - payout_amount - insurer_payment

if abs(balance_check) < 0.01:
    st.success(
        "✓ Calculation balanced successfully. "
        "The full insurer payment is safeguarded, and your COA remains intact."
    )
else:
    st.warning("Please review the calculation.")


# ============================================================
# BACKEND DETAILS
# ============================================================

with st.expander("🔒 Backend Details"):

    st.write(f"**Product:** {product}")
    st.write(f"**Insurer:** {insurer}")
    st.write(f"**Sum Assured:** ₹{SUM_ASSURED:,.0f}")
    st.write(f"**Amount Payable to Insurer:** ₹{INSURER_RATE:.2f}")
    st.write(f"**COA Received Later:** ₹{COA_AMOUNT:.2f}")


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Trial Version • PA | Manipal Cigna • Calculations per ₹1 Lakh Sum Assured"
)
