# SOURCES.md — Research and Design of Data Sources

This document explains the research, assumptions, formats, and tradeoffs behind each data source used in the Breathe ESG platform.

The platform currently supports three enterprise ESG ingestion sources:

1. SAP operational fuel and procurement data
2. Utility electricity consumption data
3. Corporate travel data

Each section explains:

* what real-world format was researched
* what patterns were observed
* how the sample data was designed
* what limitations exist
* what would break in production

---

# 1. SAP Operational Fuel Data

## Real-World Research

SAP data can be exported in multiple ways depending on the company setup.

The major formats researched were:

### SAP IDoc

SAP's enterprise integration format used for:

* system-to-system communication
* middleware integrations
* ERP synchronization

Very powerful but unrealistic for a lightweight ESG onboarding workflow.

---

### SAP OData APIs

Modern REST-based APIs exposed through SAP Gateway.

Advantages:

* real-time integration
* structured responses
* enterprise-grade architecture

Problems:

* requires SAP authentication
* requires IT approval
* requires enterprise integration support
* difficult for a prototype environment

---

### Flat CSV Export

The most realistic workflow for sustainability teams.

In practice:

* finance or operations teams export reports from SAP
* reports are downloaded as CSV/text files
* ESG analysts upload them into reporting systems

This became the final ingestion format.

---

# What Was Learned About SAP Exports

SAP exports commonly include:

* German decimal formats
* abbreviated technical headers
* inconsistent delimiters
* plant codes instead of readable names
* material codes instead of fuel names

Examples:

```text id="s1"
500,00
1.200,50
```

and headers like:

```text id="s2"
BUKRS
BLDAT
MENGE
MEINS
WERKS
```

---

# Why the Sample Data Looks Realistic

The sample SAP files intentionally include:

## Clean Rows

Examples:

* diesel purchases
* petrol usage
* LPG consumption

These simulate standard operational fuel activity.

---

## Suspicious Rows

Examples:

* extremely high quantities
* unknown units
* missing facilities
* unknown material codes

These test analyst review workflows.

---

## Failed Rows

Examples:

* corrupted quantities
* invalid dates
* missing fields

These test ingestion validation handling.

---

# Important SAP Design Decisions

## Dynamic CSV Parsing

The parser attempts to automatically detect:

* delimiters
* quantities
* dates
* facilities
* units

instead of assuming fixed templates.

---

## Raw + Parsed Values Stored Together

Example:

```text id="s3"
raw_quantity = "1.200,50"

parsed_quantity = 1200.50
```

This preserves audit traceability.

---

## Facility Mapping

SAP plant codes are mapped directly to facilities.

Example:

```text id="s4"
MU01 → Mumbai Plant
PU02 → Pune Plant
```

---

# What Would Break in Production

The current parser would struggle with:

* highly customized SAP exports
* UTF-16 encoded files
* different ERP modules
* multilingual enterprise templates
* live SAP synchronization
* thousands of client-specific material codes

A production system would require:

* configurable mappings
* client-specific parsers
* metadata registries
* schema templates

---

# 2. Utility Electricity Consumption Data

## Real-World Research

Three major utility ingestion approaches were researched:

### PDF Bills

Traditional utility invoices.

Problems:

* inconsistent layouts
* OCR complexity
* unreliable parsing
* provider-specific templates

Rejected for the prototype.

---

### Utility APIs

Some countries provide utility APIs.

Examples:

* Green Button API
* smart meter integrations

Problems:

* inconsistent adoption
* limited availability
* authentication complexity

---

### CSV Portal Export

Most realistic enterprise workflow.

Facilities managers commonly:

* log into provider portals
* select date ranges
* download CSV reports

This became the chosen ingestion format.

---

# What Was Learned About Utility Data

Utility exports commonly contain:

* multiple billing periods
* inconsistent units
* multiple meters
* provider-specific naming
* irregular date ranges

Examples of units:

```text id="s5"
kWh
MWh
GWh
```

---

# Why the Sample Data Was Designed This Way

The utility samples intentionally include:

## Multiple Units

To test normalization logic:

```text id="s6"
3400 MWh
↓
3400000 kWh
```

---

## Missing Consumption

Tests failed validation handling.

---

## Invalid Dates

Tests date parsing failures.

---

## Non-Standard Units

Examples:

```text id="s7"
UNITS
```

These simulate poorly designed provider exports.

---

# Important Utility Design Decisions

## Standardized Normalization

All electricity data is normalized into:

```text id="s8"
kWh
```

regardless of the uploaded unit.

---

## Billing Period Handling

Billing periods often span multiple months.

Example:

```text id="s9"
03 Feb → 07 Mar
```

The system currently uses the billing end date as the activity date.

This simplifies reporting.

---

## Multiple Meter Support

Large facilities commonly operate multiple meters.

The model supports:

* account numbers
* meter IDs
* provider tracking

---

# What Would Break in Production

The current implementation does not support:

* peak/off-peak tariff splits
* smart meter APIs
* estimated meter reads
* regional electricity grid factors
* provider-specific schemas
* utility bill PDFs

A production ESG platform would require provider-specific ingestion adapters.

---

# 3. Corporate Travel Data

## Real-World Research

Corporate travel platforms researched included:

* SAP Concur
* Navan
* TripActions

These platforms typically provide:

* REST APIs
* CSV exports
* reporting dashboards

---

# Initial Architecture Attempt

The original design attempted to simulate:

* a Concur REST API
* mock JSON responses
* automatic ingestion endpoints

This introduced significant complexity.

---

# Final Decision

Travel ingestion was simplified into a structured upload workflow similar to SAP and Utility ingestion.

This kept the system:

* stable
* consistent
* easier to maintain
* easier to demonstrate

---

# What Was Learned About Travel Data

Travel data differs significantly by activity type.

---

## Flights

Contain:

* airport codes
* travel class
* origin/destination

Distance is often missing and must be calculated.

---

## Hotels

Contain:

* nights stayed
* hotel city
* hotel name

Emissions are calculated per night.

---

## Ground Transport

Contain:

* travel distance
* transport activity

Emissions are calculated using distance.

---

# Why the Travel Sample Data Looks This Way

The sample data intentionally includes:

## Flights Without Distances

To test airport-distance lookup calculations.

Example:

```text id="s10"
BOM → DEL
```

---

## Unknown Airport Codes

To test suspicious-row handling.

---

## Extremely Long Hotel Stays

To trigger analyst review logic.

---

## Missing Travel Dates

To test failed validation handling.

---

# Important Travel Design Decisions

## Airport Lookup-Based Distance Calculation

Flights may not contain distances.

The system calculates approximate distances using airport pairs.

Example:

```text id="s11"
BOM → DEL = 1148 km
```

---

## Travel Class Emission Factors

Different classes use different factors:

```text id="s12"
Economy
Business
First
```

This reflects seat-space allocation methodology.

---

## Scope Classification

All travel activity is categorized as:

```text id="s13"
Scope 3
```

---

# What Would Break in Production

The current travel implementation does not support:

* international airport coverage
* OAuth2 Concur integration
* API pagination
* rail travel
* rental car categories
* hotel-specific emission factors
* employee-to-facility attribution

A production system would require:

* full travel APIs
* global airport datasets
* transport-mode categorization
* dynamic travel factors

---

# Why All Three Sources Use Similar Ingestion Architecture

Even though the data originates from different systems, all three ingestion pipelines follow the same high-level structure:

```text id="s14"
Upload
   ↓

Raw Record Storage
   ↓

Validation
   ↓

Normalization
   ↓

EmissionRecord Creation
   ↓

Analyst Review Workflow
```

This keeps the platform:

* consistent
* auditable
* maintainable
* extensible

---

# Common Challenges Across All Sources

The same enterprise ingestion problems appear across all datasets:

* inconsistent file formats
* missing fields
* invalid units
* malformed dates
* corrupted values
* non-standard headers

The platform was intentionally designed to tolerate imperfect enterprise data instead of assuming perfectly structured uploads.

---

# Final Design Philosophy

The platform prioritizes:

* auditability
* explainability
* resilience to bad data
* normalized reporting
* analyst review workflows

over:

* real-time integrations
* enterprise-scale infrastructure
* complex API ecosystems

The prototype demonstrates how messy enterprise operational data can be transformed into standardized ESG emission records suitable for reporting and review.
