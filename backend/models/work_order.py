"""WorkOrder domain model"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class WorkOrder(BaseModel):
    """Represents a maintenance or service task"""
    
    work_order_id: str = Field(..., description="Unique work order identifier")
    site_id: str = Field(..., description="Associated site ID")
    vendor_id: Optional[str] = Field(None, description="Assigned vendor ID")
    title: str = Field(..., description="Work order title")
    description: str = Field(..., description="Detailed description of work")
    priority: str = Field(
        default="medium",
        description="Priority: low, medium, high, critical"
    )
    status: str = Field(
        ...,
        description="Status: pending, in_progress, completed, late, cancelled"
    )
    created_date: datetime = Field(..., description="Date work order was created")
    due_date: datetime = Field(..., description="Expected completion date")
    completed_date: Optional[datetime] = Field(
        None,
        description="Actual completion date"
    )
    estimated_cost: Optional[float] = Field(None, description="Estimated cost in USD")
    actual_cost: Optional[float] = Field(None, description="Actual cost in USD")
    metadata: dict = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "work_order_id": "wo_001",
                "site_id": "site_001",
                "vendor_id": "vendor_001",
                "title": "Replace HVAC Filter",
                "description": "Replace main HVAC filter in rooftop unit",
                "priority": "medium",
                "status": "in_progress",
                "created_date": "2026-01-01T09:00:00Z",
                "due_date": "2026-01-05T17:00:00Z",
                "estimated_cost": 150.00
            }
        }
