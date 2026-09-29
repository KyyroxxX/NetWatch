import platform
import subprocess
import time
from dataclasses import dataclass


@dataclass
class PingResult:
    host: str
    reachable: bool
    latency_ms: float | None
    packet_loss: int
    timestamp: float


def ping_host(host: str, timeout: int = 2) -> PingResult:
    """
    Check host availability using the system ping command.
    """

    system = platform.system().lower()

    if system == "windows":
        command = ["ping", "-n", "1", "-w", str(timeout * 1000), host]
    else:
        command = ["ping", "-c", "1", "-W", str(timeout), host]

    start = time.perf_counter()

    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=timeout + 2,
            check=False,
        )

        elapsed = (time.perf_counter() - start) * 1000

        if result.returncode == 0:
            return PingResult(
                host=host,
                reachable=True,
                latency_ms=round(elapsed, 2),
                packet_loss=0,
                timestamp=time.time(),
            )

        return PingResult(
            host=host,
            reachable=False,
            latency_ms=None,
            packet_loss=100,
            timestamp=time.time(),
        )

    except (subprocess.TimeoutExpired, FileNotFoundError):
        return PingResult(
            host=host,
            reachable=False,
            latency_ms=None,
            packet_loss=100,
            timestamp=time.time(),
        )
