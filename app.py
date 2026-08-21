import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import datetime
import io

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
# CUSTOM CSS
# ============================================================

st.markdown(
    """
<style>

.stApp {
    background:
        radial-gradient(circle at 0% 0%, rgba(37, 99, 235, 0.08), transparent 30%),
        radial-gradient(circle at 100% 100%, rgba(20, 184, 166, 0.07), transparent 30%),
        #f8fafc;
}

.block-container {
    max-width: 1200px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* HEADER */

.app-title {
    font-size: 36px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -1px;
    margin-bottom: 4px;
}

.app-subtitle {
    font-size: 16px;
    color: #64748b;
    margin-bottom: 32px;
}

/* SECTION HEADINGS */

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
    margin-bottom: 5px;
}

.section-description {
    font-size: 14px;
    color: #64748b;
    margin-bottom: 18px;
}

/* INPUT AREA */

.input-container {
    background: white;
    border: 1px solid #e2e8f0;
    border-radius: 18px;
    padding: 20px;
    margin-bottom: 24px;
}

/* INPUTS */

div[data-testid="stSelectbox"] > div > div {
    border-radius: 10px;
}

div[data-testid="stNumberInput"] input {
    border-radius: 10px;
}

/* BUTTON */

div.stButton > button {
    width: 100%;
    border-radius: 10px;
    font-weight: 700;
    padding: 0.65rem;
}

/* RESULT CARDS */

.result-card {
    border-radius: 18px;
    padding: 22px;
    min-height: 155px;
    color: white;
    box-shadow: 0 12px 28px rgba(15, 23, 42, 0.12);
    margin-bottom: 12px;
}

.card-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    opacity: 0.85;
    margin-bottom: 16px;
}

.card-value {
    font-size: 30px;
    font-weight: 850;
    letter-spacing: -0.8px;
}

.card-note {
    font-size: 12px;
    margin-top: 14px;
    opacity: 0.82;
    line-height: 1.4;
}

.input-card {
    background: linear-gradient(135deg, #4338ca, #6366f1);
}

.base-card {
    background: linear-gradient(135deg, #0f766e, #14b8a6);
}

.x-card {
    background: linear-gradient(135deg, #b45309, #f59e0b);
}

.netx-card {
    background: linear-gradient(135deg, #7c2d12, #ea580c);
}

.coa-card {
    background: linear-gradient(135deg, #334155, #475569);
}

.inrate-card {
    background: linear-gradient(135deg, #047857, #10b981);
}

/* FINAL RESULT */

.final-result {
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    color: white;
    padding: 30px;
    border-radius: 22px;
    text-align: center;
    margin-top: 18px;
    box-shadow: 0 15px 35px rgba(37, 99, 235, 0.22);
}

.final-label {
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.5px;
    opacity: 0.85;
}

.final-value {
    font-size: 52px;
    font-weight: 850;
    margin-top: 8px;
}

/* INFO BOX */

.info-box {
    background: #eff6ff;
    border-left: 4px solid #2563eb;
    padding: 14px 18px;
    border-radius: 10px;
    color: #1e3a8a;
    margin-top: 18px;
}

/* FOOTER */

.footer {
    text-align: center;
    color: #94a3b8;
    font-size: 12px;
    margin-top: 30px;
}

/* STREAMLIT */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""",
    unsafe_allow_html=True
)


# ============================================================
# RATE MASTER LOADING
# ============================================================

@st.cache_data
def load_rate_master():

    file_path = Path("rate_master.csv")

    if not file_path.exists():
        return None, "rate_master.csv file not found."

    try:

        rates = pd.read_csv(file_path)

    except Exception as e:

        return None, f"Unable to read rate master: {str(e)}"

    if rates.empty:
        return None, "Rate master is empty."

    # Clean column names
    rates.columns = rates.columns.str.strip()

    required_columns = [
        "Product",
        "Insurer",
        "Base Rate",
        "COA %"
    ]

    missing_columns = [
        col for col in required_columns
        if col not in rates.columns
    ]

    if missing_columns:

        return (
            None,
            f"Missing required columns: {', '.join(missing_columns)}"
        )

    # Clean text columns
    rates["Product"] = (
        rates["Product"]
        .astype(str)
        .str.strip()
    )

    rates["Insurer"] = (
        rates["Insurer"]
        .astype(str)
        .str.strip()
    )

    # Remove empty text values
    rates = rates[
        (rates["Product"] != "")
        &
        (rates["Insurer"] != "")
        &
        (rates["Product"].str.lower() != "nan")
        &
        (rates["Insurer"].str.lower() != "nan")
    ].copy()

    # Convert numeric columns
    rates["Base Rate"] = pd.to_numeric(
        rates["Base Rate"],
        errors="coerce"
    )

    # Clean COA percentage
    rates["COA %"] = (
        rates["COA %"]
        .astype(str)
        .str.replace("%", "", regex=False)
        .str.strip()
    )

    rates["COA %"] = pd.to_numeric(
        rates["COA %"],
        errors="coerce"
    )

    # Check duplicates
    duplicates = rates.duplicated(
        subset=["Product", "Insurer"],
        keep=False
    )

    if duplicates.any():

        duplicate_rows = rates.loc[
            duplicates,
            ["Product", "Insurer"]
        ]

        duplicate_text = ", ".join(
            [
                f"{row['Product']} - {row['Insurer']}"
                for _, row in duplicate_rows.iterrows()
            ]
        )

        return (
            None,
            f"Duplicate Product/Insurer combinations found: {duplicate_text}"
        )

    return rates, None


# ============================================================
# CALCULATION FUNCTION
# ============================================================

def calculate_inrate(
    input_price,
    base_rate,
    coa_percent
):

    # --------------------------------------------------------
    # STEP 1
    # X Amount = Input Price - Base Rate
    # --------------------------------------------------------

    x_amount = input_price - base_rate

    # --------------------------------------------------------
    # STEP 2
    # Net X Amount = X Amount / 1.18
    # Removes 18% GST from X
    # --------------------------------------------------------

    net_x_amount = x_amount / 1.18

    # --------------------------------------------------------
    # STEP 3
    # COA Amount = Base Rate * COA %
    # --------------------------------------------------------

    coa_amount = base_rate * (coa_percent / 100)

    # --------------------------------------------------------
    # STEP 4
    # In-Rate Amount = Net X Amount + COA Amount
    # --------------------------------------------------------

    inrate_amount = net_x_amount + coa_amount

    # --------------------------------------------------------
    # STEP 5
    # Final In-Rate % =
    # (In-Rate Amount / Input Price) * 100
    # --------------------------------------------------------

    if input_price > 0:

        inrate_percent = (
            inrate_amount / input_price
        ) * 100

    else:

        inrate_percent = 0

    return {
        "x_amount": x_amount,
        "net_x_amount": net_x_amount,
        "coa_amount": coa_amount,
        "inrate_amount": inrate_amount,
        "inrate_percent": inrate_percent
    }


# ============================================================
# DOWNLOAD FUNCTION
# ============================================================

def create_download_file(
    product,
    insurer,
    input_price,
    base_rate,
    coa_percent,
    result
):

    report = pd.DataFrame(
        [
            {
                "Date & Time": datetime.now().strftime(
                    "%d-%m-%Y %H:%M:%S"
                ),
                "Product": product,
                "Insurer": insurer,
                "Input Price": input_price,
                "Base Rate": base_rate,
                "COA %": coa_percent,
                "X Amount": result["x_amount"],
                "Net X Amount (Excl. GST)": result["net_x_amount"],
                "COA Amount": result["coa_amount"],
                "In-Rate Amount": result["inrate_amount"],
                "Final In-Rate %": result["inrate_percent"]
            }
        ]
    )

    return report.to_csv(
        index=False
    ).encode("utf-8")


# ============================================================
# SESSION STATE
# ============================================================

if "calculated" not in st.session_state:
    st.session_state.calculated = False

if "result" not in st.session_state:
    st.session_state.result = None

if "history" not in st.session_state:
    st.session_state.history = []


# ============================================================
# LOAD RATE MASTER
# ============================================================

rates, error_message = load_rate_master()


# ============================================================
# HEADER
# ============================================================

st.markdown(
    """
<div class="app-title">
    🛡️ Insurance In-Rate Calculator
</div>

<div class="app-subtitle">
    Calculate In-Rate Amount & In-Rate % using backend-configured insurer rates and COA.
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# STOP IF RATE MASTER HAS ERROR
# ============================================================

if error_message:

    st.error(error_message)

    st.info(
        "Please ensure rate_master.csv exists and contains: "
        "Product, Insurer, Base Rate, COA %"
    )

    st.stop()


# ============================================================
# SIDEBAR - RATE MASTER
# ============================================================

with st.sidebar:

    st.markdown("## 📋 Rate Master")

    st.caption(
        "Current backend-configured rates"
    )

    st.dataframe(
        rates,
        use_container_width=True,
        hide_index=True
    )


# ============================================================
# STEP 01 - CALCULATION INPUT
# ============================================================

st.markdown(
    """
<div class="section-kicker">STEP 01</div>
<div class="section-title">Calculation Input</div>
<div class="section-description">
Select the Product and Insurer, then enter the client-side Input Price.
</div>
""",
    unsafe_allow_html=True
)


input_col1, input_col2, input_col3 = st.columns(3)


# PRODUCT

with input_col1:

    products = sorted(
        rates["Product"]
        .dropna()
        .unique()
    )

    product = st.selectbox(
        "Product",
        options=products
    )


# FILTER INSURERS

filtered_rates = rates[
    rates["Product"] == product
].copy()


# INSURER

with input_col2:

    insurers = sorted(
        filtered_rates["Insurer"]
        .dropna()
        .unique()
    )

    insurer = st.selectbox(
        "Insurer",
        options=insurers
    )


# SELECT RATE

selected_row = filtered_rates[
    filtered_rates["Insurer"] == insurer
].iloc[0]

base_rate = selected_row["Base Rate"]
coa_percent = selected_row["COA %"]


# INPUT PRICE

with input_col3:

    input_price = st.number_input(
        "Input Price (₹)",
        min_value=0.01,
        value=float(base_rate)
        if pd.notna(base_rate)
        else 1.00,
        step=0.01,
        format="%.2f"
    )


# ============================================================
# VALIDATION
# ============================================================

validation_error = None

if pd.isna(base_rate):

    validation_error = (
        "Base Rate not configured for this "
        "Product/Insurer combination."
    )

elif pd.isna(coa_percent):

    validation_error = (
        "COA % not configured for this "
        "Product/Insurer combination."
    )

elif base_rate <= 0:

    validation_error = (
        "Invalid Base Rate configured for this "
        "Product/Insurer combination."
    )

elif coa_percent < 0:

    validation_error = (
        "Invalid COA % configured for this "
        "Product/Insurer combination."
    )


if validation_error:

    st.error(validation_error)


elif input_price < base_rate:

    st.warning(
        "Input Price is lower than the Base Rate. "
        "Please verify the entered amount."
    )


# ============================================================
# CALCULATE BUTTON
# ============================================================

button_col1, button_col2 = st.columns([3, 1])


with button_col1:

    calculate_clicked = st.button(
        "Calculate In-Rate",
        type="primary",
        use_container_width=True
    )


with button_col2:

    reset_clicked = st.button(
        "Reset Calculator",
        use_container_width=True
    )


# ============================================================
# RESET
# ============================================================

if reset_clicked:

    st.session_state.calculated = False
    st.session_state.result = None

    st.rerun()


# ============================================================
# PERFORM CALCULATION
# ============================================================

if calculate_clicked:

    if validation_error:

        st.error(
            "Calculation cannot be performed until "
            "the rate configuration is corrected."
        )

        st.session_state.calculated = False

    elif input_price <= 0:

        st.error(
            "Input Price must be greater than ₹0."
        )

        st.session_state.calculated = False

    else:

        result = calculate_inrate(
            input_price=float(input_price),
            base_rate=float(base_rate),
            coa_percent=float(coa_percent)
        )

        st.session_state.result = result
        st.session_state.calculated = True

        # Save history

        history_entry = {
            "Date & Time": datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            ),
            "Product": product,
            "Insurer": insurer,
            "Input Price": float(input_price),
            "Base Rate": float(base_rate),
            "COA %": float(coa_percent),
            "COA Amount": result["coa_amount"],
            "X Amount": result["x_amount"],
            "Net X Amount": result["net_x_amount"],
            "In-Rate Amount": result["inrate_amount"],
            "In-Rate %": result["inrate_percent"]
        }

        st.session_state.history.append(
            history_entry
        )


# ============================================================
# RESULTS
# ============================================================

if st.session_state.calculated:

    result = st.session_state.result

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
<div class="section-kicker">STEP 02</div>
<div class="section-title">Calculation Results</div>
<div class="section-description">
Your calculated in-rate breakdown.
</div>
""",
        unsafe_allow_html=True
    )


    # --------------------------------------------------------
    # ROW 1
    # --------------------------------------------------------

    r1, r2, r3 = st.columns(3)


    # INPUT PRICE

    with r1:

        html = (
            f'<div class="result-card input-card">'
            f'<div class="card-label">INPUT PRICE</div>'
            f'<div class="card-value">₹{input_price:,.2f}</div>'
            f'<div class="card-note">Client-side selling price</div>'
            f'</div>'
        )

        st.markdown(
            html,
            unsafe_allow_html=True
        )


    # BASE RATE

    with r2:

        html = (
            f'<div class="result-card base-card">'
            f'<div class="card-label">BASE RATE</div>'
            f'<div class="card-value">₹{base_rate:,.2f}</div>'
            f'<div class="card-note">Backend configured insurer rate</div>'
            f'</div>'
        )

        st.markdown(
            html,
            unsafe_allow_html=True
        )


    # COA AMOUNT

    with r3:

        html = (
            f'<div class="result-card coa-card">'
            f'<div class="card-label">COA AMOUNT</div>'
            f'<div class="card-value">₹{result["coa_amount"]:,.4f}</div>'
            f'<div class="card-note">'
            f'COA: {coa_percent:.2f}% of Base Rate'
            f'</div>'
            f'</div>'
        )

        st.markdown(
            html,
            unsafe_allow_html=True
        )


    # --------------------------------------------------------
    # ROW 2
    # --------------------------------------------------------

    r4, r5, r6 = st.columns(3)


    # X AMOUNT

    with r4:

        html = (
            f'<div class="result-card x-card">'
            f'<div class="card-label">X AMOUNT</div>'
            f'<div class="card-value">₹{result["x_amount"]:,.2f}</div>'
            f'<div class="card-note">Input Price − Base Rate</div>'
            f'</div>'
        )

        st.markdown(
            html,
            unsafe_allow_html=True
        )


    # NET X AMOUNT

    with r5:

        html = (
            f'<div class="result-card netx-card">'
            f'<div class="card-label">NET X AMOUNT</div>'
            f'<div class="card-value">'
            f'₹{result["net_x_amount"]:,.4f}'
            f'</div>'
            f'<div class="card-note">X Amount excluding 18% GST</div>'
            f'</div>'
        )

        st.markdown(
            html,
            unsafe_allow_html=True
        )


    # IN-RATE AMOUNT

    with r6:

        html = (
            f'<div class="result-card inrate-card">'
            f'<div class="card-label">IN-RATE AMOUNT</div>'
            f'<div class="card-value">'
            f'₹{result["inrate_amount"]:,.4f}'
            f'</div>'
            f'<div class="card-note">Net X Amount + COA Amount</div>'
            f'</div>'
        )

        st.markdown(
            html,
            unsafe_allow_html=True
        )


    # ========================================================
    # FINAL RESULT
    # ========================================================

    final_html = (
        f'<div class="final-result">'
        f'<div class="final-label">FINAL IN-RATE PERCENTAGE</div>'
        f'<div class="final-value">'
        f'{result["inrate_percent"]:.2f}%'
        f'</div>'
        f'</div>'
    )

    st.markdown(
        final_html,
        unsafe_allow_html=True
    )


    # ========================================================
    # VIEW CALCULATION
    # ========================================================

    with st.expander("View Calculation"):

        st.markdown(
            f"""
### Step 1 — X Amount

**X Amount = Input Price − Base Rate**

₹{input_price:,.2f} − ₹{base_rate:,.2f}
= **₹{result["x_amount"]:,.2f}**

---

### Step 2 — Net X Amount

**Net X Amount = X Amount ÷ 1.18**

₹{result["x_amount"]:,.4f} ÷ 1.18
= **₹{result["net_x_amount"]:,.4f}**

---

### Step 3 — COA Amount

**COA Amount = Base Rate × COA %**

₹{base_rate:,.4f} × {coa_percent:.2f}%
= **₹{result["coa_amount"]:,.4f}**

---

### Step 4 — In-Rate Amount

**In-Rate Amount = Net X Amount + COA Amount**

₹{result["net_x_amount"]:,.4f}
+ ₹{result["coa_amount"]:,.4f}

= **₹{result["inrate_amount"]:,.4f}**

---

### Step 5 — Final In-Rate %

**In-Rate % = (In-Rate Amount ÷ Input Price) × 100**

(₹{result["inrate_amount"]:,.4f}
÷ ₹{input_price:,.2f}) × 100

= **{result["inrate_percent"]:.2f}%**
"""
        )


    # ========================================================
    # DOWNLOAD CALCULATION
    # ========================================================

    download_data = create_download_file(
        product=product,
        insurer=insurer,
        input_price=float(input_price),
        base_rate=float(base_rate),
        coa_percent=float(coa_percent),
        result=result
    )

    st.markdown("<br>", unsafe_allow_html=True)

    st.download_button(
        label="Download Calculation",
        data=download_data,
        file_name="insurance_inrate_calculation.csv",
        mime="text/csv",
        use_container_width=True
    )


# ============================================================
# CALCULATION HISTORY
# ============================================================

if st.session_state.history:

    st.markdown("<br>", unsafe_allow_html=True)

    st.markdown(
        """
<div class="section-kicker">SESSION DATA</div>
<div class="section-title">Calculation History</div>
<div class="section-description">
Successful calculations from the current session.
</div>
""",
        unsafe_allow_html=True
    )

    history_df = pd.DataFrame(
        st.session_state.history
    )

    st.dataframe(
        history_df,
        use_container_width=True,
        hide_index=True
    )

    if st.button("Clear History"):

        st.session_state.history = []

        st.rerun()


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
