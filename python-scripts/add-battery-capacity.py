import pandas as pd
from collections import Counter

# --- CONFIGURATION ---
INPUT_FILE = "python-scripts/mnt/data/Data Collection Smartphone Battery Life(Sheet1).csv"
OUTPUT_FILE = INPUT_FILE.replace(".csv", "_with_capacity.csv")

# --- LOAD DATA ---
df = pd.read_csv(INPUT_FILE)

# --- DEFINE TRANSFORMATION ---
def get_battery_capacity(phone_name: str):
    """Return battery capacity (mAh) for a given phone name (case/space tolerant)."""
    if not isinstance(phone_name, str):
        return "unknown"

    n = phone_name.lower().strip()

    # --- APPLE ---
    if "iphone 17 pro max" in n: return 5088
    if "iphone 17 pro" in n: return 4252
    if "iphone 17" in n: return 3692
    if "iphone 16 pro max" in n: return 4685
    if "iphone 16 pro" in n: return 3582
    if "iphone 16" in n: return 3561
    if "iphone 15 pro max" in n: return 4422
    if "iphone 15 pro" in n: return 3274
    if "iphone 15" in n: return 3349
    if "iphone 14 pro max" in n: return 4323
    if "iphone 14 pro" in n: return 3200
    if "iphone 14" in n: return 3279
    if "iphone 13 pro max" in n: return 4352
    if "iphone 13 pro" in n: return 3095
    if "iphone 13" in n: return 3227
    if "iphone 12" in n: return 2815
    if "iphone 11" in n: return 3110
    if "iphone air" in n: return 3149

    # --- SAMSUNG S SERIES ---
    if "samsung galaxy s25 ultra" in n: return 5000
    if "samsung galaxy s25 edge" in n or "galaxy s25 edge" in n: return 3900
    if "samsung galaxy s25" in n: return 4000
    if "samsung galaxy s24 ultra" in n: return 5000
    if "samsung galaxy s24" in n: return 4000
    if "samsung galaxy s23 ultra" in n: return 5000
    if "samsung galaxy s23" in n: return 3900
    if "samsung galaxy s22" in n: return 3700
    if "galaxy s7 edge" in n: return 3600
    if "galaxy s6 edge" in n: return 2600

    # --- SAMSUNG FOLDABLES ---
    if "samsung z fold 7" in n or "galaxy z fold 7" in n: return 4400
    if "samsung z fold 6" in n or "galaxy z fold 6" in n: return 4400
    if "samsung z flip 7" in n or "galaxy z flip 7" in n: return 4300
    if "samsung z flip 6" in n or "galaxy z flip 6" in n: return 4000
    if "samsung z flip 5" in n or "galaxy z flip 5" in n: return 3700

    # --- GOOGLE PIXEL ---
    if "google pixel 8" in n: return 4575
    if "google pixel 7" in n: return 4355

    # --- ASUS ROG ---
    if "rog phone 8 pro edition" in n or "rog phone 8 pro" in n: return 5500

    # --- XIAOMI / HUAWEI / ONEPLUS ---
    if "xiaomi 12" in n: return 4500
    if "huawei p50" in n: return 4100
    if "oneplus 10" in n: return 4800

    # --- UNKNOWN ---
    return 0


# --- APPLY TRANSFORMATION ---
df["batterycapacity_mAh"] = df["userphone"].apply(get_battery_capacity)

# --- SUMMARY ---
counts = Counter(df["batterycapacity_mAh"])
print("✅ Battery capacity column added.\n")
print("🔹 Capacity distribution:")
for cap, count in counts.items():
    print(f"  {cap:>8} mAh : {count} rows")

# --- SAVE OUTPUT ---
df.to_csv(OUTPUT_FILE, index=False)
print(f"\n💾 Saved updated dataset to: {OUTPUT_FILE}")
