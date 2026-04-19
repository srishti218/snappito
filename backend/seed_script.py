import uuid
from backend import db, app
from backend import ServiceCategory, Service

def generate_uuid():
    return str(uuid.uuid4())

with app.app_context():
    # Ensure tables exist
    db.create_all()
    # Clear existing data
    db.session.query(Service).delete()
    db.session.query(ServiceCategory).delete()
    db.session.commit()

    categories_data = [
        {"name": "Cleaning Services", "description": "Professional household cleaning"},
        {"name": "Kitchen Solutions", "description": "Specialized kitchen cleaning and preparation"},
        {"name": "Home Maintenance", "description": "Dusting, wiping and balcony care"},
        {"name": "Specialized Care", "description": "Laundry, ironing and fan cleaning"},
        {"name": "Express Packages", "description": "One-time deep cleaning for events"}
    ]

    categories = {}
    
    for cat_data in categories_data:
        cat = ServiceCategory(
            id=generate_uuid(),
            name=cat_data["name"],
            description=cat_data["description"],
            image_url=f"/assets/services/default.jpg",
            starting_price=125,
            is_active=True
        )
        db.session.add(cat)
        categories[cat.name] = cat
    
    db.session.commit()

    # (Name, Category, Price, Description)
    services_list = [
        ("Bathroom Cleaning", "Cleaning Services", 150, "Cleaning of toilet, washbasin, tiles and floor."),
        ("Fridge Cleaning", "Kitchen Solutions", 150, "Cleaning of shelves, trays, drawers and interior."),
        ("Packing And Unpacking", "Cleaning Services", 125, "Professional folding and packing assistant."),
        ("Utensils", "Kitchen Solutions", 125, "Washing, drying and sink area cleaning."),
        ("Kitchen Preparation", "Kitchen Solutions", 125, "Vegetable chopping and dough kneading."),
        ("Dusting And Wiping", "Home Maintenance", 125, "Dry dusting of surfaces and fixtures."),
        ("Sweeping And Mopping", "Home Maintenance", 125, "Floor sweeping and mopping services."),
        ("Pre-party Express Clean", "Express Packages", 375, "Full home refresh before your event."),
        ("Complete Wardrobe", "Home Maintenance", 750, "Interior organization and shelf dusting."),
        ("After-party Express Clean", "Express Packages", 375, "Home reset and spill cleanup after event."),
        ("Ironing And Folding", "Specialized Care", 125, "Professional ironing of daily wear clothes."),
        ("Windows Cleaning", "Home Maintenance", 125, "Interior window mesh and track cleaning."),
        ("Laundry", "Specialized Care", 125, "Washing machine assistant and drying help."),
        ("Kitchen Cleaning", "Kitchen Solutions", 150, "Countertops, cabinets and stove exterior."),
        ("Balcony", "Home Maintenance", 125, "Sweeping and mopping of balcony area."),
        ("Fan Cleaning", "Specialized Care", 125, "Dust removal from blades and motor body."),
        ("Kitchen Cabinet", "Kitchen Solutions", 750, "Deep interior and exterior cabinet cleaning.")
    ]

    for name, cat_name, price, desc in services_list:
        cat = categories[cat_name]
        service = Service(
            id=generate_uuid(),
            category_id=cat.id,
            name=name,
            description=desc,
            base_price=float(price),
            image_url=f"assets/services/service.jpg",
            is_active=True
        )
        db.session.add(service)

    db.session.commit()
    print("Snappito categories and services updated successfully from Master Table.")
