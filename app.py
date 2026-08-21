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
# COA % IS KEPT INTERNAL
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
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

    /* ------------------------------
       MAIN APPLICATION
    ------------------------------ */

    .stApp {
        background: #f4f7fb;
    }

    .block-container {
        max-width: 1400px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
    }


    /* ------------------------------
       HIDE STREAMLIT ELEMENTS
    ------------------------------ */

    #MainMenu {
        visibility: hidden;
    }

    footer {
        visibility: hidden;
    }

    header {
        background: transparent !important;
    }


    /* ------------------------------
       TOP HEADER
    ------------------------------ */

    .dashboard-header {
        background: linear-gradient(
            135deg,
            #111827 0%,
            #1e293b 55%,
            #2563eb 100%
        );
        border-radius: 22px;
        padding: 30px 36px;
        margin-bottom: 26px;
        box-shadow: 0 16px 35px rgba(15, 23, 42, 0.18);
    }

    .dashboard-badge {
        display: inline-block;
        background: rgba(255,255,255,0.12);
        border: 1px solid rgba(255,255,255,0.18);
        color: #dbeafe;
        padding: 6px 12px;
        border-radius: 30px;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: 1.4px;
        margin-bottom: 12px;
    }

    .dashboard-title {
        color: white;
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -0.8px;
        margin-bottom: 6px;
    }

    .dashboard-subtitle {
        color: #cbd5e1;
        font-size: 14px;
        line-height: 1.6;
    }


    /* ------------------------------
       SECTION HEADINGS
    ------------------------------ */

    .section-label {
        color: #2563eb;
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.8px;
        margin-bottom: 5px;
    }

    .section-title {
        color: #172033;
        font-size: 23px;
        font-weight: 800;
        margin-bottom: 4px;
    }

    .section-subtitle {
        color: #64748b;
        font-size: 13px;
        margin-bottom: 16px;
    }


    /* ------------------------------
       INPUT PANEL
    ------------------------------ */

    .input-panel {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 18px;
        padding: 22px;
        box-shadow: 0 8px 24px rgba(15, 23, 42, 0.05);
        margin-bottom: 24px;
    }


    /* ------------------------------
       STREAMLIT INPUTS
    ------------------------------ */

    div[data-baseweb="select"] > div {
        border-radius: 10px;
    }

    .stNumberInput input {
        border-radius: 10px;
    }


    /* ------------------------------
       RESULT KPI CARDS
    ------------------------------ */

    .kpi-card {
        border-radius: 18px;
        padding: 22px;
        min-height: 155px;
        color: white;
        position: relative;
        overflow: hidden;
        box-shadow: 0 12px 28px rgba(15, 23, 42, 0.12);
    }

    .kpi-card::after {
        content: "";
        position: absolute;
        width: 100px;
        height: 100px;
        border-radius: 50%;
        right: -35px;
        top: -35px;
        background: rgba(255,255,255,0.10);
    }

    .kpi-purple {
        background: linear-gradient(
            135deg,
            #3730a3,
            #6366f1
        );
    }

    .kpi-teal {
        background: linear-gradient(
            135deg,
            #0f766e,
            #14b8a6
        );
    }

    .kpi-orange {
        background: linear-gradient(
            135deg,
            #c2410c,
            #f97316
        );
    }

    .kpi-dark {
        background: linear-gradient(
            135deg,
            #1e293b,
            #475569
        );
    }

    .kpi-label {
        font-size: 10px;
        font-weight: 800;
        letter-spacing: 1.3px;
        opacity: 0.85;
        margin-bottom: 22px;
    }

    .kpi-value {
        font-size: 31px;
        font-weight: 800;
        letter-spacing: -0.5px;
        position: relative;
        z-index: 2;
    }

    .kpi-note {
        font-size: 11px;
        margin-top: 18px;
        opacity: 0.78;
        position: relative;
        z-index: 2;
    }


    /* ------------------------------
       FINAL RESULT
    ------------------------------ */

    .final-result-card {
        background: linear-gradient(
            135deg,
            #1e40af,
            #2563eb,
            #3b82f6
        );
        border-radius: 22px;
        padding: 30px;
        text-align: center;
        color: white;
        margin-top: 22px;
        box-shadow: 0 18px 40px rgba(37, 99, 235, 0.24);
    }

    .final-result-label {
        font-size: 11px;
        font-weight: 800;
        letter-spacing: 1.8px;
        opacity: 0.85;
    }

    .final-result-value {
        font-size: 52px;
        font-weight: 850;
        margin-top: 8px;
    }

    .final-result-note {
        font-size: 12px;
        opacity: 0.82;
        margin-top: 5px;
    }


    /* ------------------------------
       INFO STRIP
    ------------------------------ */

    .info-strip {
        background: #ecfdf5;
        border: 1px solid #bbf7d0;
        color: #166534;
        border-radius: 12px;
        padding: 14px 18px;
        font-size: 13px;
        margin-top: 18px;
    }


    /* ------------------------------
       FOOTER
    ------------------------------ */

    .footer {
        text-align: center;
        color: #94a3b8;
        font-size: 11px;
        margin-top: 32px;
        padding-bottom: 10px;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# HELPER FUNCTION
# ============================================================

def render_html(html):
    st.markdown(html, unsafe_allow_html=True)


# ============================================================
# CALCULATION ENGINE
# ============================================================

def calculate_inrate(
    client_rate,
    base_rate,
    gross_rate,
    coa_percent
):

    # ========================================================
    # CLIENT RATE ENTERED
    #
    # X AMOUNT =
    # (CLIENT RATE - INSURER GROSS RATE) / 1.18
    # ========================================================

    if client_rate > 0:

        difference = client_rate - gross_rate

        x_amount = difference / 1.18

        x_note = "Additional amount excluding 18% GST"

        denominator_rate = client_rate


    # ========================================================
    # CLIENT RATE NOT ENTERED
    #
    # X AMOUNT =
    # INSURER GROSS RATE / 1.18
    #
    # SHOW NET AMOUNT EXCLUDING GST
    # ========================================================

    else:

        x_amount = gross_rate / 1.18

        difference = gross_rate

        x_note = "Net insurer amount excluding 18% GST"

        denominator_rate = gross_rate


    # ========================================================
    # COA AMOUNT
    # INTERNAL BACKEND CALCULATION
    # ========================================================

    coa_amount = (
        base_rate *
        (coa_percent / 100)
    )


    # ========================================================
    # TOTAL IN-RATE AMOUNT
    # ========================================================

    inrate_amount = (
        x_amount +
        coa_amount
    )


    # ========================================================
    # FINAL IN-RATE %
    # ========================================================

    if denominator_rate > 0:

        inrate_percent = (
            inrate_amount /
            denominator_rate
        ) * 100

    else:

        inrate_percent = 0.0


    return {
        "difference": difference,
        "x_amount": x_amount,
        "coa_amount": coa_amount,
        "inrate_amount": inrate_amount,
        "inrate_percent": inrate_percent,
        "x_note": x_note
    }


# ============================================================
# DASHBOARD HEADER
# ============================================================

render_html("""
<div class="dashboard-header">

    <div class="dashboard-badge">
        POLICYGRACE • INTERNAL PRICING TOOL
    </div>

    <div class="dashboard-title">
        Insurance In-Rate Calculator
    </div>

    <div class="dashboard-subtitle">
        Analyse insurer pricing, client rates and internal in-rate
        calculations in one professional dashboard.
    </div>

</div>
""")


# ============================================================
# PRODUCT & INSURER SELECTION
# ============================================================

render_html("""
<div class="section-label">CONFIGURATION</div>
<div class="section-title">Select Product & Insurer</div>
<div class="section-subtitle">
Choose the product and insurer to load the configured backend pricing.
</div>
""")


input_container = st.container()

with input_container:

    left, right = st.columns(2)

    with left:

        product = st.selectbox(
            "Product",
            list(RATE_MASTER.keys())
        )

    with right:

        insurer = st.selectbox(
            "Insurer",
            list(RATE_MASTER[product].keys())
        )


# ============================================================
# GET BACKEND CONFIG
# ============================================================

config = RATE_MASTER[product][insurer]

base_rate = config.get("base_rate")

gross_rate = config.get("gross_rate")

coa_percent = config.get(
    "coa_percent",
    0.0
)

variable_rate = config.get(
    "variable_rate",
    False
)


# ============================================================
# VARIABLE RATE HANDLING
# ============================================================

if variable_rate:

    st.warning(
        "This product has a variable rate based on age and loan tenure."
    )

    st.stop()


# ============================================================
# CLIENT RATE INPUT
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

render_html("""
<div class="section-label">CLIENT PRICING</div>
<div class="section-title">Enter Client Rate</div>
<div class="section-subtitle">
Enter the rate proposed to the client. Leave it at ₹0 to view the
net insurer rate excluding GST.
</div>
""")


client_rate = st.number_input(
    "Client Rate (₹)",
    min_value=0.0,
    value=0.0,
    step=1.0,
    format="%.2f"
)


# ============================================================
# RUN CALCULATION
# ============================================================

result = calculate_inrate(
    client_rate=float(client_rate),
    base_rate=float(base_rate),
    gross_rate=float(gross_rate),
    coa_percent=float(coa_percent)
)


# ============================================================
# RESULTS SECTION
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

render_html("""
<div class="section-label">CALCULATION RESULTS</div>
<div class="section-title">Pricing Dashboard</div>
<div class="section-subtitle">
Live calculation based on the selected insurer and client rate.
</div>
""")


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)


# ------------------------------------------------------------
# INSURER GROSS RATE
# ------------------------------------------------------------

with c1:

    render_html(f"""
    <div class="kpi-card kpi-purple">

        <div class="kpi-label">
            INSURER GROSS RATE
        </div>

        <div class="kpi-value">
            ₹{gross_rate:,.2f}
        </div>

        <div class="kpi-note">
            Insurer payment including GST
        </div>

    </div>
    """)


# ------------------------------------------------------------
# X AMOUNT
# ------------------------------------------------------------

with c2:

    render_html(f"""
    <div class="kpi-card kpi-teal">

        <div class="kpi-label">
            X AMOUNT
        </div>

        <div class="kpi-value">
            ₹{result["x_amount"]:,.2f}
        </div>

        <div class="kpi-note">
            {result["x_note"]}
        </div>

    </div>
    """)


# ------------------------------------------------------------
# IN-RATE AMOUNT
# ------------------------------------------------------------

with c3:

    render_html(f"""
    <div class="kpi-card kpi-orange">

        <div class="kpi-label">
            IN-RATE AMOUNT
        </div>

        <div class="kpi-value">
            ₹{result["inrate_amount"]:,.2f}
        </div>

        <div class="kpi-note">
            X Amount + Internal COA
        </div>

    </div>
    """)


# ------------------------------------------------------------
# COA AMOUNT
# ------------------------------------------------------------

with c4:

    render_html(f"""
    <div class="kpi-card kpi-dark">

        <div class="kpi-label">
            COA AMOUNT
        </div>

        <div class="kpi-value">
            ₹{result["coa_amount"]:,.2f}
        </div>

        <div class="kpi-note">
            Calculated from backend configuration
        </div>

    </div>
    """)


# ============================================================
# FINAL IN-RATE PERCENTAGE
# ============================================================

render_html(f"""
<div class="final-result-card">

    <div class="final-result-label">
        FINAL IN-RATE PERCENTAGE
    </div>

    <div class="final-result-value">
        {result["inrate_percent"]:.2f}%
    </div>

    <div class="final-result-note">
        Calculated automatically based on the selected pricing structure
    </div>

</div>
""")


# ============================================================
# STATUS MESSAGE
# ============================================================

if client_rate > 0:

    render_html(f"""
    <div class="info-strip">
        ✓ Client rate has been considered. The additional amount above
        the insurer gross rate is converted to a net amount after
        removing 18% GST.
    </div>
    """)

else:

    render_html(f"""
    <div class="info-strip">
        ✓ No client rate entered. X Amount currently displays the
        insurer gross rate converted to the net amount excluding 18% GST.
    </div>
    """)


# ============================================================
# FOOTER
# ============================================================

render_html("""
<div class="footer">
    POLICYGRACE INSURANCE BROKING • INTERNAL USE ONLY
</div>
""")
