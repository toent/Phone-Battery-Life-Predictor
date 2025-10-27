import pandas as pd

# --- CONFIGURATION ---
INPUT_FILE = "python-scripts/mnt/data/mod/Data Collection Smartphone Battery Life(Sheet1)_with_capacity.csv"
OUTPUT_FILE = INPUT_FILE.replace(".csv", "_with_estimated_life.csv")

# --- LOAD DATA ---
df = pd.read_csv(INPUT_FILE)

# --- VALIDATE REQUIRED COLUMNS ---
required_cols = ["startbatterypercentage", "endbatterypercentage", "sessionlength"]
for col in required_cols:
    if col not in df.columns:
        raise ValueError(f"Missing required column: {col}")

# --- CLEAN AND CONVERT DATA ---
df["startbatterypercentage"] = pd.to_numeric(df["startbatterypercentage"], errors="coerce")
df["endbatterypercentage"] = pd.to_numeric(df["endbatterypercentage"], errors="coerce")
df["sessionlength"] = pd.to_numeric(df["sessionlength"], errors="coerce")

# --- CALCULATE BATTERY DRAIN AND ESTIMATED LIFE ---
def estimate_battery_life(row):
    start = row["startbatterypercentage"]
    end = row["endbatterypercentage"]
    session_time = row["sessionlength"]

    # Skip invalid or reversed values
    if pd.isna(start) or pd.isna(end) or pd.isna(session_time):
        return None
    if start <= end:
        return None

    drained_percent = start - end
    if drained_percent <= 0:
        return None

    # Estimate full battery lifetime (in seconds)
    estimated_remaining_life = (session_time / drained_percent) * start
    return int(round(estimated_remaining_life))  # round to whole seconds

# --- APPLY FUNCTION ---
df["estimated_remaining_life_s"] = df.apply(estimate_battery_life, axis=1)

# --- SAVE OUTPUT ---
df.to_csv(OUTPUT_FILE, index=False)

# --- SUMMARY ---
valid_rows = df["estimated_remaining_life_s"].notna().sum()
avg_life = df["estimated_remaining_life_s"].mean()
print(f"Added 'estimated_remaining_life_s' (rounded to whole seconds) for {valid_rows} rows.")
if not pd.isna(avg_life):
    print(f"Average estimated remaining life: {avg_life/3600:.2f} hours.")
print(f"Saved file: {OUTPUT_FILE}")