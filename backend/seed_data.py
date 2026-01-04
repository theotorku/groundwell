"""
Seed data script for Groundswell demo
Creates 3 scenarios for pilot demonstration
"""

import asyncio
import uuid
from datetime import datetime, timedelta
from backend.models import Site, Inspection, WorkOrder, Vendor, ExecutionSignal
from backend.agents import SignalExtractorAgent, RiskScorerAgent
from backend.db.config import Database


async def create_seed_data():
    """Create demo seed data for all three scenarios"""
    
    db = Database.get_client()
    signal_extractor = SignalExtractorAgent()
    risk_scorer = RiskScorerAgent()
    
    print("🌱 Seeding Groundswell database...")
    
    # Scenario 1: The Neglected Region
    print("\n📍 Creating Scenario 1: The Neglected Region")
    
    neglected_sites = []
    for i in range(1, 6):
        site = Site(
            site_id=f"site_neg_{i}",
            name=f"Southwest Retail #{i}",
            location=f"{100 + i} Main St, Phoenix, AZ",
            site_type="retail",
            region="Southwest",
            status="active"
        )
        neglected_sites.append(site)
        db.table("sites").insert(site.model_dump(mode="json")).execute()
    
    # Add missed inspections
    for site in neglected_sites[:3]:
        inspection = Inspection(
            inspection_id=str(uuid.uuid4()),
            site_id=site.site_id,
            inspector_name="John Smith",
            inspection_date=datetime.utcnow() - timedelta(days=15),
            notes="HVAC filter severely clogged. Water damage visible on ceiling tiles in break room. Emergency exit sign not functional. Floor tiles cracked near entrance.",
            status="incomplete",
            inspection_type="routine",
            confidence_score=0.92
        )
        db.table("inspections").insert(inspection.model_dump(mode="json")).execute()
        
        # Extract signals
        signals = await signal_extractor.extract_from_inspection(
            inspection.inspection_id,
            inspection.site_id,
            inspection.notes
        )
        if signals:
            for signal in signals:
                db.table("execution_signals").insert(signal.model_dump(mode="json")).execute()
        
        # Calculate risk score
        risk_score = risk_scorer.calculate_site_risk(site.site_id, signals)
        db.table("risk_scores").insert(risk_score.model_dump(mode="json")).execute()
    
    # Scenario 2: Vendor Performance Issues
    print("\n🔧 Creating Scenario 2: Vendor Performance Issues")
    
    # Create vendor
    vendor = Vendor(
        vendor_id="vendor_001",
        name="QuickFix HVAC Services",
        service_type="HVAC",
        contact_name="Mike Johnson",
        contact_email="mike@quickfix.com",
        status="active",
        sla_response_time_hours=24,
        performance_rating=2.5
    )
    db.table("vendors").insert(vendor.model_dump(mode="json")).execute()
    
    vendor_sites = []
    for i in range(1, 4):
        site = Site(
            site_id=f"site_vendor_{i}",
            name=f"Northeast Clinic #{i}",
            location=f"{200 + i} Oak Ave, Boston, MA",
            site_type="healthcare",
            region="Northeast",
            status="active"
        )
        vendor_sites.append(site)
        db.table("sites").insert(site.model_dump(mode="json")).execute()
        
        # Create late work order
        work_order = WorkOrder(
            work_order_id=str(uuid.uuid4()),
            site_id=site.site_id,
            vendor_id=vendor.vendor_id,
            title="HVAC System Repair",
            description="Air conditioning not cooling properly. Temperature reading 78°F when set to 68°F.",
            priority="high",
            status="in_progress",
            created_date=datetime.utcnow() - timedelta(days=10),
            due_date=datetime.utcnow() - timedelta(days=3),
            estimated_cost=850.00
        )
        db.table("work_orders").insert(work_order.model_dump(mode="json")).execute()
        
        # Extract signals from late work order
        signals = await signal_extractor.extract_from_work_order(
            work_order.work_order_id,
            work_order.site_id,
            work_order.description,
            work_order.created_date,
            work_order.due_date,
            work_order.status
        )
        if signals:
            for signal in signals:
                db.table("execution_signals").insert(signal.model_dump(mode="json")).execute()
        
        # Calculate risk score
        risk_score = risk_scorer.calculate_site_risk(site.site_id, signals)
        db.table("risk_scores").insert(risk_score.model_dump(mode="json")).execute()
    
    # Scenario 3: Well-Managed Portfolio
    print("\n✅ Creating Scenario 3: Well-Managed Portfolio")
    
    managed_sites = []
    for i in range(1, 4):
        site = Site(
            site_id=f"site_managed_{i}",
            name=f"Midwest Hotel #{i}",
            location=f"{300 + i} Park Blvd, Chicago, IL",
            site_type="hospitality",
            region="Midwest",
            status="active"
        )
        managed_sites.append(site)
        db.table("sites").insert(site.model_dump(mode="json")).execute()
        
        # Create completed inspection with no issues
        inspection = Inspection(
            inspection_id=str(uuid.uuid4()),
            site_id=site.site_id,
            inspector_name="Sarah Williams",
            inspection_date=datetime.utcnow() - timedelta(days=2),
            notes="All systems operational. HVAC filters changed on schedule. No safety concerns observed. Documentation complete.",
            status="completed",
            inspection_type="routine",
            confidence_score=0.98
        )
        db.table("inspections").insert(inspection.model_dump(mode="json")).execute()
        
        # These sites will have very few or no signals
        signals = await signal_extractor.extract_from_inspection(
            inspection.inspection_id,
            inspection.site_id,
            inspection.notes
        )
        if signals:
            for signal in signals:
                db.table("execution_signals").insert(signal.model_dump(mode="json")).execute()
        
        # Calculate risk score (should be low)
        risk_score = risk_scorer.calculate_site_risk(site.site_id, signals)
        db.table("risk_scores").insert(risk_score.model_dump(mode="json")).execute()
    
    print("\n✅ Seed data created successfully!")
    print(f"   - {len(neglected_sites)} sites in Neglected Region scenario")
    print(f"   - {len(vendor_sites)} sites in Vendor Performance scenario")
    print(f"   - {len(managed_sites)} sites in Well-Managed scenario")
    print(f"   - Total: {len(neglected_sites) + len(vendor_sites) + len(managed_sites)} sites")


if __name__ == "__main__":
    asyncio.run(create_seed_data())
