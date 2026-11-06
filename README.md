# Manufacturing ERP Operations & Application Support Lab

**Independent Portfolio Project | November 2026**

**Tech Stack:** Odoo 19 Community · PostgreSQL 16 · SQL · Python · Docker Compose · macOS launchd

## Project Overview

Implemented and tested a local manufacturing ERP environment to demonstrate end-to-end business workflows, SQL-based investigation, application monitoring, incident recovery, and IT operations automation.

The project simulates application support responsibilities in a manufacturing organization, connecting business transactions in Odoo with database-level verification and operational diagnostics.

## Implemented Workflows

### 1. Procurement and Inventory
- Created a supplier and configured raw-material products.
- Processed a purchase order for 5,000 resistors.
- Validated a partial goods receipt of 3,000 units.
- Verified the remaining 2,000-unit backorder.

### 2. Manufacturing Operations
- Configured an Electronic Assembly product and Bill of Materials.
- Defined a requirement of two resistors per assembly.
- Completed a manufacturing order for 100 assemblies.
- Verified 200 components consumed, leaving 2,800 resistors and 100 finished assemblies.

### 3. Quality-Control Simulation
- Created a Quality Hold storage location.
- Segregated 10 finished assemblies using an internal transfer.
- Documented a simulated inspection decision.
- Released the 10 units and verified stock-location balances using SQL.

### 4. SQL Investigation
- Queried actual Odoo PostgreSQL records.
- Joined product, warehouse-location and inventory tables.
- Reconciled material consumption, finished goods and internal stock transfers.

### 5. Application Monitoring and Incident Recovery
- Used Python-based HTTP monitoring to measure Odoo availability and response latency.
- Simulated an application outage while PostgreSQL remained healthy.
- Detected failed health checks and verified recovery following service restart.
- Documented a 136-second observed first-detection-to-recovery interval.

### 6. Backup and Change Management
- Restored an Odoo backup into a separate test database.
- Verified restored inventory records using SQL.
- Enhanced a starter monitoring script with OK/SLOW/DOWN classifications.
- Tested the change and rehearsed the original script as a rollback fallback.

### 7. IT Operations Automation
- Implemented a Python operations checker for database connectivity and stock reconciliation.
- Generated timestamped CSV operational reports.
- Tested inventory-mismatch detection and process exit codes.
- Configured five-minute macOS launchd scheduling and verified initial automatic execution.

## Project Evidence

The repository will contain selected Python scripts, read-only SQL queries, sanitized screenshots, and incident, change-management and quality-control reports.

Key ERP records:
- Purchase Order: `P00001`
- Manufacturing Order: `WH/MO/00001`
- Quality Hold Transfer: `WH/INT/00001`
- Quality Release Transfer: `WH/INT/00002`

## Implementation and Attribution

The project started with a supplied ERP training kit containing Docker configuration, sample datasets, and an initial HTTP monitoring script. The Odoo transactions, SQL investigations, operations-checking workflow, monitoring enhancements, and validation exercises were carried out during the project.

Original starter-kit components are distinguished from project additions where applicable.

## Scope and Limitations

This is an independent local portfolio lab, not a production enterprise deployment. Quality inspections were simulated, recovery testing used an isolated database, and scheduled monitoring was validated through its initial execution. The project does not represent professional administration of Flex, Baan, or Infor LN systems.
## View Project Implementation and Evidence

### ERP Business Workflows
- [Purchase Order and Partial Receiving](screenshots/01_purchase_order.png)
- [Completed Manufacturing Order](screenshots/02_manufacturing_order.png)
- [Quality Hold and Inspection Record](screenshots/03_quality_hold.png)
- [Quality Release Transfer](screenshots/04_quality_release.png)

### SQL and Python Implementation
- [PostgreSQL Inventory Reconciliation](sql/inventory_reconciliation.sql)
- [Python ERP Health Monitoring](scripts/monitor.py)
- [Python Operations Checker](scripts/ops_check.py)

### Incident, Quality and Change Management
- [INC-001 — Simulated Outage and Recovery](INC-001.md)
- [CHG-001 — Monitoring Enhancement and Rollback Rehearsal](CHG-001.md)
- [QC-001 — Quality Segregation and Release](QC-001.md)

### Monitoring Test Results
- [HTTP Availability and Recovery](evidence/health_log.csv)
- [Operational Checks and Stock Reconciliation](evidence/ops_checks.csv)
- [Monitoring Change Test](evidence/CHG001_test.csv)
- [Original Script Validation](evidence/CHG001_rollback_test.csv)

**Environment:** Local Odoo 19 Community and PostgreSQL 16. All incidents, inspections and recovery exercises were performed in a controlled training environment.
