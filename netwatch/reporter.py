from datetime import datetime


def generate_report(host: str, summary) -> str:
    total = summary["total_checks"] or 0
    failures = summary["failures"] or 0

    availability = (
        ((total - failures) / total) * 100
        if total else 0
    )

    lines = [
        "=" * 45,
        f"NETWATCH REPORT: {host}",
        "=" * 45,
        f"Generated: {datetime.now().isoformat(timespec='seconds')}",
        f"Total checks: {total}",
        f"Failures: {failures}",
        f"Availability: {availability:.2f}%",
    ]

    if summary["avg_latency"] is not None:
        lines.extend([
            f"Minimum latency: {summary['min_latency']:.2f} ms",
            f"Maximum latency: {summary['max_latency']:.2f} ms",
            f"Average latency: {summary['avg_latency']:.2f} ms",
        ])
    else:
        lines.append("Latency: No successful measurements")

    lines.append("=" * 45)

    return "\n".join(lines)
