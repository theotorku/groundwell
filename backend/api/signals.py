"""Signals API endpoints"""

from fastapi import APIRouter, HTTPException, Query
from typing import Optional

from backend.db.config import Database

router = APIRouter(prefix="/api/signals", tags=["signals"])


@router.get("/breakdown")
async def get_signals_breakdown(
    site_id: Optional[str] = Query(None, description="Filter by site"),
    signal_type: Optional[str] = Query(None, description="Filter by signal type"),
    severity: Optional[str] = Query(None, description="Filter by severity"),
    resolved: Optional[bool] = Query(None, description="Filter by resolution status")
):
    """
    Get aggregated breakdown of execution signals
    
    Args:
        site_id: Optional site filter
        signal_type: Optional signal type filter
        severity: Optional severity filter
        resolved: Optional resolution status filter
        
    Returns:
        Aggregated signal statistics
    """
    try:
        db = Database.get_client()
        
        # Build query
        query = db.table("execution_signals").select("*")
        
        if site_id:
            query = query.eq("site_id", site_id)
        if signal_type:
            query = query.eq("signal_type", signal_type)
        if severity:
            query = query.eq("severity", severity)
        if resolved is not None:
            query = query.eq("resolved", resolved)
        
        result = query.execute()
        signals = result.data
        
        # Aggregate statistics
        breakdown_by_type = {}
        breakdown_by_severity = {}
        by_site = {}
        
        for signal in signals:
            # By type
            sig_type = signal["signal_type"]
            breakdown_by_type[sig_type] = breakdown_by_type.get(sig_type, 0) + 1
            
            # By severity
            sev = signal["severity"]
            breakdown_by_severity[sev] = breakdown_by_severity.get(sev, 0) + 1
            
            # By site
            sid = signal["site_id"]
            by_site[sid] = by_site.get(sid, 0) + 1
        
        # Top sites with most signals
        top_sites = sorted(by_site.items(), key=lambda x: x[1], reverse=True)[:10]
        
        return {
            "total_signals": len(signals),
            "breakdown_by_type": breakdown_by_type,
            "breakdown_by_severity": breakdown_by_severity,
            "top_sites_by_signal_count": [
                {"site_id": site_id, "signal_count": count}
                for site_id, count in top_sites
            ],
            "filters_applied": {
                "site_id": site_id,
                "signal_type": signal_type,
                "severity": severity,
                "resolved": resolved
            }
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.patch("/{signal_id}/resolve")
async def resolve_signal(signal_id: str):
    """Mark a signal as resolved"""
    try:
        db = Database.get_client()
        
        from datetime import datetime
        
        result = db.table("execution_signals").update({
            "resolved": True,
            "resolved_date": datetime.utcnow().isoformat()
        }).eq("signal_id", signal_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Signal not found")
        
        return {
            "status": "success",
            "signal_id": signal_id
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
