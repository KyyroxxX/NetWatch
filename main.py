import argparse
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from netwatch.monitor import ping_host
from netwatch.alerts import log_event
from netwatch.database import (
    init_database,
    save_measurement,
    get_host_summary,
)


def main():
    parser = argparse.ArgumentParser(
        description="NetWatch - Concurrent Network Monitoring Tool"
    )

    parser.add_argument(
        "hosts",
        nargs="+",
        help="IP addresses or hostnames to monitor",
    )

    parser.add_argument(
        "--timeout",
        type=int,
        default=2,
        help="Ping timeout in seconds",
    )

    parser.add_argument(
        "--interval",
        type=int,
        default=5,
        help="Seconds between monitoring cycles",
    )

    args = parser.parse_args()

    if args.timeout < 1 or args.interval < 1:
        parser.error("Timeout and interval must be positive integers")

    hosts = list(dict.fromkeys(args.hosts))

    init_database()

    print("\n========== NetWatch ==========")
    print(f"Monitoring {len(hosts)} host(s)")
    print(f"Interval: {args.interval}s")
    print("Mode: Concurrent")
    print("Database: SQLite")
    print("Press Ctrl+C to stop.\n")

    log_event(f"Monitoring started for hosts: {', '.join(hosts)}")

    previous_states = {}

    try:
        with ThreadPoolExecutor(
            max_workers=min(len(hosts), 20)
        ) as executor:

            while True:
                cycle_start = time.perf_counter()

                print(f"\n[{time.strftime('%H:%M:%S')}] Monitoring cycle")

                futures = {
                    executor.submit(
                        ping_host,
                        host,
                        args.timeout,
                    ): host
                    for host in hosts
                }

                for future in as_completed(futures):
                    host = futures[future]

                    try:
                        result = future.result()

                    except Exception as error:
                        print(f"[ERROR] {host}: {error}")
                        log_event(
                            f"Monitoring error for {host}: {error}",
                            "error",
                        )
                        continue

                    # Persist measurement in SQLite
                    save_measurement(result)

                    status = "ONLINE" if result.reachable else "OFFLINE"

                    latency = (
                        f"{result.latency_ms:.2f} ms"
                        if result.latency_ms is not None
                        else "N/A"
                    )

                    summary = get_host_summary(host)

                    total = summary["total_checks"] or 0
                    failures = summary["failures"] or 0

                    loss = (
                        failures / total * 100
                        if total > 0
                        else 0
                    )

                    print(f"\nHost: {host}")
                    print(f"Status: {status}")
                    print(f"Current: {latency}")

                    if summary["min_latency"] is not None:
                        print(
                            f"MIN: {summary['min_latency']:.2f} ms"
                        )
                        print(
                            f"MAX: {summary['max_latency']:.2f} ms"
                        )
                        print(
                            f"AVG: {summary['avg_latency']:.2f} ms"
                        )

                    print(f"LOSS: {loss:.2f}%")
                    print(f"Total checks: {total}")

                    previous = previous_states.get(host)

                    if previous is not None and previous != result.reachable:

                        if result.reachable:
                            message = f"{host} recovered and is ONLINE"

                            print(f"[RECOVERY] {message}")
                            log_event(message)

                        else:
                            message = f"{host} went OFFLINE"

                            print(f"[ALERT] {message}")
                            log_event(message, "warning")

                    previous_states[host] = result.reachable

                elapsed = time.perf_counter() - cycle_start

                time.sleep(max(0, args.interval - elapsed))

    except KeyboardInterrupt:
        print("\n[INFO] Monitoring stopped.")
        log_event("Monitoring stopped by user")

        print("\n========== FINAL SUMMARY ==========")

        for host in hosts:
            summary = get_host_summary(host)

            total = summary["total_checks"] or 0
            failures = summary["failures"] or 0

            loss = (
                failures / total * 100
                if total > 0
                else 0
            )

            print(f"\nHost: {host}")
            print(f"Checks: {total}")
            print(f"Failures: {failures}")
            print(f"Packet loss: {loss:.2f}%")

            if summary["avg_latency"] is not None:
                print(
                    f"Average latency: "
                    f"{summary['avg_latency']:.2f} ms"
                )


if __name__ == "__main__":
    main()
