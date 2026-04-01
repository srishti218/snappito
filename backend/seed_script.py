import uuid
from backend import db
from backend import ServiceCategory, Service  # adjust import according to your project

def generate_uuid():
    return str(uuid.uuid4())

# Clear existing data (optional)
Service.query.delete()
ServiceCategory.query.delete()
db.session.commit()

# 1️⃣ Service Categories
categories_data = [
    {
        "name": "Home Cleaning",
        "description": "Professional deep cleaning, regular maintenance, and specialized cleaning services",
        "image_url": "https://picsum.photos/seed/home_cleaning/400/300",
        "starting_price": 50
    },
    {
        "name": "Home Repairs",
        "description": "Expert technicians for plumbing, electrical, carpentry, and general repairs",
        "image_url": "https://picsum.photos/seed/home_repairs/400/300",
        "starting_price": 75
    },
    {
        "name": "Beauty & Wellness",
        "description": "Professional beauty services in the comfort of your home",
        "image_url": "https://picsum.photos/seed/beauty_wellness/400/300",
        "starting_price": 40
    },
    {
        "name": "Appliance Repair",
        "description": "Quick and reliable repair services for all your home appliances",
        "image_url": "https://picsum.photos/seed/appliance_repair/400/300",
        "starting_price": 60
    },
    {
        "name": "Painting",
        "description": "Professional painting services for interior and exterior spaces",
        "image_url": "https://picsum.photos/seed/painting/400/300",
        "starting_price": 100
    },
    {
        "name": "Pest Control",
        "description": "Safe and effective pest control solutions for your home",
        "image_url": "https://picsum.photos/seed/pest_control/400/300",
        "starting_price": 80
    }
]

categories = []
for cat_data in categories_data:
    cat = ServiceCategory(
        id=generate_uuid(),
        name=cat_data["name"],
        description=cat_data["description"],
        image_url=cat_data["image_url"],
        starting_price=cat_data["starting_price"],
        is_active=True
    )
    db.session.add(cat)
    categories.append(cat)

db.session.commit()

# 2️⃣ Services per Category
services_data = {
    "Home Cleaning": [
        {"name": "Deep Cleaning", "description": "Thorough cleaning for entire home", "base_price": 50, "image_url": "https://picsum.photos/seed/deep_cleaning/400/300"},
        {"name": "Regular Cleaning", "description": "Daily/weekly scheduled cleaning", "base_price": 50, "image_url": "https://picsum.photos/seed/regular_cleaning/400/300"},
        {"name": "Move-in/out Cleaning", "description": "Cleaning service for moving homes", "base_price": 60, "image_url": "https://picsum.photos/seed/move_cleaning/400/300"}
    ],
    "Home Repairs": [
        {"name": "Plumbing", "description": "All plumbing services", "base_price": 75, "image_url": "https://picsum.photos/seed/plumbing/400/300"},
        {"name": "Electrical", "description": "Electrical repair services", "base_price": 75, "image_url": "https://picsum.photos/seed/electrical/400/300"},
        {"name": "Carpentry", "description": "Woodwork and furniture repairs", "base_price": 75, "image_url": "https://picsum.photos/seed/carpentry/400/300"}
    ],
    "Beauty & Wellness": [
        {"name": "Hair Styling", "description": "Professional hair styling at home", "base_price": 40, "image_url": "https://picsum.photos/seed/hair_styling/400/300"},
        {"name": "Massage", "description": "Relaxing massage therapy", "base_price": 40, "image_url": "https://picsum.photos/seed/massage/400/300"},
        {"name": "Skincare", "description": "Facials and skincare treatments", "base_price": 40, "image_url": "https://picsum.photos/seed/skincare/400/300"}
    ],
    "Appliance Repair": [
        {"name": "AC Service", "description": "AC installation and repair", "base_price": 60, "image_url": "https://picsum.photos/seed/ac_service/400/300"},
        {"name": "Washing Machine", "description": "Washing machine repair", "base_price": 60, "image_url": "https://picsum.photos/seed/washing_machine/400/300"},
        {"name": "Refrigerator", "description": "Refrigerator repair", "base_price": 60, "image_url": "https://picsum.photos/seed/refrigerator/400/300"}
    ],
    "Painting": [
        {"name": "Interior Painting", "description": "Paint walls and ceilings inside your home", "base_price": 100, "image_url": "https://picsum.photos/seed/interior_painting/400/300"},
        {"name": "Exterior Painting", "description": "Paint outer walls and facades", "base_price": 100, "image_url": "https://picsum.photos/seed/exterior_painting/400/300"},
        {"name": "Touch-ups", "description": "Small touch-up painting jobs", "base_price": 100, "image_url": "https://picsum.photos/seed/touchups/400/300"}
    ],
    "Pest Control": [
        {"name": "Termite Control", "description": "Protect your home from termites", "base_price": 80, "image_url": "https://picsum.photos/seed/termite/400/300"},
        {"name": "Cockroach Control", "description": "Eliminate cockroach infestations", "base_price": 80, "image_url": "https://picsum.photos/seed/cockroach/400/300"},
        {"name": "General Pest", "description": "Control all common household pests", "base_price": 80, "image_url": "https://picsum.photos/seed/general_pest/400/300"}
    ]
}

for cat in categories:
    for svc in services_data.get(cat.name, []):
        service = Service(
            id=generate_uuid(),
            category_id=cat.id,
            name=svc["name"],
            description=svc["description"],
            base_price=svc["base_price"],
            image_url=svc["image_url"],
            is_active=True
        )
        db.session.add(service)

db.session.commit()
print("UrbanEase categories and services seeded successfully!")
