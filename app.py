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
# DATA FROM SHEET2 ONLY
# ============================================================

PRODUCT_CONFIG = {
    "PA": {
        "Care": {
            "risk_rate": 12.00,
            "insurer_payment": 14.16,
            "coa_percent": 8.5,
        },
        "Cigna Manipal": {
            "risk_rate": 24.00,
            "insurer_payment": 28.32,
            "coa_percent": 25.0,
        },
        "Aditya Birla": {
            "risk_rate": 25.00,
            "insurer_payment": 25.00,
            "coa_percent": 25.0,
        },
    },

    "PA HOSPICASH": {
        "Magma": {
            "risk_rate": 466.40,
            "insurer_payment": 550.35,
            "coa_percent": 10.0,
        },
        "Tata": {
            "risk_rate": 169.00,
            "insurer_payment": 199.42,
            "coa_percent": 25.0,
        },
    },

    "PA + Cancer Specific": {
        "Cigna Manipal": {
            "risk_rate": 180.00,
            "insurer_payment": 212.40,
            "coa_percent": 25.0,
        },
    },

    "Cancer Specific": {
        "Cigna Manipal": {
            "risk_rate": 156.00,
            "insurer_payment": 184.08,
            "coa_percent": 25.0,
        },
    },

    "GTL": {
        "Aviva": {
            "risk_rate": 650.00,
            "insurer_payment": 767.00,
            "coa_percent": 10.0,
        },
    },

    "PA + CI": {
        "Magma": {
            "risk_rate": 300.00,
            "insurer_payment": 354.00,
            "coa_percent": 10.0,
        },
        "Cigna Manipal": {
            "risk_rate": 368.00,
            "insurer_payment": 434.24,
            "coa_percent": 25.0,
        },
    },

    "CI": {
        "Cigna Manipal": {
            "risk_rate": 344.00,
            "insurer_payment": 405.92,
            "coa_percent": 25.0,
        },
    },
}


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 10% 0%, rgba(37, 99, 235, 0.10), transparent 30%),
        radial-gradient(circle at 90% 90%, rgba(16, 185, 129, 0.08), transparent 30%),
        #f8fafc;
}

.block-container {
    max-width: 1150px;
    padding-top: 2.5rem;
}


/* TITLE */

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
    margin-bottom: 35px;
}


/* SECTION */

.section-kicker {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.3px;
    color: #2563eb;
    margin-bottom: 5px;
}

.section-title {
    font-size: 25px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 8px;
}

.section-description {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 18px;
}


/* INPUTS */

div[data-testid="stSelectbox"] > div > div {
    border-radius: 10px;
}

div[data-testid="stNumberInput"] input {
    border-radius: 10px;
}

div[data-testid="stNumberInput"] label,
div[data-testid="stSelectbox"] label {
    font-weight: 700;
}


/* RESULT CARDS */

.result-card {
    border-radius: 20px;
    padding: 24px;
    min-height: 175px;
    color: white;
    box-shadow: 0 14px 30px rgba(15, 23, 42, 0.12);
}

.client-card {
    background: linear-gradient(135deg, #4338ca, #6366f1);
}

.payout-card {
    background: linear-gradient(135deg, #047857, #10b981);
}

.retention-card {
    background: linear-gradient(135deg, #c2410c, #f97316);
}

.total-card {
    background: linear-gradient(135deg, #111827, #334155);
}

.card-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    opacity: 0.85;
    margin-bottom: 16px;
}

.card-value {
    font-size: 35px;
    font-weight: 850;
    letter-spacing: -1px;
}

.card-note {
    font-size: 12px;
    margin-top: 15px;
    opacity: 0.80;
}


/* HIDE STREAMLIT BRANDING */

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
    Calculate client pricing, payout and retention instantly.
</div>
""", unsafe_allow_html=True)


# ============================================================
# STEP 01 - PRODUCT & INSURER
# ============================================================

st.markdown("""
<div class="section-kicker">STEP 01</div>
<div class="section-title">Select Product & Insurer</div>
<div class="section-description">
Choose the product and insurer.
</div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    product = st.selectbox(
        "Select Product",
        list(PRODUCT_CONFIG.keys())
    )

with col2:
    insurer = st.selectbox(
        "Select Insurer",
        list(PRODUCT_CONFIG[product].keys())
    )


# ============================================================
# BACKEND VALUES
# ============================================================

config = PRODUCT_CONFIG[product][insurer]

risk_rate = config["risk_rate"]
insurer_payment = config["insurer_payment"]
coa_percent = config["coa_percent"]

coa_amount = risk_rate * (coa_percent / 100)


# ============================================================
# STEP 02 - INPUT
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="section-kicker">STEP 02</div>
<div class="section-title">Enter Client Pricing & Payout</div>
<div class="section-description">
Enter the final client rate and desired payout percentage.
</div>
""", unsafe_allow_html=True)

input1, input2 = st.columns(2)

with input1:
    client_rate = st.number_input(
        "Final Rate Charged to Client (₹)",
        min_value=0.0,
        value=float(insurer_payment),
        step=1.0
    )

with input2:
    payout_percent = st.number_input(
        "Payout Percentage (%)",
        min_value=0.0,
        max_value=100.0,
        value=10.0,
        step=1.0
    )


# ============================================================
# CALCULATIONS
# ============================================================

payout_amount = client_rate * (payout_percent / 100)

extra_retention = (
    client_rate
    - payout_amount
    - insurer_payment
)

total_retention = (
    extra_retention
    + coa_amount
)


# ============================================================
# STEP 03 - RESULTS
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="section-kicker">STEP 03</div>
<div class="section-title">Calculation Results</div>
<div class="section-description">
Instant payout and retention calculation.
</div>
""", unsafe_allow_html=True)

r1, r2, r3, r4 = st.columns(4)

with r1:
    st.markdown(
        f"""
        <div class="result-card client-card">
            <div class="card-label">CLIENT RATE</div>
            <div class="card-value">₹{client_rate:.2f}</div>
            <div class="card-note">Final rate charged to client</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with r2:
    st.markdown(
        f"""
        <div class="result-card payout-card">
            <div class="card-label">PAYOUT AMOUNT</div>
            <div class="card-value">₹{payout_amount:.2f}</div>
            <div class="card-note">{payout_percent:.0f}% payout</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with r3:
    st.markdown(
        f"""
        <div class="result-card retention-card">
            <div class="card-label">EXTRA RETENTION</div>
            <div class="card-value">₹{extra_retention:.2f}</div>
            <div class="card-note">After payout & insurer payment</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with r4:
    st.markdown(
        f"""
        <div class="result-card total-card">
            <div class="card-label">TOTAL RETENTION</div>
            <div class="card-value">₹{total_retention:.2f}</div>
            <div class="card-note">Includes fixed COA</div>
        </div>
        """,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Policygrace Internal Pricing Tool • Rates configured from Sheet2"
)
