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
        {"name": "Cleaning Services", "description": "Professional household cleaning", "starting_price": 50},
        {"name": "Home Items Cleaning", "description": "Cleaning for specific household items", "starting_price": 40},
        {"name": "Moving Services", "description": "Help with packing, unpacking and moving", "starting_price": 100},
        {"name": "Deep / Special Cleaning", "description": "Extensive cleaning for specific areas or whole home", "starting_price": 150},
        {"name": "Occasion Cleaning", "description": "On-demand cleaning services for events", "starting_price": 80},
        {"name": "Specialized Services", "description": "Expert specialized household tasks", "starting_price": 70},
        {"name": "Extra / Add-ons", "description": "Add-on household services", "starting_price": 30}
    ]

    categories = {}
    
    # We assign an image to categories from one of their services
    cat_image_mapping = {
        "Cleaning Services": "service_1.jpg",
        "Home Items Cleaning": "service_9.jpg",
        "Moving Services": "service_13.jpg",
        "Deep / Special Cleaning": "service_16.jpg",
        "Occasion Cleaning": "service_20.jpg",
        "Specialized Services": "service_22.jpg",
        "Extra / Add-ons": "service_24.jpg"
    }

    for cat_data in categories_data:
        cat = ServiceCategory(
            id=generate_uuid(),
            name=cat_data["name"],
            description=cat_data["description"],
            image_url=f"/assets/services/{cat_image_mapping[cat_data['name']]}",
            starting_price=cat_data["starting_price"],
            is_active=True
        )
        db.session.add(cat)
        categories[cat.name] = cat
    
    db.session.commit()

    services_data = {
        "Cleaning Services": [
            ("Sweeping & Mopping", "service_2.jpg"),
            ("Dusting & Wiping", "service_3.jpg"),
            ("Bathroom Cleaning", "service_4.jpg"),
            ("Kitchen Cleaning", "service_5.jpg"),
            ("Balcony Cleaning", "service_6.jpg"),
            ("Window Cleaning", "service_7.jpg"),
            ("Fan Cleaning", "service_8.jpg"),
            ("Car Wash", "service_9.jpg")
        ],
        "Home Items Cleaning": [
            ("Sofa Cleaning", "service_10.jpg"),
            ("Carpet Cleaning", "service_11.jpg"),
            ("Mattress Cleaning", "service_12.jpg"),
            ("Curtain Cleaning", "service_13.jpg")
        ],
        "Moving Services": [
            ("Packing", "service_14.jpg"),
            ("Unpacking", "service_15.jpg"),
            ("Move-in Cleaning", "service_16.jpg")
        ],
        "Deep / Special Cleaning": [
            ("Full Home Deep Cleaning", "service_17.jpg"),
            ("Kitchen Deep Cleaning", "service_18.jpg"),
            ("Bathroom Deep Cleaning", "service_19.jpg"),
            ("Post-Construction Cleaning", "service_20.jpg")
        ],
        "Occasion Cleaning": [
            ("Pre-Party Express Clean", "service_21.jpg"),
            ("After-Party Express Clean", "service_22.jpg")
        ],
        "Specialized Services": [
            ("Water Tank Cleaning", "service_23.jpg"),
            ("Toilet Stain Removal", "service_24.jpg")
        ],
        "Extra / Add-ons": [
            ("Complete Wardrobe Cleaning", "service_25.jpg")
        ]
    }

    for cat_name, svcs in services_data.items():
        cat = categories[cat_name]
        for name, img_file in svcs:
            service = Service(
                id=generate_uuid(),
                category_id=cat.id,
                name=name,
                description=f"Professional {name.lower()} service",
                base_price=cat.starting_price,
                image_url=f"assets/services/{img_file}",
                is_active=True
            )
            db.session.add(service)

    db.session.commit()
    print("Snappito categories and services seeded successfully!")
