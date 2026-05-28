# MODEL.md — Data Model and Design Rationale

# Overview

The Breathe ESG platform is designed to ingest emissions-related data from multiple enterprise systems and normalize them into one centralized analytical model.

Different enterprise systems produce data in different formats:

* SAP exports operational fuel and manufacturing activity
* Utility portals export electricity and energy consumption
* Travel systems export business travel records

Instead of forcing all incoming data into one structure immediately, the system uses a **two-layer architecture**:

1. Raw ingestion tables preserve uploaded data exactly as received
2. A normalized `EmissionRecord` table stores standardized emissions data used by the dashboard and analyst workflows

This design provides:

* audit traceability
* source-level debugging
* consistent reporting
* validation tracking
* scalable ingestion pipelines

---

# Core Design Principles

The data model was designed around five goals:

1. Multi-tenancy
2. Auditability
3. Source traceability
4. Data normalization
5. Analyst review workflow

Every table is tenant-scoped, every transformation is traceable, and every emission calculation can be traced back to its original uploaded row.

---

# 1. Tenant

Represents an enterprise client using the Breathe ESG platform.

Examples:

* Tata Motors
* Reliance Industries
* Infosys

## Fields

```text
id
name
created_at
```

## Why it exists

The platform supports multiple companies from a single deployment.

Every major table contains:

```python
tenant = models.ForeignKey(Tenant)
```

This ensures complete tenant isolation.

No tenant can access another tenant’s data.

---

# 2. Facility

Represents a physical operational site.

Examples:

* Mumbai Manufacturing Plant
* Pune Warehouse
* Bangalore Office

## Fields

```text
id
tenant
facility_code
facility_name
facility_type
city
country
is_active
created_at
```

## Why it exists

Emissions are generated at the facility level, not only company-wide.

Facilities allow:

* plant-level dashboards
* regional filtering
* operational segmentation
* audit traceability

## Important Design Decision

`facility_code` mirrors SAP plant codes.

Example:

```text
MU01
PU02
BLR01
```

This allows uploaded SAP rows to automatically map to facilities.

---

# 3. SAPRecord (Raw Ingestion Table)

Stores uploaded SAP CSV rows exactly as received.

## Fields

### Common ingestion fields

```text
id
tenant
facility
upload_id
raw_row
ingestion_status
error_notes
created_at
```

### SAP-specific fields

```text
material_code
material_name
plant_code
company_code
raw_quantity
parsed_quantity
raw_unit
parsed_unit
description
```

---

## Why raw + parsed values are both stored

Uploaded enterprise files often contain inconsistent formats.

Example:

```text
1.200,50
```

This must be parsed into:

```text
1200.50
```

Both values are stored to preserve audit traceability.

---

## Why raw_row exists

`raw_row` stores the complete original uploaded row as JSON.

This ensures:

* no uploaded information is lost
* debugging is easier
* ingestion rules can be improved later
* auditors can inspect the original source

---

# 4. UtilityRecord (Raw Ingestion Table)

Stores uploaded utility consumption data.

## Fields

### Common ingestion fields

```text
id
tenant
facility
upload_id
raw_row
ingestion_status
error_notes
created_at
```

### Utility-specific fields

```text
utility_type
raw_quantity
parsed_quantity
raw_unit
parsed_unit
provider_name
period_from
period_to
```

---

## Why utility normalization matters

Utility providers export energy data in different units:

```text
kWh
MWh
GWh
```

The platform normalizes everything into standard units before emissions are calculated.

Both raw and normalized values are preserved.

---

# 5. TravelRecord

Stores corporate travel activity.

## Fields

```text
id
tenant
facility
upload_id
raw_row
ingestion_status
error_notes
travel_type
origin
destination
distance_km
traveler_name
created_at
```

---

## Why travel is separate

Travel emissions behave differently from operational emissions.

Flights, hotels, and ground transportation belong to Scope 3 emissions and follow different emission factor logic.

The model separates travel data to:

* simplify ingestion
* simplify calculations
* maintain traceability

---

# 6. EmissionRecord (Normalized Table)

The central ESG analytics table.

All valid emissions eventually become normalized `EmissionRecord` rows.

The dashboard, review workflow, and KPI system all read from this table.

---

# Fields

## Identity

```text
id
tenant
facility
```

---

## Source Tracking

```text
source_type
source_record_id
source_file_name
created_at
```

---

## Activity Data

```text
activity_type
activity_date
```

Examples:

```text
Diesel
Electricity
Flight
Hotel stay
Ground transport
```

---

## Quantity Normalization

```text
original_quantity
original_unit
normalized_quantity
normalized_unit
```

This preserves both:

* original uploaded values
* normalized analytical values

---

## Emissions Calculation

```text
scope
emission_factor
emission_factor_source
co2e_kg
```

---

## Review Workflow

```text
status
review_notes
reviewer_email
reviewed_at
locked_at
```

---

# Review Lifecycle

Every emission row passes through a review lifecycle.

## Initial ingestion

```text
status = pending
```

## Analyst review

Analyst may:

* approve
* flag
* lock

---

## Status meanings

### Pending

Waiting for analyst review.

### Approved

Validated and accepted.

### Flagged

Requires further investigation.

### Locked

Finalized for audit purposes.

---

# How the Two-Layer Architecture Works

```text
CSV Upload
    ↓

Raw Ingestion Table
(SAPRecord / UtilityRecord / TravelRecord)

    ↓

Validation + Parsing

    ↓

Failed rows stay in raw tables

Clean rows create EmissionRecord

    ↓

Analyst Review Workflow

    ↓

Approved / Flagged / Locked
```

---

# Multi-Tenancy Strategy

Every major table includes:

```python
tenant = ForeignKey(Tenant)
```

Queries are always tenant-scoped:

```python
EmissionRecord.objects.filter(
    tenant=selected_tenant
)
```

This ensures strict tenant isolation.

---

# Scope Categorization

The system classifies emissions into standard GHG Protocol scopes.

## Scope 1

Direct operational emissions.

Examples:

* Diesel
* LPG
* Natural Gas

Usually from SAP operational uploads.

---

## Scope 2

Purchased electricity emissions.

Examples:

* Grid electricity
* Purchased energy

Usually from utility uploads.

---

## Scope 3

Indirect external emissions.

Examples:

* Flights
* Hotels
* Ground travel

Usually from travel records.

---

# Source Traceability

Every EmissionRecord maintains complete traceability back to its origin.

## Fields used

```text
source_type
source_record_id
source_file_name
```

This allows auditors to:

* identify the original upload
* inspect the raw uploaded row
* verify normalization
* verify emission calculations

---

# Auditability Design

Auditability is a core requirement.

The platform preserves:

* original uploaded values
* parsed values
* normalized values
* validation decisions
* analyst notes
* review timestamps

No transformation destroys original data.

---

# Current System Limitations

The current implementation intentionally excludes:

* asynchronous ingestion queues
* XLSX parsing
* real-time streaming ingestion
* dynamic emission factor registry
* role-based permissions
* advanced approval hierarchies
* large-scale pagination
* automated reconciliation workflows

These are future scalability enhancements.
