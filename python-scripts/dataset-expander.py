import pandas as pd
import numpy as np
import random

# --- Load Original Dataset ---
file_path = "python-scripts/mnt/data/Data Collection Smartphone Battery Life(Sheet1).csv"
df = pd.read_csv(file_path, sep=";")
df.columns = [
    "id", "userage", "usergender", "userphone", "phoneos", "batteryhealth",
    "startbatterypercentage", "endbatterypercentage", "sessionlength", "timedonphone",
    "appcount", "screenbrightness", "usednetwork", "usedbluetooth", "usedGPS", "usedbatterysaving"
]

# --- Phone Specifications (mAh and relative power draw multiplier) ---
phone_specs = {
    # iPhones
    "iPhone 11": (3110, 1.0),
    "iPhone 12": (2815, 1.1),
    "iPhone 13": (3240, 1.1),
    "iPhone 13 Pro": (3095, 1.15),
    "iPhone 13 Pro Max": (4352, 1.15),
    "iPhone 14": (3279, 1.15),
    "iPhone 14 Pro": (3200, 1.2),
    "iPhone 14 Pro Max": (4323, 1.2),
    "iPhone 15": (3349, 1.2),
    "iPhone 15 Pro": (3274, 1.25),
    "iPhone 15 Pro Max": (4422, 1.25),
    "iPhone 16": (3550, 1.25),
    "iPhone 16 Pro": (3580, 1.3),
    "iPhone 16 Pro Max": (4670, 1.3),
    "iPhone 17": (3720, 1.35),
    "iPhone 17 Pro": (3820, 1.4),
    "iPhone 17 Pro Max": (4870, 1.4),
    "iPhone Air": (2900, 1.05),

    # Samsung
    "Samsung Galaxy S22": (3700, 1.25),
    "Samsung Galaxy S23": (3900, 1.3),
    "Samsung Galaxy S23+": (4700, 1.3),
    "Samsung Galaxy S23 Ultra": (5000, 1.35),
    "Samsung Galaxy S24": (4000, 1.35),
    "Samsung Galaxy S24 Ultra": (5000, 1.4),
    "Samsung Galaxy S25": (4200, 1.4),
    "Samsung Galaxy S25 Ultra": (5100, 1.45),
    "Samsung Galaxy Z Fold 5": (4400, 1.5),
    "Samsung Galaxy Z Fold 6": (4600, 1.55),
    "Samsung Galaxy Z Fold 7": (4700, 1.6),
    "Samsung Galaxy Z Flip 5": (3700, 1.4),
    "Samsung Galaxy Z Flip 6": (3800, 1.45),
    "Samsung Galaxy Z Flip 7": (3900, 1.5),

    # Samsung Galaxy Edge
    "Galaxy S6 Edge": (2600, 0.9),
    "Galaxy S7 Edge": (3600, 0.95),
    "Galaxy S25 Edge": (4200, 1.45),

    # Others
    "Google Pixel 7": (4355, 1.25),
    "Google Pixel 8": (4575, 1.3),
    "OnePlus 10": (5000, 1.3),
    "Xiaomi 12": (4500, 1.3),
    "Huawei P50": (4100, 1.2),
}

phones = list(phone_specs.keys())

oses = ["Android", "iOs"]
gender_options = ["Man", "Woman", "Non-binary", "Prefer not to say"]
gender_probs = [0.55, 0.35, 0.05, 0.05]
net_options = ["Yes", "No"]
bool_options = ["Yes", "No"]

n_new = 123
new_data = []

for i in range(n_new):
    userage = np.random.randint(16, 75)
    usergender = np.random.choice(gender_options, p=gender_probs)

    # --- Weighted phone selection by age ---
    flagship_phones = [
        "iPhone 16", "iPhone 16 Pro", "iPhone 16 Pro Max",
        "iPhone 17", "iPhone 17 Pro", "iPhone 17 Pro Max",
        "Samsung Galaxy S23", "Samsung Galaxy S23+", "Samsung Galaxy S23 Ultra",
        "Samsung Galaxy S24", "Samsung Galaxy S24 Ultra",
        "Samsung Galaxy S25", "Samsung Galaxy S25 Ultra",
        "Samsung Galaxy Z Fold 5", "Samsung Galaxy Z Fold 6", "Samsung Galaxy Z Fold 7",
        "Samsung Galaxy Z Flip 5", "Samsung Galaxy Z Flip 6", "Samsung Galaxy Z Flip 7"
    ]

    weights = []
    for phone in phones:
        if userage < 22 and phone in flagship_phones:
            weights.append(0.01)  # very rare for <22
        elif userage < 40 and phone in flagship_phones:
            weights.append(0.3)   # moderate
        elif userage >= 40 and phone in flagship_phones:
            weights.append(0.05)  # uncommon
        else:
            weights.append(1.0)   # normal
    weights = np.array(weights) / np.sum(weights)
    userphone = np.random.choice(phones, p=weights)
    phoneos = "iOs" if "iPhone" in userphone else "Android"

    # --- Phone characteristics ---
    capacity, power_mult = phone_specs[userphone]

    # Battery health (integer, influenced by user age and battery capacity)
    base_health = 98 - (userage - 16) * 0.15
    degradation = np.interp(capacity, [2800, 5100], [0.9, 1.0])
    batteryhealth = int(np.clip(np.random.normal(base_health * degradation, 2), 70, 100))

    startbatterypercentage = np.random.randint(70, 101)

    # --- Usage behavior ---
    usednetwork = np.random.choice(net_options, p=[0.8, 0.2])
    usedbluetooth = np.random.choice(bool_options, p=[0.4, 0.6])  # more No than Yes
    usedGPS = np.random.choice(bool_options, p=[0.23, 0.77])        # 80% No, 20% Yes
    usedbatterysaving = np.random.choice(bool_options, p=[0.3, 0.7])

    # App count based on age — lower and more realistic
    appcount = int(np.random.normal(6 if userage < 30 else 5, 2))
    appcount = max(3, min(appcount, 15))

    # Phone usage pattern (session length = seconds, timedonphone = Yes/No)
    timedonphone = np.random.choice(["Yes", "No"], p=[0.85, 0.15])
    sessionlength = round(np.random.normal(900 if timedonphone == "Yes" else 200, 150), 1)
    sessionlength = max(60, sessionlength)

    # Screen brightness — many users use full brightness
    if np.random.rand() < 0.55:
        screenbrightness = np.random.randint(80, 101)
    else:
        screenbrightness = np.random.randint(20, 80)
    if usedbatterysaving == "Yes":
        screenbrightness = min(screenbrightness, np.random.randint(10, 50))

    # --- Battery drain ---
    drain_factor = (
        0.1 * (screenbrightness / 50)
        + 0.2 * (appcount / 40)
        + 0.05 * power_mult
    )
    if usednetwork == "Yes": drain_factor += 0.15
    if usedbluetooth == "Yes": drain_factor += 0.05
    if usedGPS == "Yes": drain_factor += 0.1
    if usedbatterysaving == "Yes": drain_factor -= 0.2

    battery_drop = int(np.clip(np.random.normal(10 * drain_factor, 3), 1, 40))
    endbatterypercentage = max(startbatterypercentage - battery_drop, 1)

    # Append new row
    new_data.append([
        len(df) + i + 1, userage, usergender, userphone, phoneos, batteryhealth,
        startbatterypercentage, endbatterypercentage, sessionlength, timedonphone,
        appcount, screenbrightness, usednetwork, usedbluetooth, usedGPS, usedbatterysaving
    ])

# --- Merge and Save ---
new_df = pd.DataFrame(new_data, columns=df.columns)
combined_df = pd.concat([df, new_df], ignore_index=True)

output_path = "python-scripts/mnt/data/Data Collection Smartphone Battery Life_expanded.csv"
combined_df.to_csv(output_path, index=False)
print(f"Expanded dataset saved to:\n{output_path}")
