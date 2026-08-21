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

    /* --------------------------------------------------------
       GLOBAL
    --------------------------------------------------------- */

    .stApp {
        background:
            radial-gradient(circle at 10% 0%, rgba(37, 99, 235, 0.12), transparent 30%),
            radial-gradient(circle at 90% 90%, rgba(16, 185, 129, 0.10), transparent 30%),
            #f8fafc;
    }

    .block-container {
        max-width: 1250px;
        padding-top: 2.2rem;
        padding-bottom: 3rem;
    }

    /* --------------------------------------------------------
       HERO HEADER
    --------------------------------------------------------- */

    .hero {
        background: linear-gradient(
            135deg,
            #0b1220 0%,
            #172554 45%,
            #1d4ed8 100%
        );

        padding: 38px 42px;
        border-radius: 28px;
        color: white;
        margin-bottom: 30px;

        box-shadow:
            0 20px 45px rgba(30, 58, 138, 0.25);
    }

    .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.18);
        padding: 7px 14px;
        border-radius: 30px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.8px;
        margin-bottom: 14px;
    }

    .hero-title {
        font-size: 42px;
        font-weight: 850;
        letter-spacing: -1.2px;
        margin-bottom: 10px;
    }

    .hero-subtitle {
        font-size: 17px;
        opacity: 0.82;
        max-width: 750px;
        line-height: 1.6;
    }


    /* --------------------------------------------------------
       SECTION HEADINGS
    --------------------------------------------------------- */

    .section-kicker {
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1.2px;
        color: #2563eb;
        margin-bottom: 5px;
    }

    .section-title {
        font-size: 27px;
        font-weight: 800;
        color: #0f172a;
        margin-bottom: 5px;
    }

    .section-description {
        color: #64748b;
        font-size: 15px;
        margin-bottom: 18px;
    }


    /* --------------------------------------------------------
       INPUT CARDS
    --------------------------------------------------------- */

    .input-card {
        background: rgba(255,255,255,0.95);
        padding: 28px;
        border-radius: 22px;

        border: 1px solid #e2e8f0;

        box-shadow:
            0 10px 30px rgba(15, 23, 42, 0.06);

        margin-bottom: 28px;
    }


    /* --------------------------------------------------------
       RESULT CARDS
    --------------------------------------------------------- */

    .result-card {
        border-radius: 22px;
        padding: 26px;
        min-height: 200px;
        color: white;

        box-shadow:
            0 16px 35px rgba(15, 23, 42, 0.14);

        position: relative;
        overflow: hidden;
    }

    .result-card::after {
        content: "";
        position: absolute;
        width: 130px;
        height: 130px;
        border-radius: 50%;
        background: rgba(255,255,255,0.08);
        right: -40px;
        top: -40px;
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
        font-size: 26px;
        margin-bottom: 14px;
    }

    .card-label {
        font-size: 12px;
        font-weight: 800;
        letter-spacing: 1px;
        opacity: 0.82;
        margin-bottom: 12px;
    }

    .card-value {
        font-size: 38px;
        font-weight: 850;
        letter-spacing: -1px;
        line-height: 1;
    }

    .card-note {
        font-size: 13px;
        margin-top: 16px;
        opacity: 0.78;
        line-height: 1.5;
    }


    /* --------------------------------------------------------
       PAYMENT FLOW
    --------------------------------------------------------- */

    .flow-card {
        background: white;
        padding: 28px;
        border-radius: 22px;
        border: 1px solid #e2e8f0;

        box-shadow:
            0 10px 30px rgba(15, 23, 42, 0.06);

        margin-top: 25px;
    }


    /* --------------------------------------------------------
       CALCULATION SUMMARY
    --------------------------------------------------------- */

    .summary-card {
        background: white;
        padding: 25px;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
    }


    /* --------------------------------------------------------
       INPUT IMPROVEMENTS
    --------------------------------------------------------- */

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


    /* --------------------------------------------------------
       HIDE STREAMLIT BRANDING
    --------------------------------------------------------- */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# HERO SECTION
# ============================================================

st.markdown("""
<div class="hero">

    <div class="hero-badge">
        POLICYGRACE • INTERNAL CALCULATOR
    </div>

    <div class="hero-title">
        🛡️ Insurance Rate & Retention Calculator
    </div>

    <div class="hero-subtitle">
        Calculate payout, insurer payment and total retention instantly.
        Safeguard the insurer premium while analysing additional retention
        generated through client pricing.
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# PRODUCT & INSURER SECTION
# ============================================================

st.markdown("""
<div class="section-kicker">STEP 01</div>
<div class="section-title">Select Product & Insurer</div>
<div class="section-description">
Choose the product configuration for which you want to calculate payout and retention.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="input-card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    product = st.selectbox(
        "🛡️ Product",
        options=list(PRODUCT_CONFIG.keys())
    )

with col2:
    insurer = st.selectbox(
        "🏢 Insurer",
        options=list(PRODUCT_CONFIG[product].keys())
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
# PRICING & PAYOUT INPUT SECTION
# ============================================================

st.markdown("""
<div class="section-kicker">STEP 02</div>
<div class="section-title">Enter Client Pricing & Payout</div>
<div class="section-description">
Enter the final price you are willing to charge the client and the payout percentage to be given.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="input-card">', unsafe_allow_html=True)

input1, input2 = st.columns(2)

with input1:

    st.markdown("#### 💰 Client Rate")

    client_rate = st.number_input(
        "Final Rate Charged to Client (₹ per ₹1 Lakh SA)",
        min_value=0.0,
        value=35.40,
        step=0.50,
        help="Enter the final premium/rate you plan to charge."
    )

with input2:

    st.markdown("#### 🤝 Payout")

    payout_percent = st.number_input(
        "Payout Percentage (%)",
        min_value=0.0,
        max_value=100.0,
        value=20.0,
        step=1.0,
        help="Enter the percentage you want to provide as payout."
    )

st.markdown('</div>', unsafe_allow_html=True)


# ============================================================
# CALCULATIONS
# ============================================================

payout_decimal = payout_percent / 100

# Payout amount
payout_amount = client_rate * payout_decimal

# Amount retained from current client premium
extra_retention = (
    client_rate
    - payout_amount
    - INSURER_PAYMENT
)

# Total retention includes extra retention + COA received later
total_retention = extra_retention + COA_AMOUNT


# ============================================================
# RESULTS SECTION
# ============================================================

st.markdown("""
<div class="section-kicker">STEP 03</div>
<div class="section-title">Calculation Results</div>
<div class="section-description">
A complete view of client pricing, payout and your retention.
</div>
""", unsafe_allow_html=True)


r1, r2, r3, r4 = st.columns(4)


# CLIENT RATE CARD
with r1:

    st.markdown(
        f"""
        <div class="result-card client-card">

            <div class="card-icon">💰</div>

            <div class="card-label">
                CLIENT RATE
            </div>

            <div class="card-value">
                ₹{client_rate:.2f}
            </div>

            <div class="card-note">
                Final price charged per ₹1 Lakh SA
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# PAYOUT CARD
with r2:

    st.markdown(
        f"""
        <div class="result-card payout-card">

            <div class="card-icon">🤝</div>

            <div class="card-label">
                PAYOUT AMOUNT
            </div>

            <div class="card-value">
                ₹{payout_amount:.2f}
            </div>

            <div class="card-note">
                {payout_percent:.2f}% of the client rate
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# EXTRA RETENTION CARD
with r3:

    st.markdown(
        f"""
        <div class="result-card extra-retention-card">

            <div class="card-icon">📈</div>

            <div class="card-label">
                EXTRA RETENTION
            </div>

            <div class="card-value">
                ₹{extra_retention:.2f}
            </div>

            <div class="card-note">
                Retention generated above insurer payment
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


# TOTAL RETENTION CARD
with r4:

    st.markdown(
        f"""
        <div class="result-card total-retention-card">

            <div class="card-icon">🏆</div>

            <div class="card-label">
                TOTAL RETENTION
            </div>

            <div class="card-value">
                ₹{total_retention:.2f}
            </div>

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

st.markdown("""
<div class="section-kicker" style="margin-top:35px;">STEP 04</div>
<div class="section-title">Premium & Payment Flow</div>
<div class="section-description">
Understand exactly how the premium is distributed.
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="flow-card">', unsafe_allow_html=True)

f1, f2, f3, f4, f5 = st.columns(5)

with f1:
    st.metric(
        "💳 Client Pays",
        f"₹{client_rate:.2f}"
    )

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
# VALIDATION
# ============================================================

balance = client_rate - payout_amount - INSURER_PAYMENT

st.markdown("### 🔍 Payment Safety Check")

if balance < 0:

    st.error(
        f"""
        ⚠️ **Insufficient Client Rate**

        After providing the payout, the remaining premium is insufficient
        to fully cover the insurer payment of ₹{INSURER_PAYMENT:.2f}.
        """
    )

else:

    st.success(
        f"""
        ✅ **Payment Safeguarded**

        The insurer payment of ₹{INSURER_PAYMENT:.2f} is fully covered.
        The remaining ₹{extra_retention:.2f} becomes additional retention,
        while the fixed COA of ₹{COA_AMOUNT:.2f} is received later.
        """
    )


# ============================================================
# DETAILED CALCULATION SUMMARY
# ============================================================

st.markdown("""
<div class="section-kicker" style="margin-top:35px;">STEP 05</div>
<div class="section-title">Detailed Calculation Summary</div>
<div class="section-description">
A transparent breakdown of premium movement and retention.
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
# BACKEND DETAILS
# ============================================================

with st.expander("🔒 View Backend Product Configuration"):

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

    st.write(f"**Amount Payable to Insurer:** ₹{INSURER_PAYMENT:.2f}")
    st.write(f"**Fixed COA Received Later:** ₹{COA_AMOUNT:.2f}")


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Policygrace Internal Tool • PA | Manipal Cigna • Calculations per ₹1 Lakh Sum Assured"
)
