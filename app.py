import streamlit as st


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Policygrace | Insurance In-Rate Calculator",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)


# ============================================================
# BACKEND RATE MASTER
# COA % IS INTERNAL AND NOT SHOWN IN DROPDOWN
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
            "variable_rate": True
        },
        "Aviva (HL & LAP)": {
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

    # --------------------------------------------------------
    # CASE 1: CLIENT RATE ENTERED
    #
    # X AMOUNT =
    # (CLIENT RATE - INSURER GROSS RATE) / 1.18
    #
    # This gives the NET amount after GST removal.
    # --------------------------------------------------------

    if client_rate > 0:

        gross_difference = client_rate - gross_rate

        x_amount = gross_difference / 1.18

        denominator = client_rate

        x_note = "Net additional amount"


    # --------------------------------------------------------
    # CASE 2: CLIENT RATE NOT ENTERED
    #
    # X AMOUNT =
    # INSURER GROSS RATE / 1.18
    #
    # Only the final net amount is shown.
    # --------------------------------------------------------

    else:

        x_amount = gross_rate / 1.18

        denominator = gross_rate

        x_note = "Net insurer amount"


    # --------------------------------------------------------
    # INTERNAL COA CALCULATION
    # --------------------------------------------------------

    coa_amount = base_rate * (coa_percent / 100)


    # --------------------------------------------------------
    # TOTAL IN-RATE AMOUNT
    # --------------------------------------------------------

    inrate_amount = x_amount + coa_amount


    # --------------------------------------------------------
    # FINAL IN-RATE PERCENTAGE
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
# APPLICATION HEADER
# ============================================================

st.title("🛡️ Insurance In-Rate Calculator")

st.caption("POLICYGRACE • INTERNAL PRICING TOOL")

st.write(
    "Analyse insurer pricing, client rates and internal "
    "in-rate calculations in one place."
)

st.divider()


# ============================================================
# CONFIGURATION SECTION
# ============================================================

st.caption("STEP 01")

st.subheader("Select Product & Insurer")

st.write(
    "Choose the product and insurer to load the configured "
    "backend pricing."
)


with st.container(border=True):

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
# LOAD BACKEND CONFIGURATION
# ============================================================

config = RATE_MASTER[product][insurer]

variable_rate = config.get(
    "variable_rate",
    False
)


# ============================================================
# VARIABLE RATE PRODUCTS
# ============================================================

if variable_rate:

    st.divider()

    st.warning(
        "This product has a variable rate based on age "
        "and loan tenure."
    )

    st.info(
        "A fixed backend rate is currently not configured "
        "for this product."
    )

    st.stop()


base_rate = config["base_rate"]

gross_rate = config["gross_rate"]

coa_percent = config["coa_percent"]


# ============================================================
# CLIENT RATE INPUT
# ============================================================

st.divider()

st.caption("STEP 02")

st.subheader("Enter Client Rate")

st.write(
    "Enter the final rate to be charged to the client. "
    "Leave it at ₹0 to view the net insurer amount."
)


with st.container(border=True):

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
# CALCULATION RESULTS
# ============================================================

st.divider()

st.caption("STEP 03")

st.subheader("Calculation Results")

st.write(
    "Your calculated in-rate result based on the selected "
    "insurer and client rate."
)


# ============================================================
# RESULT CARDS - ROW 1
# ============================================================

c1, c2, c3, c4 = st.columns(4)


with c1:

    with st.container(border=True):

        st.caption("INSURER GROSS RATE")

        st.metric(
            label="",
            value=f"₹{gross_rate:,.2f}"
        )

        st.caption(
            "Insurer payment including GST"
        )


with c2:

    with st.container(border=True):

        st.caption("X AMOUNT")

        st.metric(
            label="",
            value=f"₹{result['x_amount']:,.2f}"
        )

        st.caption(
            result["x_note"]
        )


with c3:

    with st.container(border=True):

        st.caption("IN-RATE AMOUNT")

        st.metric(
            label="",
            value=f"₹{result['inrate_amount']:,.2f}"
        )

        st.caption(
            "X Amount + Internal COA"
        )


with c4:

    with st.container(border=True):

        st.caption("COA AMOUNT")

        st.metric(
            label="",
            value=f"₹{result['coa_amount']:,.2f}"
        )

        st.caption(
            "Internal backend calculation"
        )


# ============================================================
# FINAL RESULT
# ============================================================

st.divider()

with st.container(border=True):

    left_space, result_column, right_space = st.columns(
        [1, 2, 1]
    )

    with result_column:

        st.caption(
            "FINAL IN-RATE PERCENTAGE"
        )

        st.metric(
            label="",
            value=f"{result['inrate_percentage']:.2f}%"
        )

        st.caption(
            "Calculated from the selected pricing structure"
        )


# ============================================================
# STATUS MESSAGE
# ============================================================

st.divider()

if client_rate > 0:

    st.success(
        "Calculation completed using the client rate entered."
    )

else:

    st.info(
        "No client rate entered. X Amount shows the final "
        "net insurer amount."
    )


# ============================================================
# FOOTER
# ============================================================

st.caption(
    "POLICYGRACE INSURANCE BROKING • INTERNAL USE ONLY"
)
