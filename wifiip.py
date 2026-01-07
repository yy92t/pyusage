import socket
import platform
import subprocess
import argparse
import ipaddress
import re
from typing import Optional
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_local_ip():
    # Best-effort local IPv4 detection.
    # Uses a UDP "connect" trick (no packets sent) to learn the default route IP.
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except OSError:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)


def _last_octet(ip: str) -> int:
    return int(ip.rsplit(".", 1)[-1])


def _mask_ip(ip: str) -> str:
    parts = ip.split(".")
    if len(parts) == 4:
        parts[-1] = "x"
        return ".".join(parts)
    return "x.x.x.x"


def _build_targets(network_prefix_or_cidr: str, *, max_hosts: int = 4096) -> list[str]:
    """Return a list of IPv4 target strings.

    Accepts either:
    - Prefix form: "192.168.1" (scans .1..254)
    - CIDR form:   "192.168.1.0/24" (scans usable hosts)

    To avoid accidental huge scans, CIDRs producing more than `max_hosts` targets
    raise a ValueError.
    """
    if "/" in network_prefix_or_cidr:
        net = ipaddress.ip_network(network_prefix_or_cidr, strict=False)
        if net.version != 4:
            raise ValueError("Only IPv4 networks are supported")
        targets = [str(ip) for ip in net.hosts()]
        if len(targets) > max_hosts:
            raise ValueError(
                f"Network too large ({len(targets)} hosts). "
                f"Use a smaller CIDR (e.g. /24) or adjust the code to allow it."
            )
        return targets

    # Prefix mode: assume a /24 and scan .1..254
    return [f"{network_prefix_or_cidr}.{i}" for i in range(1, 255)]


def _mask_mac(mac: str) -> str:
    # Keep vendor-ish prefix, hide device-specific tail.
    parts = mac.split(":")
    if len(parts) == 6:
        return ":".join(parts[:3] + ["xx", "xx", "xx"])
    return "xx:xx:xx:xx:xx:xx"


def _read_arp_table() -> dict[str, str]:
    """Best-effort ARP cache read (IP -> MAC).

    No packet sniffing. This only reads the OS neighbor/ARP cache.
    """
    system = platform.system().lower()
    commands: list[list[str]] = []

    if system == "darwin":
        # `-n` avoids reverse-DNS lookups that can make `arp -a` hang.
        commands = [["arp", "-an"], ["arp", "-a"]]
    elif system == "windows":
        commands = [["arp", "-a"]]
    else:
        # Linux: prefer `ip neigh`, fall back to `arp -n`.
        commands = [["ip", "neigh"], ["arp", "-n"]]

    output: Optional[str] = None
    last_error: Optional[Exception] = None

    for cmd in commands:
        try:
            proc = subprocess.run(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                stdin=subprocess.DEVNULL,
                text=True,
                timeout=5.0,
                check=False,
            )
        except FileNotFoundError as e:
            last_error = e
            continue
        except subprocess.TimeoutExpired as e:
            last_error = e
            continue

        if proc.returncode == 0 and proc.stdout:
            output = proc.stdout
            break

        last_error = RuntimeError(proc.stderr.strip() or f"command failed: {' '.join(cmd)}")

    if output is None:
        if last_error is None:
            return {}
        raise RuntimeError(f"Unable to read ARP table: {last_error}")

    table: dict[str, str] = {}

    if system == "darwin":
        # Example: ? (192.168.1.1) at aa:bb:cc:dd:ee:ff on en0 ifscope [ethernet]
        pattern = re.compile(r"\((\d+\.\d+\.\d+\.\d+)\)\s+at\s+([0-9a-fA-F:]{17}|\(incomplete\))")
        for line in output.splitlines():
            m = pattern.search(line)
            if not m:
                continue
            ip, mac = m.group(1), m.group(2)
            if mac == "(incomplete)":
                continue
            table[ip] = mac.lower()

    elif system == "windows":
        # Example row:  192.168.1.1          aa-bb-cc-dd-ee-ff     dynamic
        row = re.compile(r"^(\s*)(\d+\.\d+\.\d+\.\d+)\s+([0-9a-fA-F\-]{17})\s+(dynamic|static)")
        for line in output.splitlines():
            m = row.match(line)
            if not m:
                continue
            ip = m.group(2)
            mac = m.group(3).replace("-", ":").lower()
            table[ip] = mac

    else:
        # ip neigh: 192.168.1.1 dev wlan0 lladdr aa:bb:cc:dd:ee:ff REACHABLE
        neigh = re.compile(r"^(\d+\.\d+\.\d+\.\d+).+\blladdr\s+([0-9a-fA-F:]{17})\b")
        for line in output.splitlines():
            m = neigh.search(line)
            if m:
                table[m.group(1)] = m.group(2).lower()
                continue

        # arp -n: 192.168.1.1 ether aa:bb:cc:dd:ee:ff C eth0
        arp_n = re.compile(r"^(\d+\.\d+\.\d+\.\d+)\s+\S+\s+([0-9a-fA-F:]{17})\b")
        for line in output.splitlines():
            m = arp_n.match(line.strip())
            if m:
                table[m.group(1)] = m.group(2).lower()

    return table


def ping_sweep(
    network: str,
    *,
    reveal: bool = False,
    timeout_s: float = 1.5,
    workers: int = 64,
) -> list[str]:
    # Determine the operating system
    param = "-n" if platform.system().lower() == "windows" else "-c"

    def ping_one(ip: str) -> Optional[str]:
        command = ["ping", param, "1", ip]
        try:
            response = subprocess.run(
                command,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                stdin=subprocess.DEVNULL,
                timeout=timeout_s,
            )
        except subprocess.TimeoutExpired:
            return None
        except FileNotFoundError as e:
            raise RuntimeError("'ping' command not found on this system") from e

        return ip if response.returncode == 0 else None

    active_ips: list[str] = []
    ips = _build_targets(network)

    try:
        with ThreadPoolExecutor(max_workers=max(1, workers)) as pool:
            futures = [pool.submit(ping_one, ip) for ip in ips]
            for fut in as_completed(futures):
                ip = fut.result()
                if ip:
                    active_ips.append(ip)
                    if reveal:
                        print(f"Active IP: {ip}")
                    else:
                        print(f"Active host: .{_last_octet(ip)}")
    except KeyboardInterrupt:
        print("\nScan interrupted. Returning partial results...")

    active_ips.sort(key=_last_octet)
    return active_ips

def main():
    parser = argparse.ArgumentParser(
        description="Ping-sweep your local /24 network to find responsive hosts. "
        "By default, hides full IP addresses to protect local device privacy."
    )
    parser.add_argument(
        "--network",
        help=(
            "Network to scan. Examples: '192.168.1' (prefix mode) or "
            "'192.168.1.0/24' (CIDR mode). Default: derived from your local IP."
        ),
    )
    parser.add_argument(
        "--reveal",
        action="store_true",
        help="Print full IP addresses (privacy off).",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=1.5,
        help="Ping timeout in seconds (default: 1.5).",
    )
    parser.add_argument(
        "--workers",
        type=int,
        default=64,
        help="Number of concurrent ping workers (default: 64).",
    )
    parser.add_argument(
        "--arp",
        action="store_true",
        help="After scanning, show MAC addresses from the OS ARP cache.",
    )
    args = parser.parse_args()

    local_ip = get_local_ip()
    if args.network:
        network_prefix = args.network
    else:
        octets = local_ip.split(".")
        network_prefix = ".".join(octets[:3]) if len(octets) >= 3 else "192.168.1"

    if args.reveal:
        print("Local IP Address:", local_ip)
        print("Scanning for active IP addresses...")
    else:
        print("Local IP Address:", _mask_ip(local_ip))
        print("Scanning for active hosts (IPs hidden)...")

    try:
        active_ips = ping_sweep(
            network_prefix,
            reveal=args.reveal,
            timeout_s=args.timeout,
            workers=args.workers,
        )
    except ValueError as e:
        raise SystemExit(f"Invalid --network value: {e}") from e
    except RuntimeError as e:
        raise SystemExit(str(e)) from e

    if args.reveal:
        print("Active IP addresses found:", active_ips)
    else:
        print("Active hosts found:", len(active_ips))
        print("Active host last octets:", [_last_octet(ip) for ip in active_ips])

    if args.arp and active_ips:
        try:
            arp = _read_arp_table()
        except RuntimeError as e:
            print(f"ARP lookup failed (skipping): {e}")
        else:
            if args.reveal:
                print("ARP MACs (from local cache):")
                for ip in active_ips:
                    mac = arp.get(ip)
                    if mac:
                        print(f"  {ip} -> {mac}")
            else:
                print("ARP MACs (from local cache, masked):")
                for ip in active_ips:
                    mac = arp.get(ip)
                    if mac:
                        print(f"  .{_last_octet(ip)} -> {_mask_mac(mac)}")


if __name__ == "__main__":
    main()
