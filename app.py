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
# CALCULATION FUNCTION
# ============================================================

def calculate_inrate(
    client_rate,
    base_rate,
    gross_rate,
    coa_percent
):

    # CLIENT RATE ENTERED
    if client_rate > 0:

        # Difference from insurer gross rate
        difference = client_rate - gross_rate

        # Remove GST from difference
        x_amount = difference / 1.18

        x_note = "Net additional amount"

        denominator = client_rate

    # CLIENT RATE NOT ENTERED
    else:

        # Show insurer amount excluding GST
        x_amount = gross_rate / 1.18

        x_note = "Net insurer amount"

        denominator = gross_rate

    # COA AMOUNT
    coa_amount = base_rate * (coa_percent / 100)

    # TOTAL IN-RATE AMOUNT
    inrate_amount = x_amount + coa_amount

    # FINAL IN-RATE %
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
# SIMPLE CSS ONLY
# NO HTML DIV ELEMENTS
# ============================================================

st.markdown("""
<style>

.stApp {
    background-color: #f5f7fb;
}

.block-container {
    max-width: 1350px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

h1, h2, h3 {
    color: #172033;
}

[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 20px;
    box-shadow: 0 6px 20px rgba(0, 0, 0, 0.06);
}

[data-testid="stMetricLabel"] {
    font-weight: 700;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# HEADER
# ============================================================

st.title("🛡️ Insurance In-Rate Calculator")

st.caption(
    "POLICYGRACE • INTERNAL PRICING TOOL"
)

st.write(
    "Analyse insurer pricing, client rates and internal "
    "in-rate calculations in one place."
)

st.divider()


# ============================================================
# CONFIGURATION
# ============================================================

st.subheader("Select Product & Insurer")

st.caption(
    "Choose the product and insurer to load backend pricing."
)

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
# GET BACKEND CONFIGURATION
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
# VARIABLE RATE PRODUCTS
# ============================================================

if variable_rate:

    st.warning(
        "This product has a variable rate based on age "
        "and loan tenure."
    )

    st.info(
        "Please configure the required rate before calculation."
    )

    st.stop()


# ============================================================
# CLIENT PRICING
# ============================================================

st.divider()

st.subheader("Enter Client Rate")

st.caption(
    "Enter the final rate to be charged to the client. "
    "Leave ₹0 to calculate the net insurer amount."
)

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

st.divider()

st.subheader("Calculation Results")

st.caption(
    "Live calculation based on the selected insurer "
    "and client rate."
)


# ============================================================
# KPI CARDS
# ============================================================

c1, c2, c3, c4 = st.columns(4)


with c1:

    st.metric(
        label="INSURER GROSS RATE",
        value=f"₹{gross_rate:,.2f}"
    )

    st.caption(
        "Insurer payment including GST"
    )


with c2:

    st.metric(
        label="X AMOUNT",
        value=f"₹{result['x_amount']:,.2f}"
    )

    st.caption(
        result["x_note"]
    )


with c3:

    st.metric(
        label="IN-RATE AMOUNT",
        value=f"₹{result['inrate_amount']:,.2f}"
    )

    st.caption(
        "X Amount + Internal COA"
    )


with c4:

    st.metric(
        label="COA AMOUNT",
        value=f"₹{result['coa_amount']:,.2f}"
    )

    st.caption(
        "Internal calculation"
    )


# ============================================================
# FINAL RESULT
# ============================================================

st.divider()

final_col1, final_col2, final_col3 = st.columns([1, 2, 1])

with final_col2:

    st.metric(
        label="FINAL IN-RATE PERCENTAGE",
        value=f"{result['inrate_percentage']:.2f}%"
    )


# ============================================================
# CALCULATION STATUS
# ============================================================

if client_rate > 0:

    st.success(
        "Client rate entered. X Amount is calculated after "
        "subtracting the insurer gross rate and removing GST."
    )

else:

    st.info(
        "No client rate entered. X Amount shows the insurer "
        "gross rate converted to the net amount excluding GST."
    )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "POLICYGRACE INSURANCE BROKING • INTERNAL USE ONLY"
)
