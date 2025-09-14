import socket
import os
import platform
import subprocess

def get_local_ip():
# Get the local IP address of the current machine
hostname = socket.gethostname()
local_ip = socket.gethostbyname(hostname)
return local_ip

def ping_sweep(network):
# Determine the operating system
param = ‘-n’ if platform.system().lower() == ‘windows’ else ‘-c’

# Create a list to store the active IPs
active_ips = []

# Ping addresses on the network
for i in range(1, 255):
    ip = f"{network}.{i}"
    command = ['ping', param, '1', ip]
    response = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if response.returncode == 0:
        active_ips.append(ip)
        print(f"Active IP: {ip}")

return active_ips

def main():
# Example network, replace with your actual network prefix
network_prefix = ‘192.168.1’

print("Local IP Address:", get_local_ip())
print("Scanning for active IP addresses...")
active_ips = ping_sweep(network_prefix)
print("Active IP addresses found:", active_ips)

if name == “main”:
main()
