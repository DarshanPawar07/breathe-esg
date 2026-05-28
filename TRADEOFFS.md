# TRADEOFFS.md — Things Deliberately Not Built

Three significant features were deliberately excluded from this prototype. Each decision was made consciously to keep the project focused on the core problem: ingestion, normalization, and analyst review workflow.

---

## Tradeoff 1: No Real Concur API Integration (Travel is CSV)

**What was not built:**
A live OAuth2 integration with the Concur Travel REST API that would automatically pull travel records without any file upload.

**What was built instead:**
CSV file upload for travel data, same mechanism as SAP and Utility.

**Why this tradeoff was made:**
I spent approximately 2 days attempting to implement a mock Concur API approach. After encountering persistent technical issues that I could not resolve within the 4-day project timeline, I made a pragmatic decision to switch to CSV.

Concur and Navan both support CSV exports for companies that have not configured programmatic API access. For a new enterprise client onboarding scenario — which is exactly the context described in the assignment — CSV export is actually the more realistic starting point. IT teams at large enterprises take weeks to approve and configure OAuth2 credentials for third-party platforms.

**What is lost:**
- Automated data pull without analyst involvement
- Real-time or scheduled ingestion
- Demonstration of API-based ingestion as a distinct mechanism

**What would be needed to build it properly:**
Concur OAuth2 token management, paginated API calls (Concur returns 100 records per page), background job queue (Celery) to handle long-running pulls without blocking the HTTP request, and error handling for API rate limits and token expiry.

**Why it is still defensible:**
The ingestion logic — parsing travel types, calculating distances from airport codes, applying emission factors by class — is identical whether data arrives via CSV or API. The core domain logic is demonstrated. Only the data reading mechanism differs.

---

## Tradeoff 2: No PDF Utility Bill Parsing

**What was not built:**
A parser that accepts utility bills as PDF files and extracts consumption data automatically.

**What was built instead:**
CSV portal export ingestion only.

**Why this tradeoff was made:**
PDF parsing for utility bills is a deceptively complex problem. Utility bill PDFs have no standard layout — every provider (MSEDCL, Tata Power, BESCOM, KSEB) formats their bills differently. Libraries like pdfplumber, camelot, and tabula can extract tables from structured PDFs but fail on scanned PDFs (which require OCR) and on bills where consumption data is embedded in unstructured text paragraphs.

Building a reliable PDF parser would require:
- Layout detection to identify the consumption table on each bill
- Provider-specific parsing rules for each utility company
- OCR pipeline for scanned bills
- Validation that extracted values are plausible

This represents weeks of engineering work and significant ongoing maintenance as providers change their bill formats. The CSV portal export covers 80% of real cases — most utility portals that facilities teams use daily have a "download usage history" button that produces a structured CSV.

**What is lost:**
- Support for clients who only have PDF bills and no portal access
- Support for historical data that only exists as scanned bills

**What would be needed to build it properly:**
AWS Textract or Google Document AI for OCR, provider-specific extraction rules maintained as configuration, human-in-the-loop review for low-confidence extractions.

---

## Tradeoff 3: No Emissions Reporting Dashboard

**What was not built:**
Charts, trend analysis, year-over-year comparison, Scope breakdown pie charts, facility comparison bar charts, and export to PDF/Excel for board reporting.

**What was built instead:**
An analyst review dashboard focused on row-level review and approval workflow.

**Why this tradeoff was made:**
The assignment asks for a system where analysts can "see what came in, what failed, what looks suspicious, and approve rows before they're locked for audit." This is an operational data quality workflow, not a reporting product.

Building a reporting dashboard would require:
- All rows to be approved and locked first (the data is not ready for reporting until review is complete)
- Aggregation queries across date ranges, scopes, and facilities
- Chart library integration (Chart.js, Recharts, D3)
- Export functionality (PDF generation, Excel export)
- Handling of partial periods (what if only some months have been ingested?)

This is a separate product feature that sits downstream of what the assignment describes. Adding it would expand scope significantly and risk making the core ingestion and review workflow less polished.

**What is lost:**
- Visual emissions summary for management reporting
- Scope 1/2/3 breakdown charts
- Facility-level emissions comparison
- Trend analysis over time

**What would be needed to build it properly:**
A separate reporting layer with pre-aggregated materialized views for performance, configurable date ranges and groupings, and a chart library with export capability. This would typically be a separate sprint after the ingestion and review workflow is stable and trusted.

**Why the boundary was drawn here:**
The assignment specifically says the analyst reviews and signs off "before it goes to auditors." The product ends at the locked row — what auditors and management do with that data downstream is out of scope for this prototype.
