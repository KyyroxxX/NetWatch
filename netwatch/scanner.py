import socket
from concurrent.futures import ThreadPoolExecutor, as_completed
from dataclasses import dataclass


@dataclass
class PortResult:
    host: str
    port: int
    open: bool
    service: str


def scan_port(host: str, port: int, timeout: float = 1.0) -> PortResult:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return PortResult(
                host=host,
                port=port,
                open=True,
                service=socket.getservbyport(port, "tcp")
                if port <= 1023 else "unknown",
            )
    except (OSError, socket.timeout):
        return PortResult(host, port, False, "unknown")


def scan_ports(host: str, ports: list[int], timeout: float = 1.0):
    if not host.strip():
        raise ValueError("Host cannot be empty")

    if not ports:
        raise ValueError("At least one port is required")

    if any(port < 1 or port > 65535 for port in ports):
        raise ValueError("Ports must be between 1 and 65535")

    results = []

    with ThreadPoolExecutor(max_workers=min(len(ports), 100)) as executor:
        futures = [
            executor.submit(scan_port, host, port, timeout)
            for port in ports
        ]

        for future in as_completed(futures):
            results.append(future.result())

    return sorted(results, key=lambda result: result.port)
