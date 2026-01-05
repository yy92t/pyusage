import socket
import platform
import subprocess
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_local_ip():
    # Get the local IP address of the current machine
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    return local_ip

def ping_sweep(network):
    # Determine the operating system
    param = "-n" if platform.system().lower() == "windows" else "-c"

    def ping_one(ip: str) -> str | None:
        command = ["ping", param, "1", ip]
        try:
            response = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=1.5,
            )
        except subprocess.TimeoutExpired:
            return None

        return ip if response.returncode == 0 else None

    active_ips: list[str] = []
    ips = [f"{network}.{i}" for i in range(1, 255)]

    with ThreadPoolExecutor(max_workers=64) as pool:
        futures = [pool.submit(ping_one, ip) for ip in ips]
        for fut in as_completed(futures):
            ip = fut.result()
            if ip:
                active_ips.append(ip)
                print(f"Active IP: {ip}")

    active_ips.sort(key=lambda s: int(s.rsplit(".", 1)[-1]))
    return active_ips

def main():
    local_ip = get_local_ip()
    octets = local_ip.split(".")
    network_prefix = ".".join(octets[:3]) if len(octets) >= 3 else "192.168.1"

    print("Local IP Address:", local_ip)
    print("Scanning for active IP addresses...")
    active_ips = ping_sweep(network_prefix)
    print("Active IP addresses found:", active_ips)


if __name__ == "__main__":
    main()
