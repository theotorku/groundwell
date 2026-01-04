"""Inspection domain model"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Inspection(BaseModel):
    """Represents a site visit, audit, or checklist event"""
    
    inspection_id: str = Field(..., description="Unique inspection identifier")
    site_id: str = Field(..., description="Associated site ID")
    inspector_name: str = Field(..., description="Name of inspector")
    inspection_date: datetime = Field(..., description="Date of inspection")
    notes: str = Field(..., description="Raw inspection notes (unstructured text)")
    status: str = Field(
        ...,
        description="Inspection status: completed, incomplete, missed, scheduled"
    )
    inspection_type: Optional[str] = Field(
        None,
        description="Type: routine, compliance, safety, emergency"
    )
    confidence_score: Optional[float] = Field(
        None,
        ge=0.0,
        le=1.0,
        description="Confidence in extracted data (0.0-1.0)"
    )
    metadata: dict = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "inspection_id": "insp_001",
                "site_id": "site_001",
                "inspector_name": "John Smith",
                "inspection_date": "2026-01-04T10:00:00Z",
                "notes": "HVAC filter needs replacement. Noticed water stain on ceiling in break room. Emergency exit sign bulb out.",
                "status": "completed",
                "inspection_type": "routine",
                "confidence_score": 0.95
            }
        }
