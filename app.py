import streamlit as st
import pandas as pd

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Policygrace | Insurance In-Rate Calculator",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# BACKEND RATE MASTER
#
# insurer_base_rate = Rate excluding GST
# with_gst_rate      = Actual amount including GST
# coa_percent        = COA percentage on base rate
#
# X Amount = Client Rate - With GST Rate
# COA Amount = Base Rate × COA %
# In-Rate Amount = X Amount + COA Amount
# ============================================================

RATE_MASTER = {

    "PA": {

        "Care": {
            "insurer_base_rate": 9.00,
            "with_gst_rate": 10.62,
            "coa_percent": 8.5
        },

        "Cigna Manipal": {
            "insurer_base_rate": 24.00,
            "with_gst_rate": 28.32,
            "coa_percent": 25.0
        },

        "Aditya Birla": {
            "insurer_base_rate": 21.00,
            "with_gst_rate": 21.00,
            "coa_percent": 25.0
        }
    },


    "Hospicash": {

        "ZUNO": {
            "insurer_base_rate": 150.00,
            "with_gst_rate": 177.00,
            "coa_percent": 0.0
        }
    },


    "PA HOSPICASH": {

        "Magma": {
            "insurer_base_rate": 424.00,
            "with_gst_rate": 500.32,
            "coa_percent": 10.0
        },

        "Tata": {
            "insurer_base_rate": 169.00,
            "with_gst_rate": 199.42,
            "coa_percent": 25.0
        }
    },


    "PA + Cancer Specific": {

        "Cigna Manipal": {
            "insurer_base_rate": 180.00,
            "with_gst_rate": 212.40,
            "coa_percent": 25.0
        }
    },


    "Cancer Specific": {

        "Cigna Manipal": {
            "insurer_base_rate": 156.00,
            "with_gst_rate": 184.08,
            "coa_percent": 25.0
        }
    },


    "GTL": {

        "IPRU": {
            "insurer_base_rate": 450.00,
            "with_gst_rate": 531.00,
            "coa_percent": 0.0
        },

        "Aviva": {
            "insurer_base_rate": 320.30,
            "with_gst_rate": 377.95,
            "coa_percent": 10.0
        }
    },


    "PA + CI": {

        "Magma": {
            "insurer_base_rate": 270.00,
            "with_gst_rate": 318.60,
            "coa_percent": 10.0
        },

        "Cigna Manipal": {
            "insurer_base_rate": 368.00,
            "with_gst_rate": 434.24,
            "coa_percent": 25.0
        }
    },


    "CI": {

        "Cigna Manipal": {
            "insurer_base_rate": 344.00,
            "with_gst_rate": 405.92,
            "coa_percent": 25.0
        }
    },


    "Health": {

        "Aditya Birla": {
            "insurer_base_rate": 1879.00,
            "with_gst_rate": 2217.22,
            "coa_percent": 25.0
        },

        "18-60": {
            "insurer_base_rate": 2699.00,
            "with_gst_rate": 3184.82,
            "coa_percent": 0.0
        },

        "3369 Plan": {
            "insurer_base_rate": 3369.00,
            "with_gst_rate": 3975.42,
            "coa_percent": 0.0
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
        radial-gradient(
            circle at 5% 0%,
            rgba(37, 99, 235, 0.10),
            transparent 30%
        ),
        radial-gradient(
            circle at 95% 100%,
            rgba(16, 185, 129, 0.08),
            transparent 30%
        ),
        #f8fafc;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}


/* ============================================================
   APP HEADER
============================================================ */

.app-title {
    font-size: 36px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -1px;
    margin-bottom: 5px;
}

.app-subtitle {
    font-size: 15px;
    color: #64748b;
    margin-bottom: 35px;
}


/* ============================================================
   SECTION HEADINGS
============================================================ */

.section-kicker {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #2563eb;
    margin-bottom: 5px;
}

.section-title {
    font-size: 25px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 7px;
}

.section-description {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 18px;
}


/* ============================================================
   INPUTS
============================================================ */

div[data-testid="stSelectbox"] > div > div {
    border-radius: 10px;
}

div[data-testid="stNumberInput"] input {
    border-radius: 10px;
}

div[data-testid="stSelectbox"] label,
div[data-testid="stNumberInput"] label {
    font-weight: 700;
    color: #334155;
}


/* ============================================================
   RESULT CARDS
============================================================ */

.result-card {
    border-radius: 18px;
    padding: 24px;
    min-height: 165px;
    color: white;
    box-shadow: 0 14px 30px rgba(15, 23, 42, 0.14);
}

.with-gst-card {
    background: linear-gradient(
        135deg,
        #4338ca,
        #6366f1
    );
}

.x-card {
    background: linear-gradient(
        135deg,
        #0f766e,
        #14b8a6
    );
}

.inrate-card {
    background: linear-gradient(
        135deg,
        #c2410c,
        #f97316
    );
}

.coa-card {
    background: linear-gradient(
        135deg,
        #111827,
        #334155
    );
}

.card-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    opacity: 0.85;
    margin-bottom: 18px;
}

.card-value {
    font-size: 34px;
    font-weight: 850;
    letter-spacing: -1px;
}

.card-note {
    font-size: 12px;
    margin-top: 15px;
    opacity: 0.82;
    line-height: 1.4;
}


/* ============================================================
   FINAL RESULT
============================================================ */

.final-result {
    background: linear-gradient(
        135deg,
        #1d4ed8,
        #2563eb
    );
    color: white;
    padding: 28px;
    border-radius: 20px;
    text-align: center;
    margin-top: 25px;
    box-shadow:
        0 15px 35px
        rgba(37, 99, 235, 0.22);
}

.final-label {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.5px;
    opacity: 0.85;
}

.final-value {
    font-size: 48px;
    font-weight: 850;
    margin-top: 8px;
}


/* ============================================================
   FOOTER
============================================================ */

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 12px;
    margin-top: 20px;
}


/* ============================================================
   HIDE STREAMLIT
============================================================ */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# CALCULATION FUNCTION
# ============================================================

def calculate_inrate(
    client_rate,
    insurer_base_rate,
    with_gst_rate,
    coa_percent
):

    # --------------------------------------------------------
    # X AMOUNT
    # Client Rate - Insurer Rate Including GST
    # --------------------------------------------------------

    x_amount = (
        client_rate
        - with_gst_rate
    )


    # --------------------------------------------------------
    # COA AMOUNT
    # COA is calculated on Base Rate excluding GST
    # --------------------------------------------------------

    coa_amount = (
        insurer_base_rate
        * (coa_percent / 100)
    )


    # --------------------------------------------------------
    # IN-RATE AMOUNT
    # --------------------------------------------------------

    inrate_amount = (
        x_amount
        + coa_amount
    )


    # --------------------------------------------------------
    # FINAL IN-RATE %
    # --------------------------------------------------------

    if client_rate > 0:

        inrate_percent = (
            inrate_amount
            / client_rate
        ) * 100

    else:

        inrate_percent = 0


    return {
        "x_amount": x_amount,
        "coa_amount": coa_amount,
        "inrate_amount": inrate_amount,
        "inrate_percent": inrate_percent
    }


# ============================================================
# APP HEADER
# ============================================================

st.markdown(
    """
<div class="app-title">
    🛡️ Insurance In-Rate Calculator
</div>

<div class="app-subtitle">
    Calculate the final in-rate percentage using insurer rates including GST and COA.
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# STEP 01 - INPUT
# ============================================================

st.markdown(
    """
<div class="section-kicker">
    STEP 01
</div>

<div class="section-title">
    Calculation Input
</div>

<div class="section-description">
    Select the product and insurer, then enter the final rate charged to the client.
</div>
""",
    unsafe_allow_html=True
)


col1, col2, col3 = st.columns(3)


# ============================================================
# PRODUCT
# ============================================================

with col1:

    product = st.selectbox(
        "Product",
        list(RATE_MASTER.keys())
    )


# ============================================================
# INSURER
# ============================================================

with col2:

    insurer = st.selectbox(
        "Insurer",
        list(RATE_MASTER[product].keys())
    )


# ============================================================
# SELECT BACKEND VALUES
# ============================================================

config = RATE_MASTER[product][insurer]

insurer_base_rate = config["insurer_base_rate"]

with_gst_rate = config["with_gst_rate"]

coa_percent = config["coa_percent"]


# ============================================================
# CLIENT RATE
# ============================================================

with col3:

    client_rate = st.number_input(
        "Client Rate (₹)",
        min_value=0.0,
        value=float(with_gst_rate),
        step=1.0
    )


# ============================================================
# CALCULATE
# ============================================================

result = calculate_inrate(
    client_rate=float(client_rate),
    insurer_base_rate=float(insurer_base_rate),
    with_gst_rate=float(with_gst_rate),
    coa_percent=float(coa_percent)
)


# ============================================================
# STEP 02 - RESULTS
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown(
    """
<div class="section-kicker">
    STEP 02
</div>

<div class="section-title">
    Calculation Results
</div>

<div class="section-description">
    Your calculated in-rate result.
</div>
""",
    unsafe_allow_html=True
)


r1, r2, r3, r4 = st.columns(4)


# ============================================================
# CARD 1 - WITH GST RATE
# ============================================================

with r1:

    html = (
        f'<div class="result-card with-gst-card">'
        f'<div class="card-label">INSURER RATE WITH GST</div>'
        f'<div class="card-value">₹{with_gst_rate:,.2f}</div>'
        f'<div class="card-note">Actual insurer payment</div>'
        f'</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ============================================================
# CARD 2 - X AMOUNT
# ============================================================

with r2:

    html = (
        f'<div class="result-card x-card">'
        f'<div class="card-label">X AMOUNT</div>'
        f'<div class="card-value">₹{result["x_amount"]:,.2f}</div>'
        f'<div class="card-note">Client Rate − With GST Rate</div>'
        f'</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ============================================================
# CARD 3 - IN-RATE AMOUNT
# ============================================================

with r3:

    html = (
        f'<div class="result-card inrate-card">'
        f'<div class="card-label">IN-RATE AMOUNT</div>'
        f'<div class="card-value">₹{result["inrate_amount"]:,.2f}</div>'
        f'<div class="card-note">X Amount + COA Amount</div>'
        f'</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ============================================================
# CARD 4 - COA AMOUNT
# ============================================================

with r4:

    html = (
        f'<div class="result-card coa-card">'
        f'<div class="card-label">COA AMOUNT</div>'
        f'<div class="card-value">₹{result["coa_amount"]:,.2f}</div>'
        f'<div class="card-note">'
        f'{coa_percent:.2f}% of Base Rate'
        f'</div>'
        f'</div>'
    )

    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ============================================================
# FINAL IN-RATE PERCENTAGE
# ============================================================

final_html = (
    f'<div class="final-result">'
    f'<div class="final-label">'
    f'FINAL IN-RATE PERCENTAGE'
    f'</div>'
    f'<div class="final-value">'
    f'{result["inrate_percent"]:.2f}%'
    f'</div>'
    f'</div>'
)

st.markdown(
    final_html,
    unsafe_allow_html=True
)


# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
<div class="footer">
    Policygrace Internal Pricing Tool • Insurance In-Rate Calculator
</div>
""",
    unsafe_allow_html=True
)
