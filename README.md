# IN Rate / Risk Rate Calculator

A Streamlit calculator based on the handwritten insurance rate-calculation workflow.

## Current workflow

The calculator currently follows this interpretation of the notes:

1. Receive input from the client.
2. Enter the insurer/base rate.
3. Add the backend COA rate.
4. Treat the resulting rate as the final IN/risk rate.
5. Calculate the amount against the client input.
6. Apply the configured payout percentage.
7. Optionally compare the calculated amount with an absolute insurer amount.

### Core formula

```text
Final Rate = Insurer Rate + COA Rate

Calculated Amount = Client Input × Final Rate ÷ 100

Backend Amount = (Client Input ÷ 100,000) × Amount per Lakh

Payout Amount = Calculated Amount × Payout Rate ÷ 100
```

The example visible in the notes is:

```text
5% + 21% = 26%
```

## Run locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Community Cloud

1. Create a GitHub repository.
2. Upload `app.py` and `requirements.txt`.
3. Open Streamlit Community Cloud.
4. Select the GitHub repository.
5. Set the main file to `app.py`.
6. Deploy.

## Important business-rule note

The handwriting is partially difficult to interpret. The application therefore keeps:
- COA Rate
- Amount per Lakh
- Payout Rate

as configurable backend-style inputs.

Once the exact business formula is confirmed, the calculation section can be locked to the final Policygrace underwriting logic.
