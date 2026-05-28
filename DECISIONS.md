# DECISIONS.md — Architecture Decisions and Tradeoffs

This document explains every significant technical and architectural decision made during the development of the Breathe ESG platform. For each decision: what options were considered, what was chosen, why, what tradeoffs were accepted, and what I would ask the PM if given the opportunity.

---

## 1. SAP Ingestion — CSV Flat File Over IDoc or OData

### Options Considered

- SAP IDoc (Intermediate Document — native SAP interchange format)
- SAP OData REST API
- Flat file CSV export

### Final Decision

CSV flat file, pipe delimited with German headers.

### Why This Was Chosen

**IDoc** is SAP's native format but requires ALE/EDI middleware to parse. No enterprise client would expose IDoc directly to a third-party ESG platform without significant IT involvement. It is a system-to-system integration format, not a reporting export format.

**OData** requires live authenticated access to the SAP system, security configuration, network whitelisting, and IT approval. A new enterprise client onboarding scenario — which is exactly the context described in the assignment — rarely starts with live system API access. IT procurement and security approvals alone take weeks.

**CSV flat file** is what sustainability teams actually receive in practice. A finance or operations manager runs a standard SAP report (transaction MB51 for material movements, ME2M for procurement) and exports it as a CSV file. This is the file they email to the ESG team or upload to a portal. This is the realistic starting point for onboarding.

### What the System Handles

- Pipe delimited flat file — SAP uses pipe to avoid conflicts with German number formatting where periods are thousands separators and commas are decimal separators
- German column headers: BUKRS (company code), BLDAT (document date), MATNR (material number), MENGE (quantity), MEINS (unit of measure), WERKS (plant), BKTXT (description)
- German date format DD.MM.YYYY
- German decimal notation — "500,00" parsed to 500.00, "1.200,50" parsed to 1200.50
- Material codes requiring lookup — DIESEL01 resolved to "Diesel" via lookup table
- Plant codes requiring lookup — MU01 resolved to "Mumbai Plant" via Facility table

### What Was Intentionally Ignored

- SAP IDoc middleware integration
- Live SAP OData APIs
- Multiple SAP module exports (handling MM module material movements only, not FI financials or CO controlling)
- UTF-16 encoding (some SAP exports produce UTF-16 with German special characters)
- Semicolon delimited variants (some European SAP configurations use semicolons)
- Real-time SAP synchronization

### Tradeoff Accepted

CSV ingestion is a manual upload step — the analyst must receive the file from the SAP admin and upload it. An OData integration would be fully automated but requires infrastructure and security complexity not appropriate for a prototype.

### What I Would Ask the PM

- Which SAP transaction does the client use to export fuel and procurement data?
- Do they have a fixed export template or does each plant configure their own column set?
- Is there a plant code master list (SAP table T001W) we can get from the client upfront?
- Which SAP modules are in scope — MM only, or also FI and CO?

---

## 2. Utility Ingestion — Portal CSV Export Over PDF or API

### Options Considered

- PDF bill parsing (pdfplumber, camelot, AWS Textract)
- Utility provider API (Green Button, provider-specific APIs)
- Portal CSV export

### Final Decision

CSV portal export, comma delimited.

### Why This Was Chosen

**PDF parsing** for utility bills is deceptively complex. Every utility provider (MSEDCL, Tata Power, BESCOM, KSEB) formats their bills differently. A parser built for Tata Power bills breaks on MSEDCL bills. Scanned PDFs require OCR. Digital PDFs embed consumption data in unstructured text paragraphs. Building reliable multi-provider PDF parsing represents weeks of engineering work with significant ongoing maintenance as providers change their bill layouts. High complexity, low reliability.

**Utility APIs** exist in the US (Green Button standard) but adoption in India is inconsistent. Most Indian utility providers offer portal CSV downloads but not programmatic APIs. Even where APIs exist, they require account credentials and provider-specific authentication.

**CSV portal export** covers the most common real-world case. The facilities manager logs into the utility portal, selects a date range, and downloads usage history as a structured CSV. This is what corporate energy managers do daily across every major Indian city.

### Important Design Decision — Billing Periods

Utility billing periods do not align with calendar months. A meter might bill from Feb 3 to Mar 7. Both `period_from` and `period_to` are stored on UtilityRecord. The `period_to` date is used as the `activity_date` on EmissionRecord because the end of the billing period is the most accurate single-date representation. This is a simplification — a rigorous system would prorate consumption across calendar months for monthly reporting accuracy.

### What the System Handles

- Comma delimited CSV
- Mixed units: kWh, MWh, GWh — all normalized to kWh (MWh × 1000, GWh × 1,000,000)
- Irregular billing periods stored as period_from and period_to
- Multiple meters per account — meter_id tracked on every record
- Tariff types: Flat and Time of Use (ToU)
- Case-insensitive unit parsing — "KWH", "kwh", "kWh" all handled

### What Was Intentionally Ignored

- PDF bill parsing
- Real-time smart meter API data
- Demand charges and peak/off-peak tariff breakdowns
- Power factor correction values
- Reactive power (kVAR) data
- Estimated vs actual meter read distinction

### Tradeoff Accepted

CSV export requires manual download and upload by the facilities manager. An API integration would automate this but is not available from most Indian providers.

### What I Would Ask the PM

- Do clients have multiple utility providers across facilities?
- Should billing periods be prorated to calendar months for reporting?
- Which emission factor to use — DEFRA 2023 uses a UK grid factor but we used 0.82 kg CO₂e/kWh for India grid average. Should this be configurable per region?
- Should the system track estimated vs actual meter reads?

---

## 3. Travel Ingestion — Honest Account of What Happened

### Original Plan

The original architecture planned to simulate a Concur REST API integration using a mock JSON endpoint. The travel ingestion would call this endpoint and parse the JSON response — demonstrating understanding of how enterprise travel platforms actually expose data via REST APIs.

### What Happened

I spent approximately 2 days implementing this approach. The plan involved:
1. A mock endpoint in Django returning Concur-style JSON
2. The ingestion service calling that endpoint
3. Parsing the JSON response into TravelRecord rows

I encountered persistent issues with request handling, endpoint routing, and JSON parsing that I could not resolve within the project timeline. After 2 days without a working solution, I made a pragmatic decision to switch approaches.

### Final Decision

Travel ingestion uses CSV file upload — the same mechanism as SAP and Utility.

### Why This Was the Better Decision Under the Circumstances

Concur and Navan both support CSV exports for companies that have not configured programmatic API access. For a new enterprise client onboarding scenario, CSV export is actually the realistic starting point — IT teams at large enterprises take weeks to approve and configure OAuth2 credentials for third-party platforms.

The ingestion logic — parsing travel types, calculating distances from airport codes, applying emission factors by class, handling hotels and ground transport differently — is identical whether data arrives via CSV or API. The core domain logic is fully demonstrated. Only the data reading mechanism differs.

### What the System Handles

- Three travel types with completely different field shapes and emission factors:
  - **Flight:** origin/destination airport codes, travel class (Economy/Business/First), distance calculated from airport code lookup when not given directly
  - **Hotel:** nights, hotel name, hotel city
  - **Ground transport:** distance_km
- Distance calculation from IATA airport code pairs using great-circle approximation lookup table
- Emission factors differentiated by travel class:
  - Economy: 0.092 kg CO₂e / km
  - Business: 0.265 kg CO₂e / km (2.9× economy — larger seat allocation per passenger)
  - First: 0.434 kg CO₂e / km (4.7× economy)
- Calculated distances flagged as suspicious — analyst must verify before approving
- Unknown airport code pairs flagged as suspicious with plain English error note

### What Was Intentionally Ignored

- International flights — airport lookup covers Indian city pairs only
- Rail travel as a separate emission category
- Ferry and sea travel
- Car rental vs taxi distinction within ground transport
- Carbon offset credits claimed by the travel platform
- Employee home facility mapping (all travel attributed to facility selected at upload time)

### What I Would Build With More Time

A proper Concur OAuth2 API integration:
1. Client provides Concur API credentials as environment variables
2. System calls `/api/v3.0/travel/trips` with Bearer token
3. Token refresh handled automatically on expiry
4. Pagination loop handles 100-record page limit
5. Scheduled background job (Celery) runs nightly pull

The parsing and normalization code would remain completely unchanged.

### What I Would Ask the PM

- Does the client use Concur, Navan, or another travel platform?
- Should rail travel be included as a separate Scope 3 category?
- How should international flights outside the airport lookup table be handled?
- Should travel be attributed to the employee's home facility or to the destination?

---

## 4. Two-Layer Architecture — Raw Tables Plus EmissionRecord

### Decision

The platform stores data in two layers:
1. Raw ingestion tables (SAPRecord, UtilityRecord, TravelRecord)
2. Normalized EmissionRecord

Rather than normalizing directly into EmissionRecord on upload.

### Why

Direct normalization destroys auditability. Without raw ingestion tables:

- The original uploaded row is gone after transformation
- Parsing errors cannot be debugged after the fact
- Auditors cannot verify that transformations were correct
- If emission factors change, rows cannot be reprocessed from the original source
- A silent unit conversion bug (GAL treated as litres) would be undetectable

With raw tables, every EmissionRecord points back to its exact source row via `source_record_id`. An auditor can navigate: EmissionRecord → source_record_id=101 → SAPRecord row 101 → raw_row JSON → original file content. Complete traceability at every step.

### Flow

```
CSV uploaded
    ↓
Every row → Raw table (SAPRecord / UtilityRecord / TravelRecord)
Good AND bad rows stored here
    ↓
Validation and parsing runs on each row
    ↓
Failed / suspicious → stay in raw table, shown in Failed tab
Clean rows → EmissionRecord (status: pending)
    ↓
Analyst reviews EmissionRecord in dashboard
    ↓
Approves / Flags / Locks
```

---

## 5. Storing Both Raw and Parsed Values

### Decision

For fields with transformation risk, both the original value and the parsed value are stored side by side on every raw table row.

```
raw_date: "15.03.2024"      parsed_date: 2024-03-15
raw_quantity: "500,00"      parsed_quantity: 500.000
raw_unit: "L"               parsed_unit: "litres"
raw_consumption: "3400"     normalized_consumption: 3400000 (after MWh→kWh)
```

### Why

Enterprise ESG systems are subject to external audit. Auditors ask: "you calculated 1,325 kg CO₂e for this row — show me how." The answer requires showing the original value, the transformation, and the factor applied. If only the parsed value is stored, the transformation cannot be independently verified.

The `raw_row` JSONField on every raw table stores the complete original row exactly as it arrived — even fields that are not parsed into dedicated columns. This means no information from the original file is ever discarded.

---

## 6. Facility as a Separate Model

### Decision

Facilities were modeled as a separate table linked to Tenant, rather than storing only tenant-level emissions.

### Why

The initial design had only Tenant and EmissionRecord. Facility was added after recognizing that enterprise clients like Tata Motors operate multiple sites — manufacturing plants, assembly facilities, offices, warehouses — each producing different emission profiles.

Without facility tracking:
- Dashboard cannot filter emissions by plant
- Cannot compare emissions between facilities
- Audit traceability is incomplete — which plant produced this emission?
- Regulatory reporting often requires site-level granularity

### Important Design Choice

`facility_code` deliberately mirrors SAP plant codes (MU01, PU02, HQ). This allows SAP ingestion to automatically resolve a plant code from the uploaded file to a Facility record in the database without manual mapping. The analyst does not need to manually assign each row to a facility — it happens automatically during ingestion.

---

## 7. Scope Classification at Ingestion Time

### Decision

Emission scopes (1, 2, 3) are assigned during ingestion based on source type and activity, not calculated later.

```
SAP fuel (diesel, petrol, LPG, natural gas) → Scope 1
Utility electricity consumption              → Scope 2
Travel (flights, hotels, ground transport)  → Scope 3
```

### Why

Scope is a stable analytical attribute for these activity types. Assigning at ingestion time simplifies dashboard aggregation — the dashboard queries `WHERE scope = 'Scope 1'` without any join or calculation. It also makes the scope visible and verifiable at the row level in the analyst review workflow.

### Tradeoff

This is a simplification. A full implementation would require more granular scope logic — some SAP procurement records could be Scope 3 (purchased goods and services) if the procurement covers external supply chain activities. The current implementation assigns Scope 1 to all SAP records which is accurate only for direct fuel combustion, not all procurement categories.

---

## 8. Hardcoded Emission Factors

### Decision

Emission factors are stored as constants in `constants.py` rather than a database-driven registry.

### Why

A database-driven factor registry would require versioning, admin interface for management, effective date handling, and validation rules — significant complexity for a prototype. Hardcoded constants allow the prototype to demonstrate the full calculation pipeline without the overhead of a factor management system.

### Factors Used (DEFRA 2023)

```
Diesel:           2.65 kg CO₂e / litre
Petrol:           2.31 kg CO₂e / litre
Natural Gas:      2.04 kg CO₂e / m3
LPG:              1.56 kg CO₂e / litre
Electricity:      0.82 kg CO₂e / kWh (India grid average)
Flight Economy:   0.092 kg CO₂e / km
Flight Business:  0.265 kg CO₂e / km
Flight First:     0.434 kg CO₂e / km
Hotel:            15.0 kg CO₂e / night
Ground transport: 0.155 kg CO₂e / km
```

### Tradeoff

Updating factors requires a code change and redeployment. In production this is unacceptable — factors should be configurable through an admin interface without engineering involvement, with versioning so historical records preserve the factor that was in effect when they were calculated.

---

## 9. SQLite Instead of PostgreSQL

### Decision

SQLite is used as the development database.

### Why

SQLite requires zero setup, works immediately on any machine, and simplifies reviewer onboarding. A reviewer can clone the repository and run the project without installing or configuring a database server.

### Tradeoff

SQLite has weak concurrent write performance. Multiple simultaneous ingestion uploads would cause write contention. Not suitable for production at any meaningful scale.

### Production Choice

PostgreSQL with connection pooling (pgBouncer or Django's built-in connection pooling). Django's ORM makes migration from SQLite to PostgreSQL a configuration change with no model code changes required.

---

## 10. No Authentication Layer

### Decision

Authentication and role-based access control were intentionally excluded from the prototype.

### Why

The assignment focuses on ESG ingestion, normalization, data modeling, and analyst review workflow. Authentication adds significant infrastructure complexity (JWT tokens, session management, user model extension, middleware) without improving the demonstration of ESG domain logic.

### Tradeoff

The deployed prototype has no access control. Anyone with the URL can access all data.

### What Production Would Require

- JWT authentication for API endpoints
- Role-based access control: analyst, admin, auditor roles
- Tenant-scoped access enforcement at the authentication layer — analysts can only see their assigned clients
- Session timeout and token refresh

---

## 11. Dynamic Column Detection

### Decision

The ingestion system uses dynamic column detection and mapping rather than requiring a fixed column template.

### Why

Enterprise CSV exports are inconsistent across clients. Different companies configure SAP differently, use different report templates, and have different naming conventions. A fixed template parser breaks the moment a client uses a slightly different column name.

Dynamic detection maps common variants:

```
"Menge", "Quantity", "Qty", "Amount", "Consumption" → quantity field
"Meins", "Unit", "UOM", "Units" → unit field
"Bldat", "Date", "Posting Date", "Document Date" → date field
```

### Limitation

Dynamic detection handles common variants but cannot parse completely arbitrary or corrupted CSV structures. Completely unrecognized files fail at the ingestion level with a clear error message rather than producing incorrect data silently.

---

## 12. Validation — Three-Tier Row Classification

### Decision

Every ingested row is classified into one of three tiers rather than binary pass/fail.

```
clean      → all fields valid, values within expected ranges
suspicious → parseable but values need analyst verification
failed     → missing critical fields or unparseable values
```

### Why

Binary pass/fail is too aggressive. A row with a valid date and quantity but an unusually high value (99,999 litres of diesel) is not broken — it might be correct for a large plant. Failing it outright would discard potentially valid data. Flagging it as suspicious puts it in front of the analyst for a judgment call.

### Examples

Failed rows:
- Missing date field — cannot create a valid EmissionRecord without a date
- Unparseable quantity (e.g. "abc,00") — cannot calculate emissions without a number
- Unknown travel type — cannot assign emission factor

Suspicious rows:
- Quantity > 10,000 litres — unusually high, may be a data entry error
- Unit is GAL — gallons are ambiguous (US gallons vs imperial) in an Indian context
- Flight distance calculated from airport codes — assumption, not given data
- Unknown airport code pair — distance cannot be calculated

---

## 13. Review Workflow Design

### Decision

EmissionRecord rows pass through a four-state review lifecycle before being available for auditors.

```
pending → approved → locked
pending → flagged
```

### Why

This mirrors how enterprise ESG analysts actually work. Data cannot go directly from ingestion to audit report — an analyst must review it for plausibility, verify suspicious values, and sign off. TThe locked state is intended to represent finalized records that should no longer be editable, providing a tamper-evident workflow for auditors.

### Metadata Captured

```
reviewed_by    → analyst email who took the action
reviewed_at    → timestamp of review action
review_notes   → analyst's written justification
is_edited      → boolean flag if row was manually corrected
edited_by      → who made the correction
edit_notes     → what was changed and why
locked_at      → when row was locked for audit
```

---

## What I Would Ask the PM — Master List

Collecting all PM questions across decisions:

1. Which SAP transaction and module does the client use for fuel and procurement exports?
2. Do they have a fixed SAP export template or does each plant configure their own?
3. Is there a plant code master list we can request from the client upfront?
4. Do clients have multiple utility providers across facilities?
5. Should billing periods be prorated to calendar months for reporting accuracy?
6. Which emission factor standard to use — DEFRA 2023, EPA, IPCC, or India-specific MoEFCC factors?
7. Should emission factors be configurable per client or standardized across the platform?
8. Does the client use Concur, Navan, or another travel platform?
9. Should rail travel be included as a separate Scope 3 category?
10. How should international flights outside the airport lookup table be handled?
11. Should travel emissions be attributed to the employee's home facility or to the destination?
12. What happens after a row is locked — can it ever be unlocked, and who has authority to do so?
13. Does the client want Scope 3 to include supply chain purchased goods or only business travel?
14. What is the target reporting period — calendar year or financial year?
15. Should the system support multiple facilities reporting to a single consolidated tenant report?