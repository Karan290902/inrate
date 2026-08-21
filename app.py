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
        radial-gradient(circle at 5% 0%, rgba(37, 99, 235, 0.08), transparent 28%),
        radial-gradient(circle at 95% 100%, rgba(16, 185, 129, 0.06), transparent 28%),
        #f8fafc;
}

.block-container {
    max-width: 1150px;
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.app-title {
    font-size: 34px;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: -0.8px;
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
    letter-spacing: 1.5px;
    color: #2563eb;
    margin-bottom: 4px;
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

/* RESULT CARDS */

.result-card {
    border-radius: 18px;
    padding: 22px;
    min-height: 165px;
    color: white;
    box-shadow: 0 12px 28px rgba(15, 23, 42, 0.12);
}

.card-label {
    font-size: 11px;
    font-weight: 800;
    letter-spacing: 1px;
    opacity: 0.85;
    margin-bottom: 16px;
}

.card-value {
    font-size: 34px;
    font-weight: 850;
    letter-spacing: -1px;
}

.card-note {
    font-size: 12px;
    margin-top: 14px;
    opacity: 0.82;
}

.input-card {
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 16px;
    padding: 18px;
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

.percent-card {
    background: linear-gradient(135deg, #111827, #334155);
}

.final-result {
    background: linear-gradient(135deg, #1d4ed8, #2563eb);
    color: white;
    padding: 28px;
    border-radius: 20px;
    text-align: center;
    margin-top: 22px;
    box-shadow: 0 15px 35px rgba(37, 99, 235, 0.20);
}

.final-label {
    font-size: 13px;
    font-weight: 800;
    letter-spacing: 1.5px;
    opacity: 0.85;
}

.final-value {
    font-size: 48px;
    font-weight: 850;
    margin-top: 8px;
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
# FALLBACK RATE MASTER
# Based on latest pasted table
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
    ["Health", "Not Configured", 3369.00, 3369.00, None],
]

FALLBACK_COLUMNS = [
    "Product",
    "Insurer",
    "Insurer Base Rate",
    "KC Base Rate",
    "COA %"
]


# ============================================================
# LOAD EXCEL - SHEET2 ONLY
# ============================================================

@st.cache_data
def load_rate_master():

    possible_files = [
        "rate_master.xlsx",
        "Rate Master.xlsx",
        "rates.xlsx"
    ]

    for file_name in possible_files:

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

    fallback_df = pd.DataFrame(
        FALLBACK_DATA,
        columns=FALLBACK_COLUMNS
    )

    return fallback_df


# ============================================================
# CLEAN RATE MASTER
# ============================================================

def clean_rate_master(df):

    df = df.copy()

    # Normalize possible column names

    rename_map = {}

    for col in df.columns:

        clean_col = str(col).strip().lower()

        if "product" in clean_col:
            rename_map[col] = "Product"

        elif "insurer" in clean_col:
            rename_map[col] = "Insurer"

        elif "insurer base" in clean_col:
            rename_map[col] = "Insurer Base Rate"

        elif "kc base" in clean_col:
            rename_map[col] = "KC Base Rate"

    df = df.rename(columns=rename_map)

    # Forward fill merged Product cells

    if "Product" in df.columns:
        df["Product"] = df["Product"].ffill()

    # Clean text

    for col in ["Product", "Insurer"]:

        if col in df.columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
            )

            df.loc[
                df[col].isin(["nan", "None", ""]),
                col
            ] = None

    # Parse COA from insurer text

    coa_values = []

    for insurer in df["Insurer"]:

        if pd.isna(insurer):

            coa_values.append(None)
            continue

        insurer_text = str(insurer)

        match = re.search(
            r'@(\d+(?:\.\d+)?)%',
            insurer_text
        )

        if match:
            coa_values.append(
                float(match.group(1))
            )

        elif "nil coa" in insurer_text.lower():
            coa_values.append(0.0)

        else:
            coa_values.append(None)

    df["COA %"] = coa_values

    # Clean insurer display names

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

    df["Insurer"] = df["Insurer"].apply(
        clean_insurer_name
    )

    # Numeric conversion

    for col in [
        "Insurer Base Rate",
        "KC Base Rate",
        "COA %"
    ]:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # Keep only usable rows

    required_cols = [
        "Product",
        "Insurer",
        "Insurer Base Rate",
        "COA %"
    ]

    for col in required_cols:

        if col not in df.columns:
            df[col] = None

    df = df.dropna(
        subset=["Product", "Insurer"]
    )

    return df[
        [
            "Product",
            "Insurer",
            "Insurer Base Rate",
            "KC Base Rate",
            "COA %"
        ]
    ]


# ============================================================
# CALCULATION FUNCTION
# ============================================================

def calculate_inrate(
    input_price,
    base_rate,
    coa_percent
):

    x_amount = input_price - base_rate

    coa_amount = (
        base_rate
        * (coa_percent / 100)
    )

    inrate_amount = (
        x_amount
        + coa_amount
    )

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

st.markdown("""
<div class="app-title">
    🛡️ Insurance In-Rate Calculator
</div>

<div class="app-subtitle">
    Calculate In-Rate Amount and In-Rate Percentage instantly.
</div>
""", unsafe_allow_html=True)


# ============================================================
# CALCULATION INPUT
# ============================================================

st.markdown("""
<div class="section-kicker">
STEP 01
</div>

<div class="section-title">
Calculation Input
</div>

<div class="section-description">
Select the product and insurer, then enter the client-side input price.
</div>
""", unsafe_allow_html=True)


products = sorted(
    rates["Product"]
    .dropna()
    .unique()
)

col1, col2, col3 = st.columns(3)


with col1:

    product = st.selectbox(
        "Product",
        products
    )


filtered_rates = rates[
    rates["Product"] == product
].copy()


insurers = sorted(
    filtered_rates["Insurer"]
    .dropna()
    .unique()
)


with col2:

    insurer = st.selectbox(
        "Insurer",
        insurers
    )


selected_row = filtered_rates[
    filtered_rates["Insurer"] == insurer
].iloc[0]


base_rate = selected_row[
    "Insurer Base Rate"
]

coa_percent = selected_row[
    "COA %"
]


default_input = 100.0

if pd.notna(base_rate):
    default_input = max(
        float(base_rate),
        1.0
    )


with col3:

    input_price = st.number_input(
        "Input Price (₹)",
        min_value=0.0,
        value=float(default_input),
        step=1.0
    )


# ============================================================
# VALIDATION
# ============================================================

can_calculate = True


if input_price <= 0:

    st.error(
        "Please enter an Input Price greater than ₹0."
    )

    can_calculate = False


if pd.isna(base_rate):

    st.warning(
        "Insurer Base Rate is not configured for this combination."
    )

    can_calculate = False


if pd.isna(coa_percent):

    st.warning(
        "COA % is not configured for this Product/Insurer combination."
    )

    can_calculate = False


if (
    can_calculate
    and input_price < float(base_rate)
):

    st.warning(
        "Input Price is lower than the Insurer Base Rate. "
        "Please verify the entered amount."
    )


# ============================================================
# RESULTS
# ============================================================

if can_calculate:

    result = calculate_inrate(
        input_price=float(input_price),
        base_rate=float(base_rate),
        coa_percent=float(coa_percent)
    )


    st.markdown("<br>", unsafe_allow_html=True)


    st.markdown("""
    <div class="section-kicker">
    STEP 02
    </div>

    <div class="section-title">
    Calculation Results
    </div>

    <div class="section-description">
    In-Rate calculated using the selected insurer base rate and COA percentage.
    </div>
    """, unsafe_allow_html=True)


    r1, r2, r3, r4 = st.columns(4)


    with r1:

        st.markdown(
            f"""
            <div class="result-card base-card">

                <div class="card-label">
                    INSURER BASE RATE
                </div>

                <div class="card-value">
                    ₹{float(base_rate):,.2f}
                </div>

                <div class="card-note">
                    Backend configured rate
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with r2:

        st.markdown(
            f"""
            <div class="result-card x-card">

                <div class="card-label">
                    X AMOUNT
                </div>

                <div class="card-value">
                    ₹{result["x_amount"]:,.2f}
                </div>

                <div class="card-note">
                    Input Price − Base Rate
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with r3:

        st.markdown(
            f"""
            <div class="result-card inrate-card">

                <div class="card-label">
                    IN-RATE AMOUNT
                </div>

                <div class="card-value">
                    ₹{result["inrate_amount"]:,.2f}
                </div>

                <div class="card-note">
                    Includes COA of {float(coa_percent):.2f}%
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    with r4:

        st.markdown(
            f"""
            <div class="result-card percent-card">

                <div class="card-label">
                    COA AMOUNT
                </div>

                <div class="card-value">
                    ₹{result["coa_amount"]:,.2f}
                </div>

                <div class="card-note">
                    {float(coa_percent):.2f}% of Base Rate
                </div>

            </div>
            """,
            unsafe_allow_html=True
        )


    # ========================================================
    # FINAL IN-RATE %
    # ========================================================

    st.markdown(
        f"""
        <div class="final-result">

            <div class="final-label">
                FINAL IN-RATE PERCENTAGE
            </div>

            <div class="final-value">
                {result["inrate_percent"]:.2f}%
            </div>

        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # FORMULA
    # ========================================================

    with st.expander("View Calculation"):

        st.write(
            f"**Input Price:** ₹{input_price:,.2f}"
        )

        st.write(
            f"**Insurer Base Rate:** ₹{float(base_rate):,.2f}"
        )

        st.write(
            f"**COA %:** {float(coa_percent):.2f}%"
        )

        st.divider()

        st.write(
            "**X Amount = Input Price − Insurer Base Rate**"
        )

        st.write(
            f"₹{input_price:,.2f} − "
            f"₹{float(base_rate):,.2f} = "
            f"₹{result['x_amount']:,.2f}"
        )

        st.divider()

        st.write(
            "**COA Amount = Insurer Base Rate × COA %**"
        )

        st.write(
            f"₹{float(base_rate):,.2f} × "
            f"{float(coa_percent):.2f}% = "
            f"₹{result['coa_amount']:,.2f}"
        )

        st.divider()

        st.write(
            "**In-Rate Amount = X Amount + COA Amount**"
        )

        st.write(
            f"₹{result['x_amount']:,.2f} + "
            f"₹{result['coa_amount']:,.2f} = "
            f"₹{result['inrate_amount']:,.2f}"
        )

        st.divider()

        st.write(
            "**Final In-Rate % = "
            "(In-Rate Amount ÷ Input Price) × 100**"
        )

        st.write(
            f"(₹{result['inrate_amount']:,.2f} ÷ "
            f"₹{input_price:,.2f}) × 100 = "
            f"**{result['inrate_percent']:.2f}%**"
        )


# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.caption(
    "Policygrace Internal Pricing Tool • "
    "Insurance In-Rate Calculator"
)
