"""Work Orders API endpoints"""

from fastapi import APIRouter, HTTPException
from datetime import datetime
import uuid

from backend.models import WorkOrder
from backend.agents import SignalExtractorAgent
from backend.db.config import Database

router = APIRouter(prefix="/api/work-orders", tags=["work_orders"])

# Initialize signal extractor
signal_extractor = SignalExtractorAgent()


@router.post("/ingest")
async def ingest_work_order(work_order: WorkOrder):
    """
    Ingest a work order and extract execution signals
    
    Args:
        work_order: WorkOrder data
        
    Returns:
        Processing status and extracted signals
    """
    try:
        db = Database.get_client()
        
        # Store work order
        db.table("work_orders").insert(work_order.model_dump(mode="json")).execute()
        
        # Extract signals (late work orders, etc.)
        signals = await signal_extractor.extract_from_work_order(
            work_order_id=work_order.work_order_id,
            site_id=work_order.site_id,
            description=work_order.description,
            created_date=work_order.created_date,
            due_date=work_order.due_date,
            status=work_order.status
        )
        
        # Store signals
        if signals:
            signals_data = [s.model_dump(mode="json") for s in signals]
            db.table("execution_signals").insert(signals_data).execute()
        
        return {
            "status": "success",
            "work_order_id": work_order.work_order_id,
            "signals_extracted": len(signals),
            "signals": [
                {
                    "signal_id": s.signal_id,
                    "type": s.signal_type,
                    "severity": s.severity
                }
                for s in signals
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{work_order_id}")
async def get_work_order(work_order_id: str):
    """Get work order by ID"""
    try:
        db = Database.get_client()
        result = db.table("work_orders").select("*").eq("work_order_id", work_order_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Work order not found")
        
        return result.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/site/{site_id}")
async def get_site_work_orders(site_id: str, status: str = None):
    """Get all work orders for a site, optionally filtered by status"""
    try:
        db = Database.get_client()
        query = db.table("work_orders").select("*").eq("site_id", site_id)
        
        if status:
            query = query.eq("status", status)
        
        result = query.order("created_date", desc=True).execute()
        
        return {
            "site_id": site_id,
            "work_orders": result.data,
            "count": len(result.data)
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
