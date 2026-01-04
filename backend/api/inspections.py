"""Inspections API endpoints"""

from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Optional
import csv
import io
import uuid

from backend.models import Inspection
from backend.agents import SignalExtractorAgent
from backend.db.config import Database

router = APIRouter(prefix="/api/inspections", tags=["inspections"])

# Initialize signal extractor
signal_extractor = SignalExtractorAgent()


@router.post("/ingest")
async def ingest_inspection(inspection: Inspection):
    """
    Ingest a single inspection and extract execution signals
    
    Args:
        inspection: Inspection data
        
    Returns:
        Processing status and extracted signals
    """
    try:
        db = Database.get_client()
        
        # Store inspection
        db.table("inspections").insert(inspection.model_dump(mode="json")).execute()
        
        # Extract signals using AI agent
        signals = await signal_extractor.extract_from_inspection(
            inspection_id=inspection.inspection_id,
            site_id=inspection.site_id,
            notes=inspection.notes
        )
        
        # Store signals
        if signals:
            signals_data = [s.model_dump(mode="json") for s in signals]
            db.table("execution_signals").insert(signals_data).execute()
        
        return {
            "status": "success",
            "inspection_id": inspection.inspection_id,
            "signals_extracted": len(signals),
            "signals": [
                {
                    "signal_id": s.signal_id,
                    "type": s.signal_type,
                    "severity": s.severity,
                    "confidence": s.confidence_score
                }
                for s in signals
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/ingest/csv")
async def ingest_inspections_csv(file: UploadFile = File(...)):
    """
    Ingest multiple inspections from CSV file
    
    CSV Format:
    site_id, inspector_name, inspection_date, notes, status, inspection_type
    
    Returns:
        Processing summary
    """
    try:
        contents = await file.read()
        csv_text = contents.decode("utf-8")
        csv_reader = csv.DictReader(io.StringIO(csv_text))
        
        db = Database.get_client()
        total_processed = 0
        total_signals = 0
        
        for row in csv_reader:
            # Create inspection object
            inspection = Inspection(
                inspection_id=str(uuid.uuid4()),
                site_id=row["site_id"],
                inspector_name=row["inspector_name"],
                inspection_date=row["inspection_date"],
                notes=row["notes"],
                status=row["status"],
                inspection_type=row.get("inspection_type")
            )
            
            # Store inspection
            db.table("inspections").insert(inspection.model_dump(mode="json")).execute()
            
            # Extract signals
            signals = await signal_extractor.extract_from_inspection(
                inspection_id=inspection.inspection_id,
                site_id=inspection.site_id,
                notes=inspection.notes
            )
            
            # Store signals
            if signals:
                signals_data = [s.model_dump(mode="json") for s in signals]
                db.table("execution_signals").insert(signals_data).execute()
                total_signals += len(signals)
            
            total_processed += 1
        
        return {
            "status": "success",
            "inspections_processed": total_processed,
            "total_signals_extracted": total_signals
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{inspection_id}")
async def get_inspection(inspection_id: str):
    """Get inspection by ID"""
    try:
        db = Database.get_client()
        result = db.table("inspections").select("*").eq("inspection_id", inspection_id).execute()
        
        if not result.data:
            raise HTTPException(status_code=404, detail="Inspection not found")
        
        return result.data[0]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
