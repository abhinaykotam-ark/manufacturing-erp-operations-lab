#!/usr/bin/env python3
"""Read-only operational checks for the local Odoo ERP."""

import argparse
import csv
import subprocess
from datetime import datetime, timezone
from decimal import Decimal
from pathlib import Path

from monitor import check

ROOT = Path(__file__).resolve().parents[1]

SQL = """
SELECT COALESCE(SUM(sq.quantity), 0)
FROM stock_quant sq
JOIN product_product pp ON sq.product_id = pp.id
JOIN stock_location sl ON sq.location_id = sl.id
WHERE pp.default_code = 'RESISTOR-10K'
  AND sl.usage = 'internal';
"""

def inventory_check():
    result = subprocess.run(
        [
            "docker", "compose", "exec", "-T", "db",
            "psql", "-U", "odoo",
            "-d", "flex_manufacturing_erp",
            "-At", "-c", SQL
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
        timeout=20,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip())
    return Decimal(result.stdout.strip())

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--warn-ms", type=float, default=500)
    parser.add_argument("--expected-stock", type=Decimal)
    args = parser.parse_args()

    if args.warn_ms <= 0:
        parser.error("--warn-ms must be positive")

    web = check("http://127.0.0.1:8069/web/login", 3)
    database_ok = "YES"
    stock = ""
    error = ""

    try:
        stock = inventory_check()
    except (RuntimeError, ValueError, ArithmeticError,
            subprocess.TimeoutExpired, OSError) as exc:
        database_ok = "NO"
        error = str(exc)

    if web["available"] == "NO":
        status = "DOWN"
    elif database_ok == "NO":
        status = "DB_ERROR"
    elif (args.expected_stock is not None
          and stock != args.expected_stock):
        status = "STOCK_MISMATCH"
    elif web["latency_ms"] >= args.warn_ms:
        status = "SLOW"
    else:
        status = "OK"

    report = ROOT / "reports" / "ops_checks.csv"
    report.parent.mkdir(parents=True, exist_ok=True)

    row = {
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "status": status,
        "odoo_available": web["available"],
        "http_status": web["http_status"],
        "latency_ms": web["latency_ms"],
        "database_ok": database_ok,
        "resistor_stock": str(stock),
        "expected_stock": (
            str(args.expected_stock)
            if args.expected_stock is not None else ""
        ),
        "error": error or web["error"],
    }

    append = report.exists() and report.stat().st_size > 0
    with report.open("a", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=row.keys())
        if not append:
            writer.writeheader()
        writer.writerow(row)

    print(
        f"status={status} "
        f"odoo={web['available']} "
        f"postgres={database_ok} "
        f"stock={stock} "
        f"latency_ms={web['latency_ms']}"
    )
    print(f"Report saved: {report}")

    raise SystemExit(
        1 if status in ("DOWN", "DB_ERROR", "STOCK_MISMATCH") else 0
    )

if __name__ == "__main__":
    main()
