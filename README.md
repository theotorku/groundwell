# Groundswell

**Tagline:** Execution intelligence from the ground up

Facilities & Property Services Execution Intelligence platform for multi-site operators.

---

## Overview

Groundswell is an AI-powered execution intelligence platform that helps facilities and property services organizations:

- **Detect execution breakdowns** from unstructured operational data
- **Rank sites by risk** with explainable scoring
- **Surface hidden issues** before they become crises
- **Quantify cost and risk exposure** from execution failures

---

## Architecture

### Backend
- **Python 3.11+**
- **FastAPI** - REST API framework
- **Pydantic AI** - Agent orchestration and validation
- **PostgreSQL / Supabase** - Database and authentication
- **OpenAI GPT-4** - Signal extraction and intelligence

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Client-side routing

### Infrastructure
- **Railway** - Backend hosting
- **Vercel** - Frontend hosting
- **Docker** - Containerization

---

## Getting Started

### Prerequisites

- Python 3.11+
- Node.js 18+
- Supabase account
- OpenAI API key

### Backend Setup

```bash
# Navigate to project root
cd "Facilities & Property Services Execution Intelligence"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Set up environment variables
cp backend/.env.example backend/.env
# Edit backend/.env with your Supabase and OpenAI credentials

# Run the backend
cd backend
python main.py
```

Backend will be available at `http://localhost:8000`

### Database Setup

1. Create a Supabase project
2. Run the schema in `backend/db/schema.sql` in the Supabase SQL editor
3. Copy your Supabase URL and anon key to `backend/.env`

### Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Set up environment variables
cp .env.example .env
# Edit .env with your API URL and Supabase credentials

# Run the development server
npm run dev
```

Frontend will be available at `http://localhost:5173`

---

## API Endpoints

### Sites
- `GET /api/sites/at-risk` - Get ranked list of at-risk sites
- `GET /api/sites/{site_id}` - Get site details
- `GET /api/sites/{site_id}/history` - Get site execution history
- `POST /api/sites` - Create a new site

### Inspections
- `POST /api/inspections/ingest` - Ingest single inspection
- `POST /api/inspections/ingest/csv` - Bulk ingest from CSV
- `GET /api/inspections/{inspection_id}` - Get inspection details

### Work Orders
- `POST /api/work-orders/ingest` - Ingest work order
- `GET /api/work-orders/{work_order_id}` - Get work order details
- `GET /api/work-orders/site/{site_id}` - Get site work orders

### Signals
- `GET /api/signals/breakdown` - Get aggregated signal statistics
- `PATCH /api/signals/{signal_id}/resolve` - Mark signal as resolved

### Health
- `GET /health` - Health check endpoint

Full API documentation available at `http://localhost:8000/docs`

---

## Deployment

### Backend (Railway)

1. Create Railway project
2. Connect GitHub repository
3. Add environment variables:
   - `SUPABASE_URL`
   - `SUPABASE_KEY`
   - `OPENAI_API_KEY`
   - `FRONTEND_URL`
4. Deploy will trigger automatically

### Frontend (Vercel)

1. Create Vercel project
2. Connect GitHub repository
3. Set root directory to `frontend`
4. Add environment variables:
   - `VITE_API_URL`
   - `VITE_SUPABASE_URL`
   - `VITE_SUPABASE_ANON_KEY`
5. Deploy will trigger automatically

---

## Core Concepts

### Execution Signals

Groundswell detects the following execution signals:

- **missed_inspection** - Scheduled inspection didn't occur
- **late_work_order** - Work order past due without completion  
- **incomplete_task** - Required maintenance identified but not actioned
- **doc_gap** - Missing or incomplete documentation
- **sla_breach** - Vendor failed to meet SLA
- **safety_issue** - Safety or compliance violation

### Risk Scoring

Sites are scored 0-100 based on:
- **Severity** of signals (critical/high/medium/low)
- **Confidence** in signal detection
- **Recency** (newer signals weighted more heavily)
- **Frequency** of execution breakdowns

### Explainability

Every risk score includes:
- Contributing signal IDs
- Breakdown by signal type
- Human-readable explanation
- Trend indicator (improving/stable/deteriorating)

---

## Phase 0 Scope

✅ **In Scope:**
- Text-based signal extraction
- Deterministic risk scoring
- Site ranking and history
- Minimal dashboard UI
- CSV data ingestion

❌ **Out of Scope (Phase 1+):**
- Vision AI / photo analysis
- Predictive maintenance ML
- Workflow automation
- CMMS integrations
- Executive dashboards

---

## Project Structure

```
.
├── backend/
│   ├── agents/          # Pydantic AI agents
│   ├── api/             # FastAPI routes
│   ├── db/              # Database configuration
│   ├── models/          # Pydantic domain models
│   ├── main.py          # FastAPI application
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/  # React components
│   │   ├── pages/       # Page components
│   │   ├── lib/         # Utilities
│   │   └── services/    # API client
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── shared/
│   ├── prompts/         # AI prompt templates
│   └── schemas/         # Shared schemas
├── Dockerfile
├── railway.json
├── vercel.json
└── README.md
```

---

## Contributing

This is a Phase 0 pilot build. Feedback is welcome!

---

## License

Proprietary - All rights reserved

---

## Contact

**Groundswell** - Execution intelligence from the ground up

Built with ❤️ for facilities operators who deserve better visibility into execution performance.
