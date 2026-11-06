# ERP Monitoring and Operations Evidence

These CSV files contain results from a controlled local Odoo 19 / PostgreSQL 16 application-support lab.

- **health_log.csv** — HTTP availability checks, simulated application outage, and recovery verification.
- **ops_checks.csv** — PostgreSQL connectivity, stock reconciliation, exception detection, and scheduled operational checks.
- **CHG001_test.csv** — HTTP response-time measurements from the monitoring enhancement test.
- **CHG001_rollback_test.csv** — HTTP check performed using the original monitoring script during rollback rehearsal.

The first health-log entry is a separate connectivity-failure test, not part of incident INC-001.

These are local testing results, not production monitoring or enterprise SLA measurements.
