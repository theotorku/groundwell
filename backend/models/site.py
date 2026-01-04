"""Site domain model"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class Site(BaseModel):
    """Represents a physical location (store, building, clinic, hotel)"""
    
    site_id: str = Field(..., description="Unique site identifier")
    name: str = Field(..., description="Site name")
    location: str = Field(..., description="Address or location description")
    site_type: str = Field(
        ...,
        description="Type of site: retail, healthcare, hospitality, commercial"
    )
    region: Optional[str] = Field(None, description="Geographic region or district")
    status: str = Field(default="active", description="Site status: active, inactive")
    metadata: dict = Field(default_factory=dict, description="Additional site metadata")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "site_id": "site_001",
                "name": "Downtown Retail Store #45",
                "location": "123 Main St, Austin, TX 78701",
                "site_type": "retail",
                "region": "Southwest",
                "status": "active",
                "metadata": {"square_feet": 5000, "floors": 2}
            }
        }
