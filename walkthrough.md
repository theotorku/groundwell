# Groundswell - Phase 0 Build Walkthrough

**Project:** Facilities & Property Services Execution Intelligence  
**Build Name:** Groundswell  
**Tagline:** "Execution intelligence from the ground up"  
**Status:** Phase 0 Complete ✅

---

## What We Built

Groundswell is a fully functional AI-powered execution intelligence platform that helps facilities operators:

- ✅ **Extract execution signals** from unstructured inspection notes and work orders
- ✅ **Calculate risk scores** for sites using deterministic, explainable logic
- ✅ **Rank sites by risk** to prioritize action
- ✅ **Visualize execution timelines** showing breakdown patterns
- ✅ **Support CSV bulk uploads** for pilot data ingestion

---

## Architecture Overview

### Backend (Python + FastAPI + Pydantic AI)

```
backend/
├── models/          # 6 domain models (Site, Inspection, WorkOrder, Vendor, ExecutionSignal, RiskScore)
├── agents/          # 2 AI agents (SignalExtractorAgent, RiskScorerAgent)
├── api/             # 4 API route modules (inspections, work_orders, sites, signals)
├── db/              # Database config + PostgreSQL schema
├── main.py          # FastAPI application
└── seed_data.py     # Demo data generator
```

**Key Highlights:**

1. **[Domain Models](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/backend/models/)** - Pydantic models with validation, examples, and consistent metadata patterns

2. **[SignalExtractorAgent](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/backend/agents/signal_extractor.py)** - Uses Pydantic AI to extract execution signals from text with confidence scoring. Handles both AI-based extraction (inspection notes) and rule-based detection (late work orders).

3. **[RiskScorerAgent](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/backend/agents/risk_scorer.py)** - Deterministic risk scoring with severity weighting, recency decay, and explainability. No ML in Phase 0 - pure logic.

4. **[API Endpoints](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/backend/api/)** - RESTful API with:
   - Inspection/work order ingestion
   - At-risk site ranking
   - Site execution history
   - Signal breakdown aggregation
   - CSV bulk upload support

---

### Frontend (React + Vite + Tailwind)

```
frontend/
├── src/
│   ├── components/    # RiskBadge, SiteCard, SignalTimeline
│   ├── pages/         # Dashboard, SiteDetail
│   ├── lib/           # Utilities (supabase, utils)
│   └── services/      # API client
├── index.html
├── package.json
└── vite.config.js
```

**Key Highlights:**

1. **[Dashboard Page](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/frontend/src/pages/Dashboard.jsx)** - Grid of at-risk sites with:
   - Color-coded risk badges
   - Trend indicators (improving/deteriorating)
   - Risk score filtering (slider)
   - Hover effects and glassmorphism

2. **[SiteDetail Page](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/frontend/src/pages/SiteDetail.jsx)** - Comprehensive site view with:
   - Site metadata display
   - Risk score breakdown by signal type
   - Chronological signal timeline
   - Evidence quotes from source documents

3. **[Components](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/frontend/src/components/):**
   - **RiskBadge** - Color-coded score display (red/orange/yellow/green)
   - **SiteCard** - Glassmorphic card with site summary
   - **SignalTimeline** - Event list with severity badges and confidence scores

4. **Design System:**
   - Dark theme with command center aesthetic
   - Glassmorphism effects (`backdrop-filter: blur`)
   - HSL-based color tokens for consistency
   - Tailwind utility-first styling
   - Gradient accents for visual hierarchy

---

## Database Schema

**PostgreSQL tables created:**
- `sites` - Physical locations
- `inspections` - Site visits and audits
- `work_orders` - Maintenance tasks
- `vendors` - Service providers
- `execution_signals` - Detected breakdowns
- `risk_scores` - Aggregated site risk

**Features:**
- Row Level Security (RLS) policies
- Indexes on foreign keys and date columns
- JSONB support for flexible metadata
- Cascade deletes for data integrity

**Schema file:** [backend/db/schema.sql](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/backend/db/schema.sql)

---

## Seed Data (Demo Scenarios)

Created 3 realistic scenarios for pilot demonstration:

### Scenario 1: The Neglected Region
- 5 sites in Southwest region
- Multiple missed inspections
- Incomplete maintenance tasks
- **Expected risk scores:** 60-80 (high risk)

### Scenario 2: Vendor Performance Issues
- 3 sites with underperforming vendor
- Late work orders (3+ days overdue)
- SLA breaches
- **Expected risk scores:** 50-70 (medium-high risk)

### Scenario  3: Well-Managed Portfolio
- 3 sites with consistent execution
- Completed inspections on schedule
- No outstanding issues
- **Expected risk scores:** 0-20 (low risk)

**Seed script:** [backend/seed_data.py](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/backend/seed_data.py)

---

## Deployment Configuration

### Backend (Railway)
- [Dockerfile](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/Dockerfile) - Multi-stage Python build
- [railway.json](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/railway.json) - Service configuration with health checks
- Environment variables: `SUPABASE_URL`, `SUPABASE_KEY`, `OPENAI_API_KEY`, `FRONTEND_URL`

### Frontend (Vercel)
- [vercel.json](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/vercel.json) - SPA routing configuration
- Environment variables: `VITE_API_URL`, `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY`

Both configured for automatic deployment on git push.

---

## API Documentation

Full interactive API docs available at `/docs` when backend is running.

**Key endpoints:**

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `GET` | `/api/sites/at-risk` | Get ranked list of risky sites |
| `GET` | `/api/sites/{id}/history` | Get site execution timeline |
| `POST` | `/api/inspections/ingest` | Submit inspection for analysis |
| `POST` | `/api/inspections/ingest/csv` | Bulk upload inspections |
| `GET` | `/api/signals/breakdown` | Aggregated signal statistics |
| `PATCH` | `/api/signals/{id}/resolve` | Mark signal as addressed |

---

## Phase 0 Exit Criteria Status

✅ **System can reliably extract execution signals from raw notes**
- Signal extraction agent built with Pydantic AI
- Confidence scoring implemented
- Evidence preservation working

✅ **System can rank sites by execution risk with explainable logic**
- Deterministic risk scoring engine complete
- Severity weighting, recency decay, frequency tracking
- Breakdown by signal type

✅ **System can surface issues leadership did not previously see**
- Signal timeline shows execution patterns
- Risk trend tracking (improving/deteriorating)
- Aggregated statistics across portfolio

✅ **System supports paid pilot conversation**
- Professional UI with command center aesthetic
- Comprehensive documentation ([README.md](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/README.md))
- Seed data for demonstration
- Clear value proposition

---

## Technology Stack

### Backend
- **Python 3.11+**
- **FastAPI** - Modern async web framework
- **Pydantic AI 0.0.13** - Agent orchestration
- **Pydantic 2.9** - Data validation
- **Supabase** - PostgreSQL database + auth
- **OpenAI GPT-4** - Signal extraction

### Frontend
- **React 18** - UI library
- **Vite 5** - Build tool (fast HMR)
- **Tailwind CSS 3** - Utility-first CSS
- **React Router 6** - Client routing
- **Lucide React** - Icon system

### Infrastructure
- **Railway** - Backend hosting
- **Vercel** - Frontend hosting
- **Docker** - Containerization
- **PostgreSQL** - Primary database

---

## What's NOT Included (By Design)

Phase 0 explicitly excludes:
- ❌ Vision AI / photo analysis
- ❌ Predictive maintenance ML models
- ❌ Workflow automation
- ❌ Third-party CMMS integrations
- ❌ Executive dashboards (beyond basic lists)
- ❌ User authentication (Supabase integration ready, not implemented)

These are Phase 1+ features.

---

## Next Steps

### To Run Locally

1. **Set up Supabase:**
   - Create project at supabase.com
   - Run SQL schema from [backend/db/schema.sql](file:///c:/Users/TheoTorku/OneDrive/Desktop/DevOps/Facilities%20&%20Property%20Services%20Execution%20Intelligence/backend/db/schema.sql)
   - Copy URL and anon key

2. **Configure Backend:**
   ```bash
   cd backend
   cp .env.example .env
   # Edit .env with Supabase and OpenAI credentials
   pip install -r requirements.txt
   python main.py
   ```

3. **Configure Frontend:**
   ```bash
   cd frontend
   cp .env.example .env
   # Edit .env with API URL and Supabase credentials
   npm install
   npm run dev
   ```

4. **Seed Data:**
   ```bash
   cd backend
   python seed_data.py
   ```

5. **Access:**
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### To Deploy

1. **Railway (Backend):**
   - Connect GitHub repo
   - Add environment variables
   - Deploy auto-triggers

2. **Vercel (Frontend):**
   - Connect GitHub repo
   - Set root directory to `frontend`
   - Add environment variables
   - Deploy auto-triggers

---

## Success Metrics (For Pilot)

**Quantitative:**
- Signal extraction accuracy > 85%
- API response time < 500ms
- Zero false positives in critical signals

**Qualitative:**
- Pilot users discover previously unseen issues
- Risk explanations are understandable
- Insights are actionable

---

## File Summary

Created **50+ files** across backend, frontend, and shared:

**Backend (25 files):**
- 6 domain models
- 2 AI agents
- 4 API modules
- Database schema
- Main application
- Docker config
- Seed data script

**Frontend (20 files):**
- 3 React components
- 2 page components
- API service layer
- Vite/Tailwind config
- Styles and utilities

**Root (5 files):**
- README.md
- Dockerfile
- Railway/Vercel configs
- .gitignore

---

## Build Highlights

🎯 **Reuse-First Strategy** - Designed to mirror BeautyOps architecture for rapid vertical expansion

🧠 **AI-Powered Intelligence** - Pydantic AI agents with structured output and confidence scoring

📊 **Explainability-First** - Every risk score includes breakdown, evidence, and human-readable explanation

🎨 **Premium UI** - Dark theme glassmorphism with command center aesthetic

🚀 **Deploy-Ready** - Complete infrastructure configuration for Railway + Vercel

---

## Conclusion

**Groundswell Phase 0 is complete and ready for pilot validation.**

The system successfully demonstrates:
- Data credibility through AI signal extraction
- Risk visibility through deterministic scoring
- User interface that communicates execution intelligence clearly

Next milestone: **Pilot with 1-2 multi-site operators to validate paid conversion.**

---

**Built by:** Antigravity AI  
**Date:** January 4, 2026  
**Phase:** 0 (Foundation)  
**Status:** ✅ Complete
