import streamlit as st

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
# COA % IS INTERNAL ONLY
# ============================================================

RATE_MASTER = {

    "PA": {
        "Care": {
            "base_rate": 9.00,
            "gross_rate": 11.00,
            "coa_percent": 8.5
        },
        "Cigna Manipal": {
            "base_rate": 24.00,
            "gross_rate": 28.00,
            "coa_percent": 25.0
        },
        "Aditya Birla": {
            "base_rate": 21.00,
            "gross_rate": 25.00,
            "coa_percent": 25.0
        }
    },

    "Hospicash": {
        "ZUNO": {
            "base_rate": 150.00,
            "gross_rate": 177.00,
            "coa_percent": 0.0
        },
        "Hospicash Rate 280": {
            "base_rate": 280.00,
            "gross_rate": 330.00,
            "coa_percent": 0.0
        }
    },

    "PA HOSPICASH": {
        "Magma (18-60)": {
            "base_rate": 424.00,
            "gross_rate": 500.00,
            "coa_percent": 10.0
        },
        "Tata": {
            "base_rate": 169.00,
            "gross_rate": 200.00,
            "coa_percent": 25.0
        }
    },

    "PA + Cancer Specific": {
        "Cigna Manipal": {
            "base_rate": 180.00,
            "gross_rate": 212.00,
            "coa_percent": 25.0
        }
    },

    "Cancer Specific": {
        "Cigna Manipal": {
            "base_rate": 156.00,
            "gross_rate": 184.00,
            "coa_percent": 25.0
        }
    },

    "GTL": {
        "IPRU": {
            "base_rate": 450.00,
            "gross_rate": 531.00,
            "coa_percent": 0.0
        },
        "Aviva": {
            "base_rate": 320.30,
            "gross_rate": 378.00,
            "coa_percent": 10.0
        }
    },

    "PA + CI": {
        "Magma": {
            "base_rate": 270.00,
            "gross_rate": 319.00,
            "coa_percent": 10.0
        },
        "Cigna Manipal": {
            "base_rate": 368.00,
            "gross_rate": 434.00,
            "coa_percent": 25.0
        }
    },

    "GCL": {
        "Digit": {
            "base_rate": None,
            "gross_rate": None,
            "coa_percent": 32.5,
            "variable_rate": True
        },
        "Aviva (HL & LAP)": {
            "base_rate": None,
            "gross_rate": None,
            "coa_percent": 10.0,
            "variable_rate": True
        }
    },

    "CI": {
        "Cigna Manipal": {
            "base_rate": 344.00,
            "gross_rate": 406.00,
            "coa_percent": 25.0
        }
    },

    "Health": {
        "Aditya Birla": {
            "base_rate": 1879.00,
            "gross_rate": 2217.00,
            "coa_percent": 25.0
        },
        "Health 18-60": {
            "base_rate": 2699.00,
            "gross_rate": 3185.00,
            "coa_percent": 0.0
        },
        "Health Rate 3369": {
            "base_rate": 3369.00,
            "gross_rate": 3975.00,
            "coa_percent": 0.0
        }
    }
}


# ============================================================
# CALCULATION ENGINE
# ============================================================

def calculate_inrate(
    client_rate,
    base_rate,
    gross_rate,
    coa_percent
):

    # --------------------------------------------------------
    # CASE 1: CLIENT RATE ENTERED
    # --------------------------------------------------------
    # X Amount = (Client Rate - Insurer Gross Rate) / 1.18

    if client_rate > 0:

        difference = client_rate - gross_rate

        x_amount = difference / 1.18

        x_note = "Additional amount excluding 18% GST"

        denominator = client_rate

    # --------------------------------------------------------
    # CASE 2: CLIENT RATE NOT ENTERED
    # --------------------------------------------------------
    # X Amount = Gross Rate / 1.18
    # Shows net insurer amount excluding GST

    else:

        x_amount = gross_rate / 1.18

        x_note = "Net insurer amount excluding 18% GST"

        denominator = gross_rate

    # --------------------------------------------------------
    # COA AMOUNT
    # --------------------------------------------------------

    coa_amount = base_rate * (coa_percent / 100)

    # --------------------------------------------------------
    # IN-RATE AMOUNT
    # --------------------------------------------------------

    inrate_amount = x_amount + coa_amount

    # --------------------------------------------------------
    # FINAL IN-RATE %
    # --------------------------------------------------------

    if denominator > 0:

        inrate_percentage = (
            inrate_amount / denominator
        ) * 100

    else:

        inrate_percentage = 0.0

    return {
        "x_amount": x_amount,
        "coa_amount": coa_amount,
        "inrate_amount": inrate_amount,
        "inrate_percentage": inrate_percentage,
        "x_note": x_note
    }


# ============================================================
# PROFESSIONAL CSS
# ============================================================

st.markdown("""
<style>

    .stApp {
        background-color: #f3f6fb;
    }

    .block-container {
        max-width: 1350px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }

    /* HEADER */

    .top-header {
        background: linear-gradient(135deg, #172033, #243b64);
        padding: 30px 35px;
        border-radius: 20px;
        margin-bottom: 28px;
        box-shadow: 0px 15px 35px rgba(15, 23, 42, 0.18);
    }

    .header-badge {
        color: #bfdbfe;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin-bottom: 10px;
    }

    .header-title {
        color: white;
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .header-subtitle {
        color: #cbd5e1;
        font-size: 14px;
    }

    /* SECTION */

    .section-label {
        color: #2563eb;
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.5px;
    }

    .section-title {
        color: #1e293b;
        font-size: 24px;
        font-weight: 800;
        margin-top: 4px;
    }

    .section-text {
        color: #64748b;
        font-size: 13px;
        margin-bottom: 18px;
    }

    /* KPI CARDS */

    .metric-card {
        padding: 22px;
        border-radius: 18px;
        min-height: 145px;
        color: white;
        box-shadow: 0px 10px 25px rgba(15, 23, 42, 0.12);
        margin-bottom: 10px;
    }

    .metric-purple {
        background: linear-gradient(135deg, #4338ca, #6366f1);
    }

    .metric-green {
        background: linear-gradient(135deg, #0f766e, #14b8a6);
    }

    .metric-orange {
        background: linear-gradient(135deg, #c2410c, #f97316);
    }

    .metric-dark {
        background: linear-gradient(135deg, #1e293b, #475569);
    }

    .metric-label {
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1px;
        opacity: 0.85;
        margin-bottom: 20px;
    }

    .metric-value {
        font-size: 30px;
        font-weight: 800;
    }

    .metric-note {
        font-size: 11px;
        margin-top: 16px;
        opacity: 0.82;
    }

    /* FINAL RESULT */

    .final-card {
        background: linear-gradient(135deg, #1d4ed8, #2563eb);
        padding: 32px;
        border-radius: 22px;
        text-align: center;
        color: white;
        margin-top: 22px;
        box-shadow: 0px 15px 35px rgba(37, 99, 235, 0.22);
    }

    .final-label {
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.8px;
        opacity: 0.85;
    }

    .final-value {
        font-size: 52px;
        font-weight: 800;
        margin-top: 8px;
    }

    .final-note {
        font-size: 12px;
        opacity: 0.8;
        margin-top: 6px;
    }

    /* FOOTER */

    .app-footer {
        text-align: center;
        color: #94a3b8;
        font-size: 11px;
        margin-top: 35px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.markdown("""
<div class="top-header">
    <div class="header-badge">
        POLICYGRACE • INTERNAL PRICING TOOL
    </div>

    <div class="header-title">
        Insurance In-Rate Calculator
    </div>

    <div class="header-subtitle">
        Analyse insurer pricing, client rates and internal in-rate calculations.
    </div>
</div>
""", unsafe_allow_html=True)


# ============================================================
# PRODUCT SELECTION
# ============================================================

st.markdown("""
<div class="section-label">CONFIGURATION</div>
<div class="section-title">Select Product & Insurer</div>
<div class="section-text">
    Select the product and insurer to load backend pricing.
</div>
""", unsafe_allow_html=True)


col1, col2 = st.columns(2)


with col1:

    product = st.selectbox(
        "Product",
        options=list(RATE_MASTER.keys())
    )


with col2:

    insurer = st.selectbox(
        "Insurer",
        options=list(RATE_MASTER[product].keys())
    )


# ============================================================
# BACKEND CONFIG
# ============================================================

config = RATE_MASTER[product][insurer]

base_rate = config.get("base_rate")

gross_rate = config.get("gross_rate")

coa_percent = config.get("coa_percent", 0)

variable_rate = config.get("variable_rate", False)


# ============================================================
# VARIABLE RATE PRODUCTS
# ============================================================

if variable_rate:

    st.warning(
        "This product has a variable rate based on age and loan tenure. "
        "A fixed calculation is not currently configured."
    )

    st.stop()


# ============================================================
# CLIENT RATE
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="section-label">CLIENT PRICING</div>
<div class="section-title">Enter Client Rate</div>
<div class="section-text">
    Enter the final rate to be charged to the client. Leave ₹0 to view
    the insurer net amount excluding GST.
</div>
""", unsafe_allow_html=True)


client_rate = st.number_input(
    "Client Rate (₹)",
    min_value=0.0,
    value=0.0,
    step=1.0,
    format="%.2f"
)


# ============================================================
# CALCULATE
# ============================================================

result = calculate_inrate(
    client_rate=float(client_rate),
    base_rate=float(base_rate),
    gross_rate=float(gross_rate),
    coa_percent=float(coa_percent)
)


# ============================================================
# RESULTS
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

st.markdown("""
<div class="section-label">CALCULATION RESULTS</div>
<div class="section-title">Pricing Dashboard</div>
<div class="section-text">
    Live results based on the selected insurer and client rate.
</div>
""", unsafe_allow_html=True)


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.markdown(f"""
    <div class="metric-card metric-purple">
        <div class="metric-label">
            INSURER GROSS RATE
        </div>

        <div class="metric-value">
            ₹{gross_rate:,.2f}
        </div>

        <div class="metric-note">
            Insurer payment including GST
        </div>
    </div>
    """, unsafe_allow_html=True)


with c2:

    st.markdown(f"""
    <div class="metric-card metric-green">
        <div class="metric-label">
            X AMOUNT
        </div>

        <div class="metric-value">
            ₹{result["x_amount"]:,.2f}
        </div>

        <div class="metric-note">
            {result["x_note"]}
        </div>
    </div>
    """, unsafe_allow_html=True)


with c3:

    st.markdown(f"""
    <div class="metric-card metric-orange">
        <div class="metric-label">
            IN-RATE AMOUNT
        </div>

        <div class="metric-value">
            ₹{result["inrate_amount"]:,.2f}
        </div>

        <div class="metric-note">
            X Amount + Internal COA
        </div>
    </div>
    """, unsafe_allow_html=True)


with c4:

    st.markdown(f"""
    <div class="metric-card metric-dark">
        <div class="metric-label">
            COA AMOUNT
        </div>

        <div class="metric-value">
            ₹{result["coa_amount"]:,.2f}
        </div>

        <div class="metric-note">
            Internal backend calculation
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# FINAL IN-RATE
# ============================================================

st.markdown(f"""
<div class="final-card">

    <div class="final-label">
        FINAL IN-RATE PERCENTAGE
    </div>

    <div class="final-value">
        {result["inrate_percentage"]:.2f}%
    </div>

    <div class="final-note">
        Calculated automatically based on the current pricing structure
    </div>

</div>
""", unsafe_allow_html=True)


# ============================================================
# FOOTER
# ============================================================

st.markdown("""
<div class="app-footer">
    POLICYGRACE INSURANCE BROKING • INTERNAL USE ONLY
</div>
""", unsafe_allow_html=True)
