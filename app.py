import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Insurance Rate & Retention Calculator",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# BACKEND PRODUCT CONFIGURATION
# ============================================================

PRODUCT_CONFIG = {
    "PA": {
        "Manipal Cigna": {
            "insurer_payment": 28.32,
            "coa_amount": 6.00,
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
        radial-gradient(circle at bottom right, #ede9fe 0%, transparent 30%),
        #f8fafc;
}

.block-container {
    max-width: 1200px;
    padding-top: 2.5rem;
}

/* HEADER */

.hero {
    background: linear-gradient(135deg, #0f172a, #1e3a8a, #2563eb);
    padding: 35px 40px;
    border-radius: 24px;
    color: white;
    margin-bottom: 28px;
    box-shadow: 0 16px 40px rgba(30, 58, 138, 0.20);
}

.hero-title {
    font-size: 40px;
    font-weight: 800;
    margin-bottom: 8px;
}

.hero-subtitle {
    font-size: 16px;
    opacity: 0.82;
}

/* INPUT CARD */

.input-card {
    background: white;
    padding: 26px;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 8px 25px rgba(15, 23, 42, 0.06);
    margin-bottom: 24px;
}

.section-heading {
    font-size: 21px;
    font-weight: 750;
    color: #0f172a;
    margin-bottom: 18px;
}

/* RESULT CARDS */

.result-card {
    padding: 28px;
    border-radius: 22px;
    min-height: 185px;
    color: white;
    box-shadow: 0 14px 30px rgba(15, 23, 42, 0.12);
}

.client-card {
    background: linear-gradient(135deg, #312e81, #6366f1);
}

.payout-card {
    background: linear-gradient(135deg, #065f46, #10b981);
}

.retention-card {
    background: linear-gradient(135deg, #7c2d12, #ea580c);
}

.total-retention-card {
    background: linear-gradient(135deg, #0f172a, #334155);
}

.card-label {
    font-size: 13px;
    font-weight: 700;
    letter-spacing: 0.8px;
    opacity: 0.82;
    margin-bottom: 15px;
}

.card-value {
    font-size: 36px;
    font-weight: 850;
}

.card-note {
    font-size: 13px;
    margin-top: 12px;
    opacity: 0.78;
}

/* FLOW CARD */

.flow-card {
    background: white;
    padding: 26px;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 8px 25px rgba(15, 23, 42, 0.06);
    margin-top: 25px;
}

/* INPUT STYLING */

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
    <div class="hero-title">🛡️ Insurance Rate & Retention Calculator</div>
    <div class="hero-subtitle">
        Calculate payout and total retention while safeguarding insurer payment.
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# PRODUCT & INSURER SELECTION
# ============================================================

st.markdown('<div class="input-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="section-heading">📋 Product Details</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:
    product = st.selectbox(
        "Product",
        list(PRODUCT_CONFIG.keys())
    )

with col2:
    insurer = st.selectbox(
        "Insurer",
        list(PRODUCT_CONFIG[product].keys())
    )

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# FETCH BACKEND VALUES
# ============================================================

config = PRODUCT_CONFIG[product][insurer]

INSURER_PAYMENT = config["insurer_payment"]
COA_AMOUNT = config["coa_amount"]
SUM_ASSURED = config["sum_assured"]


# ============================================================
# USER INPUTS
# ============================================================

st.markdown('<div class="input-card">', unsafe_allow_html=True)

st.markdown(
    '<div class="section-heading">🎯 Pricing & Payout</div>',
    unsafe_allow_html=True
)

input1, input2 = st.columns(2)

with input1:
    client_rate = st.number_input(
        "Client Rate (₹ per ₹1 Lakh SA)",
        min_value=0.0,
        value=35.40,
        step=0.50,
        help="Enter the final rate you are willing to charge the client."
    )

with input2:
    payout_percent = st.number_input(
        "Payout (%)",
        min_value=0.0,
        max_value=100.0,
        value=20.0,
        step=1.0,
        help="Enter the payout percentage to be given."
    )

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# CALCULATIONS
# ============================================================

payout_decimal = payout_percent / 100

# Payout given to the client / partner
payout_amount = client_rate * payout_decimal

# Amount left after payout and insurer payment
extra_retention = (
    client_rate
    - payout_amount
    - INSURER_PAYMENT
)

# Total retention includes:
# 1. Extra retention from the client rate
# 2. Fixed COA received later from insurer
total_retention = extra_retention + COA_AMOUNT


# ============================================================
# RESULTS
# ============================================================

st.markdown("## 📊 Calculation Results")

r1, r2, r3, r4 = st.columns(4)


# CLIENT RATE
with r1:
    st.markdown(
        f"""
        <div class="result-card client-card">
            <div class="card-label">CLIENT RATE</div>
            <div class="card-value">₹{client_rate:.2f}</div>
            <div class="card-note">
                Final price charged per ₹1 Lakh SA
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# PAYOUT
with r2:
    st.markdown(
        f"""
        <div class="result-card payout-card">
            <div class="card-label">PAYOUT AMOUNT</div>
            <div class="card-value">₹{payout_amount:.2f}</div>
            <div class="card-note">
                {payout_percent:.2f}% of client rate
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# EXTRA RETENTION
with r3:
    st.markdown(
        f"""
        <div class="result-card retention-card">
            <div class="card-label">EXTRA RETENTION</div>
            <div class="card-value">₹{extra_retention:.2f}</div>
            <div class="card-note">
                Amount retained after payout and insurer payment
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )


# TOTAL RETENTION
with r4:
    st.markdown(
        f"""
        <div class="result-card total-retention-card">
            <div class="card-label">TOTAL RETENTION</div>
            <div class="card-value">₹{total_retention:.2f}</div>
            <div class="card-note">
                Extra retention + ₹{COA_AMOUNT:.2f} fixed COA
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

f1, f2, f3, f4, f5 = st.columns(5)

with f1:
    st.metric(
        "Client Pays",
        f"₹{client_rate:.2f}"
    )

with f2:
    st.metric(
        "Payout",
        f"₹{payout_amount:.2f}",
        f"{payout_percent:.0f}%"
    )

with f3:
    st.metric(
        "Paid to Insurer",
        f"₹{INSURER_PAYMENT:.2f}"
    )

with f4:
    st.metric(
        "Extra Retention",
        f"₹{extra_retention:.2f}"
    )

with f5:
    st.metric(
        "COA Received Later",
        f"₹{COA_AMOUNT:.2f}"
    )

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# VALIDATION
# ============================================================

balance = client_rate - payout_amount - INSURER_PAYMENT

if balance < 0:
    st.error(
        "⚠️ Insufficient client rate. After the payout, the full insurer payment of "
        f"₹{INSURER_PAYMENT:.2f} is not covered."
    )
else:
    st.success(
        "✓ Insurer payment is fully safeguarded. Any remaining amount increases your retention."
    )


# ============================================================
# CALCULATION SUMMARY
# ============================================================

st.markdown("### 📑 Calculation Summary")

summary_col1, summary_col2 = st.columns(2)

with summary_col1:
    st.write("**Premium Flow**")
    st.write(f"Client Rate: ₹{client_rate:.2f}")
    st.write(f"Less Payout: ₹{payout_amount:.2f}")
    st.write(f"Less Insurer Payment: ₹{INSURER_PAYMENT:.2f}")

with summary_col2:
    st.write("**Retention Flow**")
    st.write(f"Extra Retention: ₹{extra_retention:.2f}")
    st.write(f"Fixed COA: ₹{COA_AMOUNT:.2f}")
    st.write(f"Total Retention: ₹{total_retention:.2f}")


# ============================================================
# BACKEND DETAILS
# ============================================================

with st.expander("🔒 Backend Details"):

    st.write(f"**Product:** {product}")
    st.write(f"**Insurer:** {insurer}")
    st.write(f"**Sum Assured:** ₹{SUM_ASSURED:,.0f}")
    st.write(f"**Amount Payable to Insurer:** ₹{INSURER_PAYMENT:.2f}")
    st.write(f"**Fixed COA Received Later:** ₹{COA_AMOUNT:.2f}")


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Trial Version • PA | Manipal Cigna • Calculations per ₹1 Lakh Sum Assured"
)
