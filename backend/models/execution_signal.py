"""ExecutionSignal domain model"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ExecutionSignal(BaseModel):
    """Represents a detected execution breakdown or risk indicator"""
    
    signal_id: str = Field(..., description="Unique signal identifier")
    site_id: str = Field(..., description="Associated site ID")
    signal_type: str = Field(
        ...,
        description="Type: missed_inspection, late_work_order, incomplete_task, doc_gap, sla_breach, safety_issue"
    )
    severity: str = Field(
        ...,
        description="Severity: low, medium, high, critical"
    )
    detected_date: datetime = Field(..., description="When the signal was detected")
    confidence_score: float = Field(
        ...,
        ge=0.0,
        le=1.0,
        description="Confidence in signal detection (0.0-1.0)"
    )
    evidence: dict = Field(
        ...,
        description="Evidence supporting the signal (quotes, data points)"
    )
    explanation: str = Field(
        ...,
        description="Human-readable explanation of why this is a problem"
    )
    source_type: Optional[str] = Field(
        None,
        description="Source: inspection, work_order, manual"
    )
    source_id: Optional[str] = Field(
        None,
        description="ID of source document (inspection_id, work_order_id)"
    )
    resolved: bool = Field(default=False, description="Whether signal has been addressed")
    resolved_date: Optional[datetime] = Field(None, description="Resolution date")
    metadata: dict = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "signal_id": "sig_001",
                "site_id": "site_001",
                "signal_type": "incomplete_task",
                "severity": "medium",
                "detected_date": "2026-01-04T10:00:00Z",
                "confidence_score": 0.89,
                "evidence": {
                    "quote": "HVAC filter needs replacement",
                    "inspection_id": "insp_001"
                },
                "explanation": "Inspection identified required maintenance task that has not been converted to a work order",
                "source_type": "inspection",
                "source_id": "insp_001",
                "resolved": False
            }
        }
