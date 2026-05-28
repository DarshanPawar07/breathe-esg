# Breathe ESG — Emissions Management Platform

A full-stack ESG emissions intelligence platform built for enterprise sustainability analysts. The platform ingests operational emissions data from SAP exports, utility provider reports, and corporate travel records, normalizes the data into a common emissions schema, and provides an analyst review workflow before final reporting and audit review.

---

# Live Deployment

## Frontend

https://breathe-esg-swart.vercel.app/

## Backend API

https://breathe-esg-production-edc7.up.railway.app/api

---

# Production Deployment Stack

| Service        | Platform   |
| -------------- | ---------- |
| Frontend       | Vercel     |
| Backend        | Railway    |
| Database       | PostgreSQL |
| Static Hosting | WhiteNoise |

---

# Production Features

* Full-stack cloud deployment
* PostgreSQL production database
* REST API architecture
* File upload pipelines
* Production-ready React frontend
* Railway cloud backend hosting
* Vercel frontend deployment
* Responsive dashboard UI
* Upload history tracking
* ESG emissions normalization pipeline

---

# Overview

Enterprise sustainability teams receive emissions-related operational data from multiple disconnected systems:

* **SAP exports** — operational procurement and fuel consumption data
* **Utility provider reports** — electricity consumption and billing data
* **Corporate travel records** — flights, hotels, and ground transport

Each source produces data in a different format, with different units, inconsistent naming conventions, and varying levels of data quality.

This platform standardizes those inputs into a unified emissions model (`EmissionRecord`) using ingestion pipelines, normalization rules, validation logic, and emission factor calculations.

---

# Features

* Multi-source ingestion pipeline

  * SAP CSV ingestion
  * Utility CSV ingestion
  * Travel CSV ingestion

* Two-layer architecture

  * Raw ingestion tables preserve uploaded source data
  * Normalized `EmissionRecord` table powers analytics and review workflows

* Validation engine with three-tier classification

  * `clean`
  * `suspicious`
  * `failed`

* Emissions normalization

  * Unit standardization
  * Scope classification
  * CO₂e calculation using DEFRA-style emission factors

* Analyst review workflow

  * Pending review
  * Approved rows
  * Flagged rows

* Facility-level emissions tracking

* Tenant-scoped data separation at the application layer

* Source traceability

  * Every normalized record points back to the original source row

---

# Tech Stack

| Layer            | Technology                              |
| ---------------- | --------------------------------------- |
| Backend          | Django 5                                |
| API              | Django REST Framework                   |
| Frontend         | React + Vite                            |
| Database         | PostgreSQL + SQLite (local development) |
| Data Processing  | Pandas                                  |
| HTTP Client      | Axios                                   |
| Frontend Hosting | Vercel                                  |
| Backend Hosting  | Railway                                 |

---

# Architecture

The platform uses a two-layer ingestion architecture.

## Layer 1 — Raw Ingestion Tables

Each source stores uploaded rows exactly as received:

* `SAPRecord`
* `UtilityRecord`
* `TravelRecord`

These tables preserve:

* raw uploaded values
* parsing results
* validation status
* ingestion errors
* source traceability

This layer exists for:

* debugging
* auditability
* reprocessing
* analyst verification

---

## Layer 2 — Normalized Emissions Layer

All clean rows are transformed into:

* `EmissionRecord`

This table contains:

* normalized quantities
* standardized units
* scope classification
* emission factors
* CO₂e calculations
* review workflow metadata

---

# Scope Classification

The system assigns emission scopes during ingestion:

| Source                      | Scope   |
| --------------------------- | ------- |
| SAP fuel records            | Scope 1 |
| Utility electricity records | Scope 2 |
| Travel records              | Scope 3 |

---

# Project Structure

```text
breatheesg/
│
├── README.md
├── MODEL.md
├── DECISIONS.md
├── TRADEOFFS.md
├── SOURCES.md
│
├── manage.py
├── requirements.txt
│
├── breatheesg/
│   ├── settings.py
│   └── urls.py
│
├── core/
│   ├── models.py
│   ├── views.py
│   ├── serializers.py
│   ├── urls.py
│   ├── constants.py
│   │
│   ├── services/
│   │   └── ingestion/
│   │       ├── sap.py
│   │       ├── utility.py
│   │       └── travel.py
│   │
│   └── sample_data/
│       ├── sap_export.csv
│       ├── utility_export.csv
│       └── travel_export.csv
│
└── frontend/
    └── src/
        ├── pages/
        ├── components/
        ├── api/
        └── styles/
```

---

# Running Locally

## Prerequisites

* Python 3.11+
* Node.js 18+

---

# Backend Setup

```bash
git clone <repository-url>
cd breatheesg

pip install -r requirements.txt

python manage.py migrate
```

Create sample tenant and facility data:

```bash
python manage.py shell
```

```python
from core.models import Tenant, Facility

tenant = Tenant.objects.create(
    name="Tata Motors"
)

Facility.objects.create(
    tenant=tenant,
    facility_code="MU01",
    facility_name="Mumbai Plant",
    facility_type="manufacturing",
    city="Mumbai",
    country="India"
)

Facility.objects.create(
    tenant=tenant,
    facility_code="PU02",
    facility_name="Pune Assembly",
    facility_type="manufacturing",
    city="Pune",
    country="India"
)

print("Sample data created")
```

Start backend server:

```bash
python manage.py runserver
```

Backend (Local):

```text
http://localhost:8000
```

---

# Frontend Setup

```bash
cd frontend

npm install

npm run dev
```

Frontend (Local):

```text
http://localhost:5173
```

Frontend (Production):

```text
https://breathe-esg-swart.vercel.app/
```

---

# Testing the Application

Sample CSV files are included in:

```text
core/sample_data/
```

## SAP Upload

Upload:

```text
sap_export.csv
```

The ingestion layer handles:

* German decimal notation
* SAP-style headers
* plant codes
* quantity normalization
* suspicious quantity detection

---

## Utility Upload

Upload:

```text
utility_export.csv
```

The ingestion layer handles:

* mixed electricity units
* billing periods
* unit normalization
* suspicious consumption values

---

## Travel Upload

Upload:

```text
travel_export.csv
```

The ingestion layer handles:

* flights
* hotels
* ground transport
* airport distance lookup
* travel-class-based emission factors

---

# API Endpoints

```text
GET   /api/emission-records/

POST  /api/upload/sap/
POST  /api/upload/utility/
POST  /api/upload/travel/

GET   /api/upload-history/
GET   /api/dashboard/
```

---

# Data Model

| Table          | Purpose                    |
| -------------- | -------------------------- |
| Tenant         | Client company             |
| Facility       | Plant / office / warehouse |
| SAPRecord      | Raw SAP ingestion rows     |
| UtilityRecord  | Raw utility ingestion rows |
| TravelRecord   | Raw travel ingestion rows  |
| EmissionRecord | Normalized emissions layer |

See `MODEL.md` for complete schema documentation.

---

# Important Design Decisions

## Why Raw Tables + EmissionRecord?

Direct normalization destroys auditability.

The system preserves:

* original uploaded rows
* parsed values
* validation results
* normalization decisions

Every `EmissionRecord` points back to its original source row.

---

## Why CSV Instead of Direct APIs?

CSV ingestion reflects realistic enterprise onboarding scenarios.

Most enterprise sustainability teams initially exchange operational data using exports from:

* SAP reports
* utility portals
* travel systems

A full API integration layer would require:

* OAuth flows
* credential management
* background jobs
* API rate-limit handling
* enterprise security approvals

The ingestion and normalization logic remains identical regardless of whether data arrives via CSV or API.

---

## Why SQLite + PostgreSQL?

SQLite was used during local development for simplicity and portability.

Production deployment uses PostgreSQL hosted on Railway for improved scalability and production-grade persistence.

---

# Limitations

* No authentication layer
* No RBAC / user permissions
* No PDF utility bill parsing
* No asynchronous ingestion queue
* Emission factors are hardcoded
* Limited airport lookup coverage

See `TRADEOFFS.md` for full details.

---

# Deployment

## Frontend Deployment

Frontend is deployed on Vercel:

https://breathe-esg-swart.vercel.app/

## Backend Deployment

Backend API is deployed on Railway:

https://breathe-esg-production-edc7.up.railway.app/api

## Production Database

Production database uses PostgreSQL hosted on Railway.

## Environment Variables

### Backend

```env
SECRET_KEY=<secret>
DEBUG=False
```

### Frontend

```env
VITE_API_BASE_URL=https://breathe-esg-production-edc7.up.railway.app/api
```

---

# Submission

Built for the Breathe ESG technical assessment.
