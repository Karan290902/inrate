import streamlit as st

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Policygrace | Rate & Retention Calculator",
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

/* =========================================================
   GLOBAL
========================================================= */

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(37, 99, 235, 0.10), transparent 30%),
        radial-gradient(circle at 90% 90%, rgba(16, 185, 129, 0.08), transparent 30%),
        #f8fafc;
}

.block-container {
    max-width: 1250px;
    padding-top: 2.5rem;
    padding-bottom: 3rem;
}


/* =========================================================
   APP TITLE
========================================================= */

.app-title {
    font-size: 36px;
    font-weight: 850;
    color: #0f172a;
    letter-spacing: -1px;
    margin-bottom: 6px;
}

.app-subtitle {
    font-size: 16px;
    color: #64748b;
    margin-bottom: 32px;
}


/* =========================================================
   SECTION HEADINGS
========================================================= */

.section-kicker {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.3px;
    color: #2563eb;
    margin-bottom: 6px;
}

.section-title {
    font-size: 28px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 6px;
}

.section-description {
    font-size: 15px;
    color: #64748b;
    margin-bottom: 20px;
}


/* =========================================================
   INPUT CARDS
========================================================= */

.input-card {
    background: rgba(255, 255, 255, 0.97);
    padding: 30px;
    border-radius: 22px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
    margin-bottom: 32px;
}


/* =========================================================
   RESULT CARDS
========================================================= */

.result-card {
    border-radius: 22px;
    padding: 27px;
    min-height: 210px;
    color: white;
    box-shadow: 0 16px 35px rgba(15, 23, 42, 0.14);
    position: relative;
    overflow: hidden;
}

.result-card::after {
    content: "";
    position: absolute;
    width: 140px;
    height: 140px;
    border-radius: 50%;
    background: rgba(255, 255, 255, 0.08);
    right: -45px;
    top: -45px;
}

.client-card {
    background: linear-gradient(135deg, #4338ca, #6366f1);
}

.payout-card {
    background: linear-gradient(135deg, #047857, #10b981);
}

.extra-retention-card {
    background: linear-gradient(135deg, #c2410c, #f97316);
}

.total-retention-card {
    background: linear-gradient(135deg, #111827, #334155);
}

.card-icon {
    font-size: 28px;
    margin-bottom: 15px;
}

.card-label {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1px;
    opacity: 0.82;
    margin-bottom: 13px;
}

.card-value {
    font-size: 39px;
    font-weight: 850;
    letter-spacing: -1px;
    line-height: 1;
}

.card-note {
    font-size: 13px;
    margin-top: 17px;
    opacity: 0.80;
    line-height: 1.5;
}


/* =========================================================
   PAYMENT FLOW
========================================================= */

.flow-card {
    background: white;
    padding: 30px;
    border-radius: 22px;
    border: 1px solid #e2e8f0;
    box-shadow: 0 10px 30px rgba(15, 23, 42, 0.06);
}


/* =========================================================
   SUMMARY
========================================================= */

.summary-card {
    background: white;
    padding: 28px;
    border-radius: 20px;
    border: 1px solid #e2e8f0;
    min-height: 220px;
    box-shadow: 0 8px 25px rgba(15, 23, 42, 0.05);
}


/* =========================================================
   INPUT STYLING
========================================================= */

div[data-testid="stSelectbox"] > div > div {
    border-radius: 12px;
}

div[data-testid="stNumberInput"] input {
    border-radius: 12px;
    font-size: 16px;
}

div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label {
    font-weight: 700;
    color: #334155;
}


/* =========================================================
   STREAMLIT BRANDING
========================================================= */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# APP TITLE
# ============================================================

st.markdown("""
<div class="app-title">
    🛡️ Insurance Rate & Retention Calculator
</div>

<div class="app-subtitle">
    Analyse client pricing, payout and retention while safeguarding insurer payments.
</div>
""", unsafe_allow_html=True)


# ============================================================
# STEP 01 - PRODUCT & INSURER
# ============================================================

st.markdown("""
<div class="section-kicker">STEP 01</div>
<div class="section-title">Select Product & Insurer</div>
<div class="section-description">
Choose the product and insurer for which you want to calculate pricing,
payout and retention.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="input-card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    product = st.selectbox(
        "🛡️ Select Product",
        options=list(PRODUCT_CONFIG.keys())
    )

with col2:
    insurer = st.selectbox(
        "🏢 Select Insurer",
        options=list(PRODUCT_CONFIG[product].keys())
    )

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# BACKEND VALUES
# ============================================================

config = PRODUCT_CONFIG[product][insurer]

INSURER_PAYMENT = config["insurer_payment"]
COA_AMOUNT = config["coa_amount"]
SUM_ASSURED = config["sum_assured"]


# ============================================================
# STEP 02 - CLIENT PRICING & PAYOUT
# ============================================================

st.markdown("""
<div class="section-kicker">STEP 02</div>
<div class="section-title">Enter Client Pricing & Payout</div>
<div class="section-description">
Enter the final rate you are willing to charge the client and
the payout percentage you wish to provide.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="input-card">', unsafe_allow_html=True)

input1, input2 = st.columns(2)

with input1:
    st.markdown("#### 💰 Client Pricing")

    client_rate = st.number_input(
        "Final Rate Charged to Client (₹ per ₹1 Lakh SA)",
        min_value=0.0,
        value=35.40,
        step=0.50
    )

with input2:
    st.markdown("#### 🤝 Payout Requirement")

    payout_percent = st.number_input(
        "Payout Percentage (%)",
        min_value=0.0,
        max_value=100.0,
        value=20.0,
        step=1.0
    )

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# CALCULATIONS
# ============================================================

payout_decimal = payout_percent / 100

payout_amount = client_rate * payout_decimal

extra_retention = (
    client_rate
    - payout_amount
    - INSURER_PAYMENT
)

total_retention = extra_retention + COA_AMOUNT


# ============================================================
# STEP 03 - CALCULATION RESULTS
# ============================================================

st.markdown("""
<div class="section-kicker">STEP 03</div>
<div class="section-title">Calculation Results</div>
<div class="section-description">
Review the financial outcome based on the selected client rate
and payout percentage.
</div>
""", unsafe_allow_html=True)

r1, r2, r3, r4 = st.columns(4)

with r1:
    st.markdown(
        f"""
        <div class="result-card client-card">
            <div class="card-icon">💰</div>
            <div class="card-label">CLIENT RATE</div>
            <div class="card-value">₹{client_rate:.2f}</div>
            <div class="card-note">
                Final price charged per ₹1 Lakh SA
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with r2:
    st.markdown(
        f"""
        <div class="result-card payout-card">
            <div class="card-icon">🤝</div>
            <div class="card-label">PAYOUT AMOUNT</div>
            <div class="card-value">₹{payout_amount:.2f}</div>
            <div class="card-note">
                {payout_percent:.2f}% of the client rate
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with r3:
    st.markdown(
        f"""
        <div class="result-card extra-retention-card">
            <div class="card-icon">📈</div>
            <div class="card-label">EXTRA RETENTION</div>
            <div class="card-value">₹{extra_retention:.2f}</div>
            <div class="card-note">
                Amount retained after payout and insurer payment
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with r4:
    st.markdown(
        f"""
        <div class="result-card total-retention-card">
            <div class="card-icon">🏆</div>
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
# STEP 04 - PAYMENT FLOW
# ============================================================

st.markdown("""
<div style="margin-top:40px;">
    <div class="section-kicker">STEP 04</div>
    <div class="section-title">Premium & Payment Flow</div>
    <div class="section-description">
        Understand exactly how the client premium is distributed.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="flow-card">', unsafe_allow_html=True)

f1, f2, f3, f4, f5 = st.columns(5)

with f1:
    st.metric("💳 Client Pays", f"₹{client_rate:.2f}")

with f2:
    st.metric(
        "🤝 Payout",
        f"₹{payout_amount:.2f}",
        f"{payout_percent:.0f}%"
    )

with f3:
    st.metric(
        "🏢 Insurer Payment",
        f"₹{INSURER_PAYMENT:.2f}"
    )

with f4:
    st.metric(
        "📈 Extra Retention",
        f"₹{extra_retention:.2f}"
    )

with f5:
    st.metric(
        "🛡️ Fixed COA",
        f"₹{COA_AMOUNT:.2f}"
    )

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# PAYMENT SAFETY CHECK
# ============================================================

st.markdown("### 🔍 Payment Safety Check")

balance = client_rate - payout_amount - INSURER_PAYMENT

if balance < 0:
    st.error(
        f"""
        ⚠️ Insufficient Client Rate

        After providing the payout, the remaining premium is insufficient
        to fully cover the insurer payment of ₹{INSURER_PAYMENT:.2f}.
        """
    )
else:
    st.success(
        f"""
        ✅ Insurer Payment Safeguarded

        The insurer payment of ₹{INSURER_PAYMENT:.2f} is fully covered.
        ₹{extra_retention:.2f} remains as additional retention, while
        ₹{COA_AMOUNT:.2f} is received separately as fixed COA.
        """
    )


# ============================================================
# STEP 05 - DETAILED CALCULATION SUMMARY
# ============================================================

st.markdown("""
<div style="margin-top:35px;">
    <div class="section-kicker">STEP 05</div>
    <div class="section-title">Detailed Calculation Summary</div>
    <div class="section-description">
        Complete premium movement and retention breakdown.
    </div>
</div>
""", unsafe_allow_html=True)

summary1, summary2 = st.columns(2)

with summary1:
    st.markdown('<div class="summary-card">', unsafe_allow_html=True)

    st.markdown("### 💳 Premium Flow")
    st.write(f"**Client Rate Charged:** ₹{client_rate:.2f}")
    st.write(f"**Less: Payout Amount:** ₹{payout_amount:.2f}")
    st.write(f"**Less: Insurer Payment:** ₹{INSURER_PAYMENT:.2f}")

    st.markdown('</div>', unsafe_allow_html=True)

with summary2:
    st.markdown('<div class="summary-card">', unsafe_allow_html=True)

    st.markdown("### 🏆 Retention Flow")
    st.write(f"**Extra Retention:** ₹{extra_retention:.2f}")
    st.write(f"**Fixed COA Received Later:** ₹{COA_AMOUNT:.2f}")
    st.write(f"**Total Retention:** ₹{total_retention:.2f}")

    st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# PRODUCT CONFIGURATION
# ============================================================

st.markdown("### ⚙️ Product Configuration")

with st.expander("View Backend Product Details"):

    b1, b2, b3 = st.columns(3)

    with b1:
        st.write("**Product**")
        st.write(product)

    with b2:
        st.write("**Insurer**")
        st.write(insurer)

    with b3:
        st.write("**Sum Assured**")
        st.write(f"₹{SUM_ASSURED:,.0f}")

    st.divider()

    st.write(
        f"**Amount Payable to Insurer:** ₹{INSURER_PAYMENT:.2f}"
    )

    st.write(
        f"**Fixed COA Received Later:** ₹{COA_AMOUNT:.2f}"
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Policygrace Internal Pricing Tool • PA | Manipal Cigna • Calculations per ₹1 Lakh Sum Assured"
)
