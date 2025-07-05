# 🔧 Project: Wi-Fi Device Tracking System

✅ Phase 1: Environment & Tool Setup
1. Install OS and Tools
Ensure you're using a Linux distro like Kali Linux or Ubuntu with support for monitor mode.

        sudo apt update && sudo apt install aircrack-ng tcpdump wireshark hostapd isc-dhcp-server freeradius python3 python3-pip
Install Python packages:
   
    pip3 install scapy flask pandas numpy
3. Enable Monitor Mode on Wi-Fi Interface
List your wireless interfaces:

        iwconfig

Put your interface in monitor mode:

    sudo ip link set wlan0 down
    sudo iw dev wlan0 set type monitor
    sudo ip link set wlan0 up

📡 Phase 2: Packet Sniffing & MAC Capture
1. Passive Probe Request Capture with airodump-ng

        sudo airodump-ng wlan0mon --write wifi_probes --output-format csv

This captures:

    Probing MACs

    SSIDs requested

    Signal strength (RSSI)

Filter probe requests:

