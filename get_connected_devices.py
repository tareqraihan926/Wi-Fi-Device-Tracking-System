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
