#!/usr/bin/env python3
"""HTTP availability check and latency capture for a local Odoo test instance."""
import argparse
import csv
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check(url, timeout):
    started = time.perf_counter()
    status = "ERROR"
    error = ""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as response:
            status = str(response.status)
            healthy = 200 <= response.status < 400
    except urllib.error.HTTPError as exc:
        status = str(exc.code)
        healthy = False
        error = str(exc)
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        healthy = False
        error = str(exc)
    return {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "url": url,
        "available": "YES" if healthy else "NO",
        "http_status": status,
        "latency_ms": round((time.perf_counter() - started) * 1000, 2),
        "error": error,
    }


def main():
    p = argparse.ArgumentParser(description="Monitor an ERP login page")
    p.add_argument("--url", default="http://127.0.0.1:8069/web/login")
    p.add_argument("--count", type=int, default=1, help="Number of checks")
    p.add_argument("--interval", type=float, default=5.0, help="Seconds between checks")
    p.add_argument("--timeout", type=float, default=3.0)
    p.add_argument("--warn-ms", type=float, default=500.0,
                   help="Response-time warning threshold in milliseconds")
    p.add_argument("--log", type=Path, default=ROOT / "reports/health_log.csv")
    args = p.parse_args()
    if args.count < 1 or args.interval < 0 or args.timeout <= 0 or args.warn_ms <= 0:
        p.error("count >= 1, interval >= 0 and timeout > 0 required")
    args.log.parent.mkdir(parents=True, exist_ok=True)
    append = args.log.exists() and args.log.stat().st_size > 0
    failed = 0
    with args.log.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["timestamp_utc", "url", "available", "http_status", "latency_ms", "error"])
        if not append:
            writer.writeheader()
        for i in range(args.count):
            entry = check(args.url, args.timeout)
            writer.writerow(entry)
            handle.flush()
            if entry["available"] == "NO":
                failed += 1
            state = (
                "DOWN" if entry["available"] == "NO"
                else "SLOW" if entry["latency_ms"] >= args.warn_ms
                else "OK"
            )
            print(f"{entry['timestamp_utc']} health={state} available={entry['available']} status={entry['http_status']} latency_ms={entry['latency_ms']}")
            if i < args.count - 1:
                time.sleep(args.interval)
    print(f"Recorded {args.count} check(s), {failed} failure(s) -> {args.log}")
    raise SystemExit(1 if failed else 0)


if __name__ == "__main__":
    main()
