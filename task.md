# Groundswell - Phase 0 Build Tasks

**Project:** Facilities & Property Services Execution Intelligence  
**Build Name:** Groundswell  
**Tagline:** "Execution intelligence from the ground up"  
**Objective:** Data credibility foundation for multi-site facilities management

---

## Phase 0: Foundation (Weeks 1-3)

### 🏗️ Repository & Environment Setup
- [x] Create repository structure (`/backend`, `/frontend`, `/shared`)
- [x] Set up Python environment with Pydantic AI, FastAPI
- [ ] Configure Supabase project (database + auth)
- [x] Set up React + Vite frontend template
- [x] Configure environment variables and secrets
- [x] Create Docker configuration for backend
- [x] Set up Railway deployment (backend)
- [x] Set up Vercel deployment (frontend)

### 📊 Core Domain Modeling
- [x] Define Pydantic models for facilities domain:
  - [x] `Site` model
  - [x] `Inspection` model
  - [x] `WorkOrder` model
  - [x] `Vendor` model
  - [x] `ExecutionSignal` model
  - [x] `RiskScore` model
- [x] Create database schema (PostgreSQL)
- [ ] Set up database migrations
- [x] Create schema versioning strategy

### 📥 Data Ingestion Layer
- [x] Build inspection note ingestion endpoint
- [x] Build work order status ingestion endpoint
- [x] Create CSV upload handler (for pilot historical data)
- [x] Implement data normalization pipeline
- [x] Add input validation and error handling

### 🤖 AI Execution Signal Extraction
- [x] Design prompts for facilities note structuring
- [x] Implement signal extraction logic:
  - [x] Missed inspections detector
  - [x] Late work orders detector
  - [x] Incomplete tasks detector
  - [x] Documentation gaps detector
- [x] Add confidence scoring to each signal
- [x] Persist extracted signals to database
- [x] Create extraction validation layer

### ⚠️ Site-Level Risk Scoring
- [x] Define risk scoring rules:
  - [x] Failure frequency calculation
  - [x] Severity weighting system
  - [x] Recency decay algorithm
- [x] Implement deterministic scoring engine
- [x] Generate site risk score snapshots
- [x] Store historical risk trends
- [x] Create explainability output (why a site is risky)

### 🔍 Query & Insight Layer
- [x] Create API endpoints:
  - [x] `/api/sites/at-risk` - List at-risk sites
  - [x] `/api/sites/{id}/history` - Site execution history
  - [x] `/api/signals/breakdown` - Signal breakdown by category
- [x] Add query filtering and pagination
- [ ] Implement natural-language query prototype (internal)

### 🎨 Minimal Frontend (Internal-Facing)
- [x] Set up React + Vite + Tailwind CSS + Shadcn
- [ ] Implement Supabase authentication
- [x] Create core views:
  - [x] At-risk sites list page
  - [x] Site detail page
  - [x] Signal timeline view
- [x] Add basic navigation and routing
- [x] Implement responsive layout

### ✅ Validation & Quality Controls
- [x] Set signal confidence thresholds
- [ ] Add manual override/correction support
- [ ] Implement logging for extraction failures
- [ ] Create sample data replay for debugging
- [ ] Add unit tests for critical paths

### 🚀 Pilot Readiness
- [x] Create seed demo data for facilities scenarios
- [/] Define pilot success metrics (signal accuracy, risk ranking, time-to-insight)
- [x] Write internal README for pilot operators
- [ ] Create demo walkthrough documentation
- [ ] Set up monitoring and logging

---

## Phase 0 Exit Criteria

Phase 0 is complete when the system can:

- ✅ Reliably extract facilities execution signals from raw notes
- ✅ Rank sites by execution risk with explainable logic
- ✅ Surface issues leadership did not previously see
- ✅ Support a paid pilot conversation

---

## Out of Scope (Phase 0)

- ❌ Vision AI / photo analysis
- ❌ Predictive maintenance models
- ❌ Workflow automation
- ❌ Third-party CMMS integrations
- ❌ Executive dashboards (beyond basic lists)
