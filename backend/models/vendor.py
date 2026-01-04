"""Vendor domain model"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Vendor(BaseModel):
    """Represents an external service provider"""
    
    vendor_id: str = Field(..., description="Unique vendor identifier")
    name: str = Field(..., description="Vendor company name")
    service_type: str = Field(
        ...,
        description="Type of service: HVAC, plumbing, electrical, cleaning, landscaping"
    )
    contact_name: Optional[str] = Field(None, description="Primary contact name")
    contact_email: Optional[str] = Field(None, description="Contact email")
    contact_phone: Optional[str] = Field(None, description="Contact phone")
    status: str = Field(default="active", description="Status: active, inactive")
    sla_response_time_hours: Optional[int] = Field(
        None,
        description="SLA response time in hours"
    )
    performance_rating: Optional[float] = Field(
        None,
        ge=0.0,
        le=5.0,
        description="Performance rating (0.0-5.0)"
    )
    metadata: dict = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "vendor_id": "vendor_001",
                "name": "CoolAir HVAC Services",
                "service_type": "HVAC",
                "contact_name": "Mike Johnson",
                "contact_email": "mike@coolair.com",
                "contact_phone": "555-0123",
                "status": "active",
                "sla_response_time_hours": 24,
                "performance_rating": 4.5
            }
        }
