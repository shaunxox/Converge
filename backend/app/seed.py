import logging
from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.recycler import Recycler
from app.models.collector import Collector
from app.models.price import PriceObservation
from app.models.enums import AuthorizationStatus, MaterialCategory, PriceChannel, ObservationSource, ObservationUnit, AccountType, PreferredLanguage

logger = logging.getLogger("seed")

def seed_database(db: Session):
    # Check if recyclers already exist
    existing_count = db.query(Recycler).count()
    if existing_count > 0:
        return

    logger.info("Seeding initial collectors, shop SHOP-9876, recyclers and price observations...")

    # Seed default shop owner & feriwalas in Mangalore
    shop_owner = Collector(
        collector_id="col-demo-101",
        phone_number="9876543210",
        display_name="Ramesh Kumar (Ganesh Kabadi Shop)",
        preferred_language=PreferredLanguage.hi,
        operating_locality="Bunder, Mangalore",
        account_type=AccountType.shop,
        shop_code="SHOP-9876",
    )
    db.add(shop_owner)
    db.commit()
    db.refresh(shop_owner)

    feriwala1 = Collector(
        collector_id="col-sub-001",
        phone_number="9822011223",
        display_name="Suresh Poojary (Feriwala)",
        preferred_language=PreferredLanguage.kn,
        operating_locality="Kadri, Mangalore",
        account_type=AccountType.sub_collector,
        parent_shop_id=shop_owner.collector_id,
    )
    feriwala2 = Collector(
        collector_id="col-sub-002",
        phone_number="9822044556",
        display_name="Vikram Shetty (Feriwala)",
        preferred_language=PreferredLanguage.kn,
        operating_locality="Surathkal, Mangalore",
        account_type=AccountType.sub_collector,
        parent_shop_id=shop_owner.collector_id,
    )
    feriwala3 = Collector(
        collector_id="col-ind-001",
        phone_number="9800033333",
        display_name="Anil Rai (Independent Collector)",
        preferred_language=PreferredLanguage.kn,
        operating_locality="Bejai, Mangalore",
        account_type=AccountType.independent,
    )
    db.add(feriwala1)
    db.add(feriwala2)
    db.add(feriwala3)
    db.commit()

    recyclers_data = [
        # Mangalore & Coastal Karnataka Hub Recyclers (KSPPCB Registered)
        {
            "recycler_id": "rec-mgl-001",
            "name": "EcoRecycle Mangalore (Baikampady Industrial Hub)",
            "facility_lat": 12.9463,
            "facility_lng": 74.8080,
            "service_radius_km": 30.0,
            "materials_accepted": ["PCB", "BATTERY", "CABLE", "LCD_PANEL", "CRT", "MOTOR_MAGNET", "MIXED_PLASTIC"],
            "authorization_status": AuthorizationStatus.verified,
            "authorization_ref_no": "KSPPCB/E-WASTE/2024/052",
            "contact_phone": "9888888888",
            "offered_rates": {"PCB": 265.0, "BATTERY": 92.0, "CABLE": 152.0, "LCD_PANEL": 110.0, "CRT": 40.0, "MOTOR_MAGNET": 72.0, "MIXED_PLASTIC": 25.0},
            "pickup_available": True,
        },
        {
            "recycler_id": "rec-mgl-002",
            "name": "Coastal Karnataka Green Recyclers",
            "facility_lat": 13.0067,
            "facility_lng": 74.7943,
            "service_radius_km": 35.0,
            "materials_accepted": ["PCB", "CABLE", "MOTOR_MAGNET", "BATTERY"],
            "authorization_status": AuthorizationStatus.verified,
            "authorization_ref_no": "KSPPCB/E-WASTE/2024/088",
            "contact_phone": "9765432109",
            "offered_rates": {"PCB": 260.0, "CABLE": 155.0, "MOTOR_MAGNET": 75.0, "BATTERY": 95.0},
            "pickup_available": True,
        },
        {
            "recycler_id": "rec-mgl-003",
            "name": "Dakshina E-Scrap & Metal Processors (Yeyyadi)",
            "facility_lat": 12.8935,
            "facility_lng": 74.8622,
            "service_radius_km": 25.0,
            "materials_accepted": ["PCB", "BATTERY", "CABLE", "LCD_PANEL", "CRT", "MOTOR_MAGNET", "MIXED_PLASTIC"],
            "authorization_status": AuthorizationStatus.verified,
            "authorization_ref_no": "KSPPCB/E-WASTE/2024/034",
            "contact_phone": "9812345678",
            "offered_rates": {"PCB": 275.0, "BATTERY": 98.0, "CABLE": 160.0, "LCD_PANEL": 115.0, "CRT": 42.0, "MOTOR_MAGNET": 78.0, "MIXED_PLASTIC": 26.0},
            "pickup_available": True,
        },
        {
            "recycler_id": "rec-mgl-004",
            "name": "Kudla E-Waste Solutions (Bunder Port)",
            "facility_lat": 12.8622,
            "facility_lng": 74.8355,
            "service_radius_km": 20.0,
            "materials_accepted": ["PCB", "BATTERY", "CABLE"],
            "authorization_status": AuthorizationStatus.verified,
            "authorization_ref_no": "KSPPCB/E-WASTE/2024/115",
            "contact_phone": "9833445566",
            "offered_rates": {"PCB": 280.0, "BATTERY": 100.0, "CABLE": 165.0},
            "pickup_available": False,
        },
        {
            "recycler_id": "rec-udupi-001",
            "name": "Udupi & Manipal CleanTech Recovery",
            "facility_lat": 13.3409,
            "facility_lng": 74.7421,
            "service_radius_km": 40.0,
            "materials_accepted": ["PCB", "BATTERY", "CABLE", "LCD_PANEL"],
            "authorization_status": AuthorizationStatus.verified,
            "authorization_ref_no": "KSPPCB/E-WASTE/2024/204",
            "contact_phone": "9844556677",
            "offered_rates": {"PCB": 270.0, "BATTERY": 96.0, "CABLE": 158.0, "LCD_PANEL": 112.0},
            "pickup_available": True,
        },
        # Legacy ID alias for rec-pune-001 so existing tests & cache don't fail
        {
            "recycler_id": "rec-pune-001",
            "name": "EcoRecycle Mangalore (Hub 1)",
            "facility_lat": 12.9463,
            "facility_lng": 74.8080,
            "service_radius_km": 30.0,
            "materials_accepted": ["PCB", "BATTERY", "CABLE", "LCD_PANEL", "CRT", "MOTOR_MAGNET", "MIXED_PLASTIC"],
            "authorization_status": AuthorizationStatus.verified,
            "authorization_ref_no": "KSPPCB/E-WASTE/2024/052",
            "contact_phone": "9888888888",
            "offered_rates": {"PCB": 265.0, "BATTERY": 92.0, "CABLE": 152.0, "LCD_PANEL": 110.0, "CRT": 40.0, "MOTOR_MAGNET": 72.0, "MIXED_PLASTIC": 25.0},
            "pickup_available": True,
        },
    ]

    for r in recyclers_data:
        rec = Recycler(**r)
        db.add(rec)

    db.commit()

    # Seed Price Observations across regional coastal Karnataka districts
    districts = [
        ("Mangalore", {"PCB": 265, "BATTERY": 92, "CABLE": 152, "LCD_PANEL": 110, "CRT": 40, "MOTOR_MAGNET": 72, "MIXED_PLASTIC": 25}),
        ("Surathkal", {"PCB": 260, "BATTERY": 95, "CABLE": 155, "LCD_PANEL": 112, "CRT": 42, "MOTOR_MAGNET": 75, "MIXED_PLASTIC": 26}),
        ("Udupi", {"PCB": 270, "BATTERY": 96, "CABLE": 158, "LCD_PANEL": 112, "CRT": 42, "MOTOR_MAGNET": 72, "MIXED_PLASTIC": 26}),
        ("Manipal", {"PCB": 275, "BATTERY": 98, "CABLE": 160, "LCD_PANEL": 115, "CRT": 42, "MOTOR_MAGNET": 74, "MIXED_PLASTIC": 26}),
        ("Puttur", {"PCB": 250, "BATTERY": 88, "CABLE": 145, "LCD_PANEL": 105, "CRT": 38, "MOTOR_MAGNET": 68, "MIXED_PLASTIC": 23}),
        ("Bangalore", {"PCB": 285, "BATTERY": 105, "CABLE": 165, "LCD_PANEL": 125, "CRT": 45, "MOTOR_MAGNET": 80, "MIXED_PLASTIC": 28}),
        ("Pune", {"PCB": 260, "BATTERY": 90, "CABLE": 150, "LCD_PANEL": 110, "CRT": 40, "MOTOR_MAGNET": 70, "MIXED_PLASTIC": 25}),  # fallback compatibility
    ]

    now = datetime.now(timezone.utc)
    for dist_name, rates in districts:
        for cat_str, formal_price in rates.items():
            cat_enum = MaterialCategory[cat_str]

            # Formal observation
            obs_formal = PriceObservation(
                material_category=cat_enum,
                sub_category=cat_str,
                location_district=dist_name,
                observed_at=now - timedelta(days=1),
                buying_price=float(formal_price),
                quoted_price=float(formal_price),
                unit=ObservationUnit.per_kg,
                market_range_low=float(formal_price * 0.92),
                market_range_high=float(formal_price * 1.08),
                source=ObservationSource.manual_admin_entry,
                channel=PriceChannel.formal,
            )
            db.add(obs_formal)

            # Informal reference observation
            obs_informal = PriceObservation(
                material_category=cat_enum,
                sub_category=cat_str,
                location_district=dist_name,
                observed_at=now - timedelta(days=2),
                buying_price=float(round(formal_price * 0.82, 1)),
                quoted_price=float(round(formal_price * 0.82, 1)),
                unit=ObservationUnit.per_kg,
                source=ObservationSource.manual_admin_entry,
                channel=PriceChannel.informal,
            )
            db.add(obs_informal)

    db.commit()
    logger.info("Database seeding complete!")
