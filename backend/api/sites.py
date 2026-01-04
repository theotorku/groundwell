"""Sites API endpoints"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from backend.models import Site, RiskScore
from backend.agents import RiskScorerAgent
from backend.db.config import Database

router = APIRouter(prefix="/api/sites", tags=["sites"])

# Initialize risk scorer
risk_scorer = RiskScorerAgent()


@router.post("/")
async def create_site(site: Site):
    """Create a new site"""
    try:
        db = Database.get_client()
        db.table("sites").insert(site.model_dump(mode="json")).execute()
        
        return {
            "status": "success",
            "site_id": site.site_id
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{site_id}")
async def get_site(site_id: str):
    """Get site by ID with current risk score"""
    try:
        db = Database.get_client()
        
        # Get site
        site_result = db.table("sites").select("*").eq("site_id", site_id).execute()
        
        if not site_result.data:
            raise HTTPException(status_code=404, detail="Site not found")
        
        site = site_result.data[0]
        
        # Get latest risk score
        risk_result = db.table("risk_scores").select("*").eq("site_id", site_id).order("calculated_date", desc=True).limit(1).execute()
        
        site["current_risk_score"] = risk_result.data[0] if risk_result.data else None
        
        return site
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{site_id}/history")
async def get_site_history(site_id: str):
    """Get execution signal timeline for a site"""
    try:
        db = Database.get_client()
        
        # Get site
        site_result = db.table("sites").select("*").eq("site_id", site_id).execute()
        
        if not site_result.data:
            raise HTTPException(status_code=404, detail="Site not found")
        
        # Get signals (ordered by date, most recent first)
        signals_result = db.table("execution_signals").select("*").eq("site_id", site_id).order("detected_date", desc=True).execute()
        
        # Get risk score history
        risk_result = db.table("risk_scores").select("*").eq("site_id", site_id).order("calculated_date", desc=True).execute()
        
        return {
            "site": site_result.data[0],
            "signals": signals_result.data,
            "risk_history": risk_result.data
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/at-risk")
async def get_at_risk_sites(
    min_score: float = Query(default=50.0, description="Minimum risk score"),
    limit: int = Query(default=50, le=100)
):
    """
    Get ranked list of at-risk sites
    
    Args:
        min_score: Minimum risk score threshold
        limit: Maximum number of sites to return
        
    Returns:
        Ranked list of sites by risk score
    """
    try:
        db = Database.get_client()
        
        # Get latest risk scores for all sites above threshold
        risk_result = db.table("risk_scores").select("*").gte("score", min_score).order("calculated_date", desc=True).execute()
        
        # Group by site (keep only latest score per site)
        site_scores = {}
        for score in risk_result.data:
            site_id = score["site_id"]
            if site_id not in site_scores:
                site_scores[site_id] = score
        
        # Get site details
        sites_with_scores = []
        for site_id, score in site_scores.items():
            site_result = db.table("sites").select("*").eq("site_id", site_id).execute()
            if site_result.data:
                site = site_result.data[0]
                site["risk_score"] = score
                sites_with_scores.append(site)
        
        # Sort by risk score (highest first)
        sites_with_scores.sort(key=lambda x: x["risk_score"]["score"], reverse=True)
        
        return {
            "sites": sites_with_scores[:limit],
            "count": len(sites_with_scores),
            "min_score_threshold": min_score
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
