import csv

csv_file = "wifi_probes-01.csv"

with open(csv_file, "r", encoding="utf-8", errors="ignore") as f:
    lines = f.readlines()

# Find the index where station list starts
station_start = None
for i, line in enumerate(lines):
    if line.strip().startswith("Station MAC"):
        station_start = i + 1
        break

if station_start is None:
    print("Ã¢ï¿½Å’ Could not find Station MAC section. Please check the CSV format.")
    exit(1)

print("Ã¢Å“â€¦ Found Station MAC section.\n")

# Extract MAC + probe info
for line in lines[station_start:]:
    if line.strip():
        parts = line.strip().split(',')
        if len(parts) >= 6:
            mac = parts[0]
            rssi = parts[3]
            probes = parts[-1]
            print(f"MAC: {mac}, RSSI: {rssi}, Probing SSIDs: {probes}")
