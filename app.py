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
# COA % IS HIDDEN FROM DROPDOWN
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

.stApp {
    background: #f8fafc;
}

.block-container {
    max-width: 1250px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.app-title {
    font-size: 36px;
    font-weight: 800;
    color: #172033;
    margin-bottom: 4px;
}

.app-subtitle {
    font-size: 15px;
    color: #64748b;
    margin-bottom: 32px;
}

.section-kicker {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.8px;
    color: #2563eb;
    margin-bottom: 6px;
}

.section-title {
    font-size: 25px;
    font-weight: 800;
    color: #172033;
    margin-bottom: 6px;
}

.section-description {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 20px;
}

.result-card {
    border-radius: 18px;
    padding: 24px;
    min-height: 155px;
    color: white;
    box-shadow: 0 14px 30px rgba(15, 23, 42, 0.14);
}

.gross-card {
    background: linear-gradient(135deg, #4338ca, #6366f1);
}

.x-card {
    background: linear-gradient(135deg, #0f766e, #14b8a6);
}

.inrate-card {
    background: linear-gradient(135deg, #c2410c, #f97316);
}

.coa-card {
    background: linear-gradient(135deg, #1e293b, #475569);
}

.card-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    opacity: 0.88;
    margin-bottom: 20px;
}

.card-value {
    font-size: 34px;
    font-weight: 800;
    letter-spacing: -1px;
}

.card-note {
    font-size: 12px;
    margin-top: 18px;
    opacity: 0.82;
}

.final-result {
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    color: white;
    padding: 34px;
    border-radius: 22px;
    text-align: center;
    margin-top: 24px;
    box-shadow: 0 16px 35px rgba(37, 99, 235, 0.22);
}

.final-label {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.8px;
    opacity: 0.85;
}

.final-value {
    font-size: 52px;
    font-weight: 850;
    margin-top: 10px;
}

.variable-box {
    background: #fff7ed;
    border-left: 4px solid #f97316;
    padding: 16px 20px;
    border-radius: 10px;
    color: #9a3412;
}

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 12px;
    margin-top: 35px;
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
# HTML RENDER FUNCTION
# ============================================================

def render_html(html):
    st.markdown(
        html,
        unsafe_allow_html=True
    )


# ============================================================
# CALCULATION FUNCTION
#
# STEP 1:
# Difference = Client Rate - Insurer Gross Rate
#
# STEP 2:
# X Amount = Difference / 1.18
#
# STEP 3:
# COA Amount = Base Rate × COA %
#
# STEP 4:
# In-Rate Amount = X Amount + COA Amount
#
# STEP 5:
# In-Rate % = In-Rate Amount / Client Rate × 100
# ============================================================

def calculate_inrate(
    client_rate,
    base_rate,
    gross_rate,
    coa_percent
):

    # Gross difference including GST
    gross_difference = client_rate - gross_rate

    # Remove 18% GST from X Amount
    x_amount = gross_difference / 1.18

    # COA Amount - backend calculation
    coa_amount = base_rate * (coa_percent / 100)

    # Total In-Rate Amount
    inrate_amount = x_amount + coa_amount

    # Final In-Rate Percentage
    if client_rate > 0:
        inrate_percent = (
            inrate_amount / client_rate
        ) * 100
    else:
        inrate_percent = 0.0

    return {
        "gross_difference": gross_difference,
        "x_amount": x_amount,
        "coa_amount": coa_amount,
        "inrate_amount": inrate_amount,
        "inrate_percent": inrate_percent
    }


# ============================================================
# APP HEADER
# ============================================================

render_html(
    '<div class="app-title">🛡️ Insurance In-Rate Calculator</div>'
    '<div class="app-subtitle">'
    'Analyse client pricing and calculate X Amount, COA and final In-Rate instantly.'
    '</div>'
)


# ============================================================
# STEP 01
# ============================================================

render_html(
    '<div class="section-kicker">STEP 01</div>'
    '<div class="section-title">Select Product & Insurer</div>'
    '<div class="section-description">'
    'Backend rates are automatically selected based on your product and insurer selection.'
    '</div>'
)


col1, col2 = st.columns(2)

with col1:
    product = st.selectbox(
        "Product",
        list(RATE_MASTER.keys())
    )

with col2:
    insurer = st.selectbox(
        "Insurer",
        list(RATE_MASTER[product].keys())
    )


# ============================================================
# BACKEND CONFIG
# ============================================================

config = RATE_MASTER[product][insurer]

base_rate = config.get("base_rate")
gross_rate = config.get("gross_rate")
coa_percent = config.get("coa_percent", 0.0)
variable_rate = config.get("variable_rate", False)


# ============================================================
# VARIABLE RATE PRODUCTS
# ============================================================

if variable_rate:

    render_html(
        '<div class="variable-box">'
        '<b>Variable Rate Product</b><br>'
        'This product is priced based on age and loan tenure. '
        'Fixed rates are not configured.'
        '</div>'
    )

    st.stop()


# ============================================================
# STEP 02
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

render_html(
    '<div class="section-kicker">STEP 02</div>'
    '<div class="section-title">Enter Client Rate</div>'
    '<div class="section-description">'
    'Enter the final rate you are planning to charge the client.'
    '</div>'
)


client_rate = st.number_input(
    "Client Rate (₹)",
    min_value=0.0,
    value=float(gross_rate),
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
# STEP 03
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

render_html(
    '<div class="section-kicker">STEP 03</div>'
    '<div class="section-title">Calculation Results</div>'
    '<div class="section-description">'
    'Your calculated in-rate result.'
    '</div>'
)


# ============================================================
# RESULT CARDS
# ============================================================

r1, r2, r3, r4 = st.columns(4)


# INSURER GROSS RATE
with r1:
    render_html(
        f'<div class="result-card gross-card">'
        f'<div class="card-label">INSURER GROSS RATE</div>'
        f'<div class="card-value">₹{gross_rate:,.2f}</div>'
        f'<div class="card-note">Insurer payment including GST</div>'
        f'</div>'
    )


# X AMOUNT
with r2:
    render_html(
        f'<div class="result-card x-card">'
        f'<div class="card-label">X AMOUNT</div>'
        f'<div class="card-value">₹{result["x_amount"]:,.2f}</div>'
        f'<div class="card-note">After removing 18% GST</div>'
        f'</div>'
    )


# IN-RATE AMOUNT
with r3:
    render_html(
        f'<div class="result-card inrate-card">'
        f'<div class="card-label">IN-RATE AMOUNT</div>'
        f'<div class="card-value">₹{result["inrate_amount"]:,.2f}</div>'
        f'<div class="card-note">X Amount + COA Amount</div>'
        f'</div>'
    )


# COA AMOUNT
with r4:
    render_html(
        f'<div class="result-card coa-card">'
        f'<div class="card-label">COA AMOUNT</div>'
        f'<div class="card-value">₹{result["coa_amount"]:,.2f}</div>'
        f'<div class="card-note">Backend calculated amount</div>'
        f'</div>'
    )


# ============================================================
# FINAL IN-RATE RESULT
# ============================================================

render_html(
    f'<div class="final-result">'
    f'<div class="final-label">FINAL IN-RATE PERCENTAGE</div>'
    f'<div class="final-value">{result["inrate_percent"]:.2f}%</div>'
    f'</div>'
)


# ============================================================
# CALCULATION DETAILS
# ============================================================

with st.expander("View Calculation Logic"):

    st.markdown(f"""
### Client Rate
₹{client_rate:,.2f}

### Insurer Gross Rate
₹{gross_rate:,.2f}

### Gross Difference
₹{result["gross_difference"]:,.2f}

### X Amount
(Gross Difference ÷ 1.18)

₹{result["gross_difference"]:,.2f} ÷ 1.18

= **₹{result["x_amount"]:,.2f}**

### COA Amount
Calculated internally based on backend configuration.

= **₹{result["coa_amount"]:,.2f}**

### In-Rate Amount

X Amount + COA Amount

₹{result["x_amount"]:,.2f} + ₹{result["coa_amount"]:,.2f}

= **₹{result["inrate_amount"]:,.2f}**

### Final In-Rate Percentage

(In-Rate Amount ÷ Client Rate) × 100

= **{result["inrate_percent"]:.2f}%**
""")


# ============================================================
# FOOTER
# ============================================================

render_html(
    '<div class="footer">'
    'Policygrace Internal Pricing Tool • Insurance In-Rate Calculator'
    '</div>'
)
