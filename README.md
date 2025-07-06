# 🔧 Project: Wi-Fi Device Tracking System

## 📦 Components and Their Functions

| **Component**                   | **Function**                                                       |
| ------------------------------ | ------------------------------------------------------------------ |
| **Monitor Mode + Airodump-ng** | Passive sniffing of all nearby probe requests & beacons            |
| **ARP/Nmap Scan + ARP Table**  | Extract hostname, MAC, and IP when the device is online            |
| **CSV Log Generator**          | Save captured data in a daily log for future analysis              |
| **RSSI Handler**    | Estimate device proximity using received signal strength (RSSI)    |
| **MAC Randomization Detection**| Identify randomized MAC addresses via SSID probe pattern analysis  |

---

✅ Phase 1: Environment & Tool Setup
1. Install OS and Tools
Ensure you're using a Linux distro like Kali Linux or Ubuntu with support for monitor mode.

        sudo apt update && sudo apt install aircrack-ng tcpdump wireshark hostapd isc-dhcp-server freeradius python3 python3-pip
Install Python packages:
   
    pip3 install scapy flask pandas numpy
3. Enable Monitor Mode on Wi-Fi Interface
List your wireless interfaces:

        iwconfig

## 🔸 Next Step: Enable Monitor Mode

To begin passive packet capture, enable **Monitor Mode** on your Wi-Fi interface using the following command:

```
sudo airmon-ng start <your_wifi_interface>
```
Example:
````
sudo airmon-ng start wlx90de8007d432
````

📡 Phase 2: Packet Sniffing & MAC Capture
1. Passive Probe Request Capture with airodump-ng

        sudo airodump-ng wlan0mon --write wifi_probes --output-format csv

After run the above command need to be wait 1-2 minutes to scan and collect logs then Press CTRL+C to exit. This captures:

    Probing MACs

    SSIDs requested

    Signal strength (RSSI)

The logs looks like:
![image](https://github.com/user-attachments/assets/e9291f62-9228-494d-84d7-c2ee53ff362c)

Filter probe requests:

## Next Step: Parse Captured Devices (Passive Probe Requests)
Create parse_passive_scan.py

````
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
    print("❌ Could not find Station MAC section. Please check the CSV format.")
    exit(1)

print("✅ Found Station MAC section.\n")

# Extract MAC + probe info
for line in lines[station_start:]:
    if line.strip():
        parts = line.strip().split(',')
        if len(parts) >= 6:
            mac = parts[0]
            rssi = parts[3]
            probes = parts[-1]
            print(f"MAC: {mac}, RSSI: {rssi}, Probing SSIDs: {probes}")
````

Locates the Station MAC section in the CSV (bottom half of airodump-ng output). Parses each line for: MAC address, Signal strength, Probed SSIDs (helps in MAC de-randomization).

## 🧪 Run it:
````
python3 parse_passive_scan.py
````
Result looks like:
![image](https://github.com/user-attachments/assets/b6c54087-ea37-46ec-818d-bdaec4fa0b50)

## IP, Hostname, MAC Mapping (Active Scan)

Use ARP/NMAP to Get Hostnames. Create get_hostnames.py:

````
import os
import datetime
import subprocess

def scan_network():
    today = datetime.datetime.now().strftime("%Y-%m-%d")
    logfile = f"device_log_{today}.csv"
    os.system("sudo nmap -sn 192.168.37.0/24 > nmap_output.txt")
    os.system("arp -a > arp_table.txt")
    
    with open("arp_table.txt") as f, open(logfile, "w") as out:
        out.write("Hostname,IP,MAC\n")
        for line in f:
            parts = line.split()
            if len(parts) >= 4:
                hostname = parts[0]
                ip = parts[1].strip("()")
                mac = parts[3]
                out.write(f"{hostname},{ip},{mac}\n")

if __name__ == "__main__":
    scan_network()
````
Run:
````
python3 get_hostnames.py
````
This will generate a daily CSV log file like device_log_2025-06-16.csv

# Automate Logging (Optional)- ((System Automation setup will be stated here later after confirmation of the test))

Use cron to schedule:
````
crontab -e
````

.......................................................
