import argparse
from datetime import datetime

from netwatch.database import init_database, get_recent_measurements


def main():
    parser = argparse.ArgumentParser(
        description="NetWatch - Monitoring History"
    )

    parser.add_argument(
        "--limit",
        type=int,
        default=20,
        help="Number of measurements to display",
    )

    args = parser.parse_args()

    if args.limit < 1:
        parser.error("Limit must be a positive integer")

    init_database()

    rows = get_recent_measurements(args.limit)

    print("\n========== NetWatch History ==========")

    if not rows:
        print("No measurements found.")
        return

    for row in rows:
        timestamp = datetime.fromtimestamp(
            row["timestamp"]
        ).strftime("%Y-%m-%d %H:%M:%S")

        status = "ONLINE" if row["reachable"] else "OFFLINE"

        latency = (
            f"{row['latency_ms']:.2f} ms"
            if row["latency_ms"] is not None
            else "N/A"
        )

        print(
            f"{timestamp} | {row['host']} | "
            f"{status} | {latency}"
        )


if __name__ == "__main__":
    main()
