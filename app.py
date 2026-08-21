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
#
# Base Rate  = Insurer Base Rate excluding GST
# Gross Rate = Insurer payable amount including GST
#
# X Amount       = Client Rate - Gross Rate
# COA Amount     = Base Rate × COA %
# In-Rate Amount = X Amount + COA Amount
# In-Rate %      = In-Rate Amount ÷ Client Rate × 100
# ============================================================

RATE_MASTER = {

    "PA": {
        "Care @8.5%": {
            "base_rate": 9.00,
            "gross_rate": 11.00,
            "coa_percent": 8.5
        },
        "Cigna Manipal @25%": {
            "base_rate": 24.00,
            "gross_rate": 28.00,
            "coa_percent": 25.0
        },
        "Aditya Birla @25% (incl GST)": {
            "base_rate": 21.00,
            "gross_rate": 25.00,
            "coa_percent": 25.0
        }
    },

    "Hospicash": {
        "ZUNO (Nil COA)": {
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
        "Magma (18-60) @10%": {
            "base_rate": 424.00,
            "gross_rate": 500.00,
            "coa_percent": 10.0
        },
        "Tata @25%": {
            "base_rate": 169.00,
            "gross_rate": 200.00,
            "coa_percent": 25.0
        }
    },

    "PA + Cancer Specific": {
        "Cigna Manipal @25%": {
            "base_rate": 180.00,
            "gross_rate": 212.00,
            "coa_percent": 25.0
        }
    },

    "Cancer Specific": {
        "Cigna Manipal @25%": {
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
        "Aviva @10%": {
            "base_rate": 320.30,
            "gross_rate": 378.00,
            "coa_percent": 10.0
        }
    },

    "PA + CI": {
        "Magma @10%": {
            "base_rate": 270.00,
            "gross_rate": 319.00,
            "coa_percent": 10.0
        },
        "Cigna Manipal @25%": {
            "base_rate": 368.00,
            "gross_rate": 434.00,
            "coa_percent": 25.0
        }
    },

    "GCL": {
        "Digit @32.5%": {
            "base_rate": None,
            "gross_rate": None,
            "coa_percent": 32.5,
            "variable_rate": True
        },
        "Aviva (HL & LAP) @10%": {
            "base_rate": None,
            "gross_rate": None,
            "coa_percent": 10.0,
            "variable_rate": True
        }
    },

    "CI": {
        "Cigna Manipal @25%": {
            "base_rate": 344.00,
            "gross_rate": 406.00,
            "coa_percent": 25.0
        }
    },

    "Health": {
        "Aditya Birla @25%": {
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
    background:
        radial-gradient(
            circle at 0% 0%,
            rgba(59, 130, 246, 0.10),
            transparent 32%
        ),
        radial-gradient(
            circle at 100% 100%,
            rgba(16, 185, 129, 0.08),
            transparent 32%
        ),
        #f8fafc;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

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
    margin-bottom: 30px;
}

.section-kicker {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1.5px;
    color: #2563eb;
    margin-bottom: 5px;
}

.section-title {
    font-size: 24px;
    font-weight: 800;
    color: #0f172a;
    margin-bottom: 6px;
}

.section-description {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 18px;
}

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

.result-card {
    border-radius: 18px;
    padding: 22px;
    min-height: 155px;
    color: white;
    box-shadow: 0 14px 30px rgba(15, 23, 42, 0.12);
}

.gross-card {
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
        #1e293b,
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

.final-result {
    background: linear-gradient(
        135deg,
        #1d4ed8,
        #2563eb
    );

    color: white;
    padding: 30px;
    border-radius: 22px;
    text-align: center;
    margin-top: 24px;

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
    font-size: 50px;
    font-weight: 850;
    margin-top: 8px;
}

.alert-box {
    background: #fff7ed;
    border-left: 4px solid #f97316;
    color: #9a3412;
    padding: 16px;
    border-radius: 10px;
    margin-top: 20px;
}

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 12px;
    margin-top: 30px;
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
# FIXES HTML SHOWING AS TEXT
# ============================================================

def render_html(html):
    st.markdown(
        html.strip(),
        unsafe_allow_html=True
    )


# ============================================================
# CALCULATION FUNCTION
# ============================================================

def calculate_inrate(
    client_rate,
    base_rate,
    gross_rate,
    coa_percent
):

    # X Amount = Client Rate - Insurer Gross Rate
    x_amount = client_rate - gross_rate

    # COA Amount = Insurer Base Rate × COA %
    coa_amount = (
        base_rate
        * (coa_percent / 100)
    )

    # In-Rate Amount = X Amount + COA Amount
    inrate_amount = (
        x_amount
        + coa_amount
    )

    # Final In-Rate %
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

render_html("""
<div class="app-title">
    🛡️ Insurance In-Rate Calculator
</div>

<div class="app-subtitle">
    Analyse client pricing and calculate X Amount, COA and final In-Rate instantly.
</div>
""")


# ============================================================
# STEP 01
# ============================================================

render_html("""
<div class="section-kicker">
    STEP 01
</div>

<div class="section-title">
    Select Product & Insurer
</div>

<div class="section-description">
    Backend rates are automatically selected based on the chosen product and insurer.
</div>
""")


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
# BACKEND CONFIGURATION
# ============================================================

config = RATE_MASTER[product][insurer]

base_rate = config.get("base_rate")
gross_rate = config.get("gross_rate")
coa_percent = config.get("coa_percent", 0.0)

variable_rate = config.get(
    "variable_rate",
    False
)


# ============================================================
# VARIABLE RATE PRODUCTS
# ============================================================

if variable_rate:

    render_html("""
    <div class="alert-box">
        <b>Variable Rate Product</b><br>
        This product is priced based on age and loan tenure.
        Fixed Base Rate and Gross Rate are not configured.
    </div>
    """)

    st.stop()


# ============================================================
# STEP 02
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

render_html("""
<div class="section-kicker">
    STEP 02
</div>

<div class="section-title">
    Enter Client Rate
</div>

<div class="section-description">
    Enter the final rate you plan to charge the client.
</div>
""")


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
# STEP 03 - RESULTS
# ============================================================

st.markdown("<br>", unsafe_allow_html=True)

render_html("""
<div class="section-kicker">
    STEP 03
</div>

<div class="section-title">
    Calculation Results
</div>

<div class="section-description">
    Your calculated in-rate result.
</div>
""")


r1, r2, r3, r4 = st.columns(4)


# ============================================================
# INSURER GROSS RATE
# ============================================================

with r1:

    render_html(f"""
<div class="result-card gross-card">

    <div class="card-label">
        INSURER GROSS RATE
    </div>

    <div class="card-value">
        ₹{gross_rate:,.2f}
    </div>

    <div class="card-note">
        Insurer payment including GST
    </div>

</div>
""")


# ============================================================
# X AMOUNT
# ============================================================

with r2:

    render_html(f"""
<div class="result-card x-card">

    <div class="card-label">
        X AMOUNT
    </div>

    <div class="card-value">
        ₹{result["x_amount"]:,.2f}
    </div>

    <div class="card-note">
        Client Rate − Gross Rate
    </div>

</div>
""")


# ============================================================
# IN-RATE AMOUNT
# ============================================================

with r3:

    render_html(f"""
<div class="result-card inrate-card">

    <div class="card-label">
        IN-RATE AMOUNT
    </div>

    <div class="card-value">
        ₹{result["inrate_amount"]:,.2f}
    </div>

    <div class="card-note">
        X Amount + COA Amount
    </div>

</div>
""")


# ============================================================
# COA AMOUNT
# ============================================================

with r4:

    render_html(f"""
<div class="result-card coa-card">

    <div class="card-label">
        COA AMOUNT
    </div>

    <div class="card-value">
        ₹{result["coa_amount"]:,.2f}
    </div>

    <div class="card-note">
        {coa_percent:.2f}% of Base Rate
    </div>

</div>
""")


# ============================================================
# FINAL IN-RATE %
# ============================================================

render_html(f"""
<div class="final-result">

    <div class="final-label">
        FINAL IN-RATE PERCENTAGE
    </div>

    <div class="final-value">
        {result["inrate_percent"]:.2f}%
    </div>

</div>
""")


# ============================================================
# VIEW CALCULATION
# ============================================================

with st.expander("View Calculation Logic"):

    st.markdown(f"""
### 1. Client Rate

**₹{client_rate:,.2f}**

---

### 2. Insurer Base Rate

**₹{base_rate:,.2f}**

---

### 3. Insurer Gross Rate

**₹{gross_rate:,.2f}**

---

### 4. X Amount

**Client Rate − Gross Rate**

₹{client_rate:,.2f} − ₹{gross_rate:,.2f}

= **₹{result["x_amount"]:,.2f}**

---

### 5. COA Amount

**Base Rate × COA %**

₹{base_rate:,.2f} × {coa_percent:.2f}%

= **₹{result["coa_amount"]:,.2f}**

---

### 6. In-Rate Amount

**X Amount + COA Amount**

₹{result["x_amount"]:,.2f} + ₹{result["coa_amount"]:,.2f}

= **₹{result["inrate_amount"]:,.2f}**

---

### 7. Final In-Rate %

**In-Rate Amount ÷ Client Rate × 100**

₹{result["inrate_amount"]:,.2f} ÷ ₹{client_rate:,.2f} × 100

= **{result["inrate_percent"]:.2f}%**
""")


# ============================================================
# FOOTER
# ============================================================

render_html("""
<div class="footer">
    Policygrace Internal Pricing Tool • Insurance In-Rate Calculator
</div>
""")
