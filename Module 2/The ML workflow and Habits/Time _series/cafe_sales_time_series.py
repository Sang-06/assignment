import pandas as pd
import numpy as np

# ── STEP 1 — Create Dataset ───────────────────────────
data = {
    "date": pd.date_range(start="2024-01-01", periods=30, freq="D"),
    "sales": [
        200, 220, 215, 230, 250, 245, 260, 270, 265, 280,
        300, 295, 310, 330, 325, 340, 360, 355, 370, 390,
        410, 405, 420, 440, 435, 450, 470, 465, 480, 500
    ]
}

df = pd.DataFrame(data)
print("STEP 1 — Dataset Created")

# ── STEP 2 — Prepare Time Series 
df["date"] = pd.to_datetime(df["date"])
df = df.set_index("date")
df = df.sort_index()
print("STEP 2 Data set as index, sorted")

# ── STEP 3 — Rolling Window Features 
df["rolling_mean_3"] = df["sales"].rolling(window=3).mean()
df["rolling_std_3"] = df["sales"].rolling(window=3).std()
df["rolling_max_3"] = df["sales"].rolling(window=3).max()
print("STEP 3 - Rolling Features created")

# ── STEP 4 — Lag Features 
df["lag_1"] = df["sales"].shift(1)
df["lag_7"] = df["sales"].shift(7)
print("STEP 4 - Lag features created")

# ── STEP 5 — Train Test Split
split = int(len(df) * 0.8)
train = df.iloc[:split]
test = df.iloc[split:]
print("STEP 5 Train test split done")

# ── STEP 6 — Baseline Forecasts
test = test.copy()
test["native_forecast"]      = test["lag_1"]
test["rolling_mean_forecast"] = test["rolling_mean_3"]
print("STEP 6 - Baseline forecast created")

# ── STEP 7 — MAPE Function 
def mape(actual, predicted):
    actual  = actual.dropna()
    predicted = predicted[actual.index].dropna()
    common = actual.index.intersection(predicted.index)
    actual = actual[common]
    predicted = predicted[common]
    return round((abs(actual - predicted) / actual).mean() * 100,2)

naive_mape = mape(test["sales"], test["native_forecast"])
rolling_mape = mape(test["sales"], test["rolling_mean_forecast"])
print("STEP 7 - Mape calculated")

# ── STEP 8 — Final Output
print("\n" + "=" * 55)
print("STEP 8 - Final Output")
print("=" * 55)

print("\n---First 10 rows after feature creation")
print(df.head(10).to_string())

print("\n---Train & Test Date Range")
print("Train : ", train.index[0].date(), "to", train.index[-1].date())
print("Test  : ", test.index[0].date(),  "to", test.index[-1].date())
print("Train size :", len(train), "rows")
print("Test size  :", len(test),  "rows")

print("\n--- MAPE Results ---")
print("Naive Forecast MAPE        :", naive_mape,   "%")
print("Rolling Mean Forecast MAPE :", rolling_mape, "%")

print("\n--- Conclusion ---")
if naive_mape < rolling_mape:
    print("Naive forecast performed better with lower MAPE of",
          naive_mape, "% vs", rolling_mape, "%")
else:
    print("Rolling mean forecast performed better with lower MAPE of",
          rolling_mape, "% vs", naive_mape, "%")

print("\nALL 8 Steps Completed!")

