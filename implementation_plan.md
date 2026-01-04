# Groundswell - Phase 0 Implementation Plan

**Project:** Facilities & Property Services Execution Intelligence  
**Build Name:** Groundswell  
**Tagline:** "Execution intelligence from the ground up"  
**Timeline:** 3 weeks  
**Strategy:** Reuse-first, validate-fast

---

## Overview

Groundswell is an AI-powered execution intelligence platform for multi-site facilities management. Phase 0 focuses on establishing **data credibility** - the foundation that allows facilities leaders to trust execution insights extracted from unstructured operational data.

This build leverages the proven BeautyOps AI architecture and adapts it for the facilities domain, minimizing greenfield development while validating the horizontal execution intelligence thesis.

---

## User Review Required

> [!IMPORTANT]
> **Technology Stack Alignment**
> 
> This implementation uses the following stack to maximize reuse from BeautyOps AI:
> - **Backend:** Python, Pydantic AI, FastAPI, PostgreSQL/Supabase
> - **Frontend:** React, Vite, Tailwind CSS, Shadcn UI
> - **AI:** OpenAI models for signal extraction and risk scoring
> - **Deployment:** Railway (backend), Vercel (frontend)
> 
> If you prefer different technologies or have existing BeautyOps code to fork from, please let me know.

> [!WARNING]
> **Phase 0 Scope Constraints**
> 
> This phase explicitly excludes:
> - Vision AI / photo analysis
> - Predictive maintenance ML models
> - Workflow automation engines
> - Third-party CMMS integrations
> - Executive dashboards beyond basic lists
> 
> These features are deferred to Phase 1+ to maintain focus on data credibility.

---

## Proposed Changes

### Backend Architecture

#### [NEW] [backend/main.py](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/backend/main.py)

FastAPI application entry point with:
- CORS configuration for Vercel frontend
- Authentication middleware (Supabase JWT)
- Health check endpoint
- API route registration

---

#### [NEW] [backend/models/](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/backend/models/)

Core Pydantic domain models adapted from BeautyOps:

**Site Model:**
```python
class Site(BaseModel):
    site_id: str
    name: str
    location: str
    site_type: str  # retail, healthcare, hospitality, commercial
    status: str  # active, inactive
    metadata: dict
```

**Inspection Model:**
```python
class Inspection(BaseModel):
    inspection_id: str
    site_id: str
    inspector_name: str
    inspection_date: datetime
    notes: str
    status: str  # completed, incomplete, missed
    confidence_score: float
```

**WorkOrder Model:**
```python
class WorkOrder(BaseModel):
    work_order_id: str
    site_id: str
    vendor_id: Optional[str]
    created_date: datetime
    due_date: datetime
    completed_date: Optional[datetime]
    status: str  # pending, in_progress, completed, late
    description: str
```

**ExecutionSignal Model:**
```python
class ExecutionSignal(BaseModel):
    signal_id: str
    site_id: str
    signal_type: str  # missed_inspection, late_work_order, incomplete_task, doc_gap
    severity: str  # low, medium, high, critical
    detected_date: datetime
    confidence_score: float
    evidence: dict
    explanation: str
```

**RiskScore Model:**
```python
class RiskScore(BaseModel):
    risk_score_id: str
    site_id: str
    score: float  # 0-100
    calculated_date: datetime
    contributing_signals: list[str]
    explanation: str
    trend: str  # improving, stable, deteriorating
```

---

#### [NEW] [backend/agents/](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/backend/agents/)

Pydantic AI agents for execution intelligence:

**Signal Extraction Agent:**
- Analyzes inspection notes and work orders
- Extracts execution signals with confidence scores
- Categorizes signals by type and severity

**Risk Scoring Agent:**
- Aggregates signals per site
- Applies deterministic scoring rules
- Generates explainable risk assessments

---

#### [NEW] [backend/api/](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/backend/api/)

API endpoints:

**`POST /api/inspections/ingest`**
- Accepts raw inspection notes (text or CSV)
- Normalizes data into canonical format
- Triggers signal extraction agent
- Returns processing status

**`POST /api/work-orders/ingest`**
- Accepts work order data
- Detects SLA breaches and delays
- Persists to database

**`GET /api/sites/at-risk`**
- Returns ranked list of sites by risk score
- Supports filtering and pagination
- Includes trend indicators

**`GET /api/sites/{site_id}/history`**
- Returns execution signal timeline for a site
- Shows risk score evolution
- Provides explainability data

**`GET /api/signals/breakdown`**
- Aggregates signals by type, severity, date range
- Returns summary statistics

---

#### [NEW] [backend/db/](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/backend/db/)

Database layer:

**PostgreSQL Schema:**
- `sites` table
- `inspections` table
- `work_orders` table
- `vendors` table
- `execution_signals` table
- `risk_scores` table

**Migrations:**
- Alembic or Supabase migrations
- Schema versioning

---

### Frontend Architecture

#### [NEW] [frontend/src/](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/frontend/src/)

React application with minimal, internal-facing UI:

**Pages:**
1. **At-Risk Sites Dashboard** (`/dashboard`)
   - Ranked list of sites by risk score
   - Color-coded severity indicators
   - Quick filters (region, site type, risk level)

2. **Site Detail Page** (`/sites/{site_id}`)
   - Site metadata
   - Current risk score with explainability
   - Signal timeline (chronological list)
   - Trend chart (simple line chart)

3. **Authentication** (`/login`)
   - Supabase Auth UI
   - Email/password login

**Components:**
- `SiteCard` - Displays site risk summary
- `SignalTimeline` - Chronological signal list
- `RiskBadge` - Color-coded risk indicator
- `ExplainabilityPanel` - Shows why a site is risky

**Styling:**
- Tailwind CSS for utility-first styling
- Shadcn UI for pre-built components
- Dark mode support (facilities command center aesthetic)

---

### Shared Layer

#### [NEW] [shared/prompts/](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/shared/prompts/)

AI prompt templates for signal extraction:

**Inspection Note Structuring Prompt:**
```
Analyze the following facilities inspection note and extract execution signals.

Inspection Note: {note}

Identify:
1. Missed inspections or delayed visits
2. Incomplete tasks or documentation gaps
3. Safety or compliance issues
4. Vendor performance problems

For each signal, provide:
- Type (missed_inspection, incomplete_task, doc_gap, safety_issue)
- Severity (low, medium, high, critical)
- Confidence (0.0-1.0)
- Evidence (quoted from note)
- Explanation (why this is a problem)
```

---

### Infrastructure

#### [NEW] [Dockerfile](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/Dockerfile)

Multi-stage build for backend:
- Python 3.11+ base image
- Install dependencies with `uv`
- Run FastAPI with Uvicorn

#### [NEW] [railway.json](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/railway.json)

Railway deployment configuration:
- Backend service definition
- Environment variable mappings
- Health check endpoint

#### [NEW] [vercel.json](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/vercel.json)

Vercel deployment configuration:
- SPA routing rules
- Environment variable injection

---

## Verification Plan

### Automated Tests

**Backend Tests:**
```bash
pytest backend/tests/
```

Test coverage:
- Signal extraction accuracy (using fixtures)
- Risk scoring determinism
- API endpoint responses
- Database operations

**Frontend Tests:**
```bash
npm run test
```

Test coverage:
- Component rendering
- Authentication flow
- API integration

---

### Manual Verification

1. **Signal Extraction Validation**
   - Upload sample inspection notes
   - Verify extracted signals match expected outputs
   - Check confidence scores are reasonable

2. **Risk Scoring Validation**
   - Create sites with known signal patterns
   - Verify risk scores rank correctly
   - Validate explainability outputs

3. **End-to-End Flow**
   - Log in as pilot user
   - Upload inspection data
   - View at-risk sites list
   - Drill into site details
   - Confirm signals and risk scores display correctly

4. **Pilot Demo**
   - Seed database with realistic facilities data
   - Walk through key user flows
   - Demonstrate value proposition (unseen issues surfaced)

---

## Seed Data Strategy

Create 3 demo scenarios representing common facilities patterns:

**Scenario 1: "The Neglected Region"**
- 20 sites with inconsistent inspections
- Multiple missed visits
- Rising risk scores over time

**Scenario 2: "Vendor Performance Issues"**
- Sites with repeat work orders from same vendor
- SLA breaches
- Documentation gaps

**Scenario 3: "Well-Managed Portfolio"**
- Sites with consistent execution
- Low risk scores
- Control group for comparison

---

## Success Metrics (Pilot)

**Quantitative:**
- Signal extraction accuracy > 85%
- Risk ranking precision (top 10 sites)
- API response time < 500ms

**Qualitative:**
- Pilot users identify previously unseen issues
- Explainability is understandable
- System surfaces actionable insights

---

## Timeline & Milestones

### Week 1: Foundation
- [ ] Repository setup
- [ ] Domain models defined
- [ ] Database schema created
- [ ] Basic API endpoints functional

### Week 2: Intelligence
- [ ] Signal extraction working
- [ ] Risk scoring implemented
- [ ] Seed data created
- [ ] Backend deployed to Railway

### Week 3: UI & Polish
- [ ] Frontend pages built
- [ ] Authentication working
- [ ] End-to-end flow validated
- [ ] Pilot demo ready

---

## Risk Mitigation

| Risk | Mitigation |
|------|------------|
| Signal extraction accuracy issues | Start with rule-based extraction, iterate prompts, add human-in-loop validation |
| Risk scoring doesn't match user intuition | Make scoring rules configurable, provide override mechanism |
| Integration complexity | Keep Phase 0 standalone (CSV uploads), defer CMMS integrations |
| Scope creep | Strict adherence to Phase 0 feature list, track requests for Phase 1 |

---

## Next Steps After Approval

1. Create repository structure
2. Set up Python backend with FastAPI + Pydantic AI
3. Define domain models and database schema
4. Build signal extraction agent
5. Implement risk scoring engine
6. Create minimal frontend
7. Deploy to Railway + Vercel
8. Seed demo data and validate

---

**Ready to build?** Approve this plan and I'll begin implementation immediately. 🚀
