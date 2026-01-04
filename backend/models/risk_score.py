"""RiskScore domain model"""

from datetime import datetime
from pydantic import BaseModel, Field


class RiskScore(BaseModel):
    """Represents aggregated execution risk for a site"""
    
    risk_score_id: str = Field(..., description="Unique risk score identifier")
    site_id: str = Field(..., description="Associated site ID")
    score: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Risk score (0-100, higher is riskier)"
    )
    calculated_date: datetime = Field(..., description="When score was calculated")
    contributing_signals: list[str] = Field(
        ...,
        description="List of signal IDs contributing to this score"
    )
    explanation: str = Field(
        ...,
        description="Human-readable explanation of the risk score"
    )
    trend: str = Field(
        ...,
        description="Risk trend: improving, stable, deteriorating"
    )
    breakdown: dict = Field(
        default_factory=dict,
        description="Score breakdown by signal type"
    )
    metadata: dict = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "risk_score_id": "risk_001",
                "site_id": "site_001",
                "score": 67.5,
                "calculated_date": "2026-01-04T10:00:00Z",
                "contributing_signals": ["sig_001", "sig_002", "sig_003"],
                "explanation": "Site shows elevated risk due to 2 missed inspections, 1 late work order, and incomplete maintenance tasks",
                "trend": "deteriorating",
                "breakdown": {
                    "missed_inspection": 30.0,
                    "late_work_order": 20.0,
                    "incomplete_task": 17.5
                }
            }
        }
