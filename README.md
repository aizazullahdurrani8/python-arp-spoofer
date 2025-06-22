# 🛠️ ARP Spoofer (Python & Scapy)

A Python tool that performs ARP spoofing using Scapy to intercept communication between a target device and the network gateway.

## ⚠️ Disclaimer

This script is intended for **educational and authorized testing** purposes only. Unauthorized use on networks you don’t own or have permission to test is **illegal**.

## ✅ Features

- Performs ARP spoofing between a target and a gateway
- Restores original ARP tables on exit (CTRL+C)
- Shows packet count in real-time
- Uses Scapy for low-level network packet crafting

## 🚀 Usage

```bash
sudo python arp_spoofer.py -t <target_ip> -g <gateway_ip>
```

## 🔍 Example:

    sudo python arp_spoofer.py -t 192.168.1.5 -g 192.168.1.1

## 🧠 Requirements

- Python 3 installed on your system.

- Scapy library

Install Scapy:

    pip install scapy
