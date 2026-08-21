import streamlit as st
import pandas as pd
import re
from pathlib import Path

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

st.markdown("""
<style>

.stApp {
    background:
        radial-gradient(circle at 5% 0%, rgba(37, 99, 235, 0.10), transparent 30%),
        radial-gradient(circle at 95% 100%, rgba(16, 185, 129, 0.08), transparent 30%),
        #f8fafc;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

/* APP HEADER */

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

/* SECTION HEADINGS */

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

/* INPUTS */

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

/* RESULT CARDS */

.result-card {
    border-radius: 18px;
    padding: 24px;
    min-height: 165px;
    color: white;
    box-shadow: 0 14px 30px rgba(15, 23, 42, 0.14);
}

.base-card {
    background: linear-gradient(135deg, #4338ca, #6366f1);
}

.x-card {
    background: linear-gradient(135deg, #0f766e, #14b8a6);
}

.inrate-card {
    background: linear-gradient(135deg, #c2410c, #f97316);
}

.coa-card {
    background: linear-gradient(135deg, #111827, #334155);
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

/* FINAL RESULT */

.final-result {
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    color: white;
    padding: 28px;
    border-radius: 20px;
    text-align: center;
    margin-top: 25px;
    box-shadow: 0 15px 35px rgba(37, 99, 235, 0.22);
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

/* HIDE STREAMLIT */

#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# ============================================================
# FALLBACK DATA
# ============================================================

FALLBACK_DATA = [
    ["PA", "Care", 9.00, 12.00, 8.5],
    ["PA", "Cigna Manipal", 24.00, 24.00, 25.0],
    ["PA", "Aditya Birla", 21.00, 25.00, 25.0],

    ["Hospicash", "ZUNO", 150.00, 165.00, 0.0],

    ["PA HOSPICASH", "Magma", 424.00, 471.00, 10.0],
    ["PA HOSPICASH", "Tata", 169.00, 169.00, 25.0],

    ["PA + Cancer Specific", "Cigna Manipal", 180.00, 180.00, 25.0],

    ["Cancer Specific", "Cigna Manipal", 156.00, 156.00, 25.0],

    ["GTL", "IPRU", 450.00, None, None],
    ["GTL", "Aviva", 320.30, None, 10.0],

    ["PA + CI", "Magma", 270.00, 300.00, 10.0],
    ["PA + CI", "Cigna Manipal", 368.00, 368.00, 25.0],

    ["GCL", "Digit", None, None, 32.5],
    ["GCL", "Aviva (HL & LAP)", None, None, 10.0],

    ["CI", "Cigna Manipal", 344.00, 344.00, 25.0],

    ["Health", "Aditya Birla", 1879.00, 1879.00, 25.0],
    ["Health", "18-60", 2699.00, 2287.00, None],
    ["Health", "3369 Plan", 3369.00, 3369.00, None],
]

FALLBACK_COLUMNS = [
    "Product",
    "Insurer",
    "Insurer Base Rate",
    "KC Base Rate",
    "COA %"
]


# ============================================================
# CLEAN EXCEL DATA
# ============================================================

def clean_rate_master(df):

    df = df.copy()

    # Forward fill merged Product cells
    if "Product" in df.columns:
        df["Product"] = df["Product"].ffill()

    # Convert Product and Insurer to clean text
    for col in ["Product", "Insurer"]:

        if col in df.columns:

            df[col] = df[col].astype(str).str.strip()

            df.loc[
                df[col].isin(["nan", "None", ""]),
                col
            ] = None

    # Extract COA from insurer text
    coa_values = []

    for insurer in df["Insurer"]:

        if pd.isna(insurer):
            coa_values.append(None)
            continue

        text = str(insurer)

        match = re.search(
            r'@(\d+(?:\.\d+)?)%',
            text
        )

        if match:
            coa_values.append(float(match.group(1)))

        elif "nil coa" in text.lower():
            coa_values.append(0.0)

        else:
            coa_values.append(None)

    df["COA %"] = coa_values

    # Clean insurer display name
    def clean_insurer_name(name):

        if pd.isna(name):
            return name

        name = str(name)

        name = re.sub(
            r'\s*\(.*?@\d+(?:\.\d+)?%\)',
            '',
            name
        )

        name = re.sub(
            r'\s*@\d+(?:\.\d+)?%',
            '',
            name
        )

        name = re.sub(
            r'\s*\(Nil COA\)',
            '',
            name,
            flags=re.IGNORECASE
        )

        return name.strip()

    df["Insurer"] = df["Insurer"].apply(clean_insurer_name)

    # Convert rates to numeric
    for col in [
        "Insurer Base Rates",
        "Insurer Base Rate",
        "KC Base Rate"
    ]:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # Standardize column name
    if (
        "Insurer Base Rates" in df.columns
        and "Insurer Base Rate" not in df.columns
    ):
        df = df.rename(
            columns={
                "Insurer Base Rates": "Insurer Base Rate"
            }
        )

    # Ensure columns exist
    required_columns = [
        "Product",
        "Insurer",
        "Insurer Base Rate",
        "KC Base Rate",
        "COA %"
    ]

    for col in required_columns:

        if col not in df.columns:
            df[col] = None

    # Remove empty rows
    df = df.dropna(
        subset=["Product", "Insurer"]
    )

    return df[required_columns]


# ============================================================
# LOAD SHEET2
# ============================================================

@st.cache_data
def load_rate_master():

    file_options = [
        "rate_master.xlsx",
        "Rate Master.xlsx",
        "rates.xlsx"
    ]

    for file_name in file_options:

        if Path(file_name).exists():

            try:

                df = pd.read_excel(
                    file_name,
                    sheet_name="Sheet2"
                )

                df.columns = [
                    str(col).strip()
                    for col in df.columns
                ]

                return clean_rate_master(df)

            except Exception:
                pass

    # Fallback if Excel is not found
    return pd.DataFrame(
        FALLBACK_DATA,
        columns=FALLBACK_COLUMNS
    )


# ============================================================
# CALCULATION
# ============================================================

def calculate_inrate(
    input_price,
    insurer_base_rate,
    coa_percent
):

    # Input Price - Insurer Base Rate
    x_amount = (
        input_price
        - insurer_base_rate
    )

    # COA Amount
    coa_amount = (
        insurer_base_rate
        * (coa_percent / 100)
    )

    # In-Rate Amount
    inrate_amount = (
        x_amount
        + coa_amount
    )

    # In-Rate Percentage
    inrate_percent = (
        inrate_amount
        / input_price
    ) * 100

    return {
        "x_amount": x_amount,
        "coa_amount": coa_amount,
        "inrate_amount": inrate_amount,
        "inrate_percent": inrate_percent
    }


# ============================================================
# LOAD DATA
# ============================================================

rates = load_rate_master()


# ============================================================
# APP HEADER
# ============================================================

st.markdown(
    """
<div class="app-title">
    🛡️ Insurance In-Rate Calculator
</div>

<div class="app-subtitle">
    Calculate the in-rate percentage instantly using insurer base rates and COA.
</div>
""",
    unsafe_allow_html=True
)


# ============================================================
# STEP 01 - INPUT
# ============================================================

st.markdown(
    """
<div class="section-kicker">STEP 01</div>
<div class="section-title">Calculation Input</div>
<div class="section-description">
Select the product and insurer, then enter the client rate.
</div>
""",
    unsafe_allow_html=True
)


products = sorted(
    rates["Product"]
    .dropna()
    .unique()
)


col1, col2, col3 = st.columns(3)


# PRODUCT
with col1:

    product = st.selectbox(
        "Product",
        products
    )


# FILTER INSURERS
product_rates = rates[
    rates["Product"] == product
].copy()


insurers = sorted(
    product_rates["Insurer"]
    .dropna()
    .unique()
)


# INSURER
with col2:

    insurer = st.selectbox(
        "Insurer",
        insurers
    )


# SELECT ROW
selected_row = product_rates[
    product_rates["Insurer"] == insurer
].iloc[0]


insurer_base_rate = selected_row[
    "Insurer Base Rate"
]

coa_percent = selected_row[
    "COA %"
]


# CLIENT RATE INPUT
with col3:

    default_rate = 100.0

    if pd.notna(insurer_base_rate):
        default_rate = float(insurer_base_rate)

    input_price = st.number_input(
        "Client Rate (₹)",
        min_value=0.0,
        value=default_rate,
        step=1.0
    )


# ============================================================
# VALIDATION
# ============================================================

can_calculate = True


if input_price <= 0:

    st.error(
        "Please enter a Client Rate greater than ₹0."
    )

    can_calculate = False


if pd.isna(insurer_base_rate):

    st.warning(
        "Insurer Base Rate is not configured for this combination."
    )

    can_calculate = False


if pd.isna(coa_percent):

    st.warning(
        "COA percentage is not configured for this combination."
    )

    can_calculate = False


# ============================================================
# STEP 02 - RESULTS
# ============================================================

if can_calculate:

    result = calculate_inrate(
        input_price=float(input_price),
        insurer_base_rate=float(insurer_base_rate),
        coa_percent=float(coa_percent)
    )


    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown(
        """
<div class="section-kicker">STEP 02</div>
<div class="section-title">Calculation Results</div>
<div class="section-description">
Your calculated in-rate result.
</div>
""",
        unsafe_allow_html=True
    )


    r1, r2, r3, r4 = st.columns(4)


    # CARD 1
    with r1:

        html = (
            f'<div class="result-card base-card">'
            f'<div class="card-label">INSURER BASE RATE</div>'
            f'<div class="card-value">₹{float(insurer_base_rate):,.2f}</div>'
            f'<div class="card-note">Backend configured rate</div>'
            f'</div>'
        )

        st.markdown(
            html,
            unsafe_allow_html=True
        )


    # CARD 2
    with r2:

        html = (
            f'<div class="result-card x-card">'
            f'<div class="card-label">X AMOUNT</div>'
            f'<div class="card-value">₹{result["x_amount"]:,.2f}</div>'
            f'<div class="card-note">Client Rate − Base Rate</div>'
            f'</div>'
        )

        st.markdown(
            html,
            unsafe_allow_html=True
        )


    # CARD 3
    with r3:

        html = (
            f'<div class="result-card inrate-card">'
            f'<div class="card-label">IN-RATE AMOUNT</div>'
            f'<div class="card-value">₹{result["inrate_amount"]:,.2f}</div>'
            f'<div class="card-note">Includes COA of {float(coa_percent):.2f}%</div>'
            f'</div>'
        )

        st.markdown(
            html,
            unsafe_allow_html=True
        )


    # CARD 4
    with r4:

        html = (
            f'<div class="result-card coa-card">'
            f'<div class="card-label">COA AMOUNT</div>'
            f'<div class="card-value">₹{result["coa_amount"]:,.2f}</div>'
            f'<div class="card-note">{float(coa_percent):.2f}% of Base Rate</div>'
            f'</div>'
        )

        st.markdown(
            html,
            unsafe_allow_html=True
        )


    # ========================================================
    # FINAL IN-RATE %
    # ========================================================

    final_html = (
        f'<div class="final-result">'
        f'<div class="final-label">FINAL IN-RATE PERCENTAGE</div>'
        f'<div class="final-value">{result["inrate_percent"]:.2f}%</div>'
        f'</div>'
    )

    st.markdown(
        final_html,
        unsafe_allow_html=True
    )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Policygrace Internal Pricing Tool • Insurance In-Rate Calculator"
)
