import re

backend_path = "/Users/apple/Varun/snappito/backend/backend.py"
with open(backend_path, 'r') as f:
    text = f.read()

new_seeder = """@app.route('/api/seed/services', methods=['POST'])
def seed_services():
    try:
        # 1️⃣ Clear existing data
        Service.query.delete()
        ServiceCategory.query.delete()
        db.session.commit()

        # 2️⃣ Service Categories
        categories_data = [
            {
                "name": "Cleaning Services",
                "description": "Premium home, room, and appliance cleaning packages.",
                "image_url": "assets/premium/sweeping-mopping.png",
                "starting_price": 125
            },
            {
                "name": "Organization & Prep",
                "description": "Professional garment care, organization, and kitchen prep.",
                "image_url": "assets/premium/laundry.png",
                "starting_price": 125
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

        # 3️⃣ Services per Category
        services_data = {
            "Cleaning Services": [
                {"name": "Bathroom Cleaning", "description": "Inside and rim, washbasin, visible tiles, floor sweeping and mopping.", "base_price": 150},
                {"name": "Fridge Cleaning", "description": "Interior surfaces, shelves, basic deodorising, wiping exterior.", "base_price": 150},
                {"name": "Dusting And Wiping", "description": "Dusting of furniture, shelves, corners, and light fixtures.", "base_price": 125},
                {"name": "Sweeping And Mopping", "description": "Sweeping and mopping floors, removing loose dirt.", "base_price": 125},
                {"name": "Pre-party Express Clean", "description": "90 mins living room, kitchen, bathroom, floor mop.", "base_price": 375},
                {"name": "After-party Express Clean", "description": "Spill cleanup, trash disposal, kitchen reset, mopping.", "base_price": 375},
                {"name": "Windows Cleaning", "description": "Dust removal from window mesh, wiping accessible sills.", "base_price": 125},
                {"name": "Kitchen Cleaning", "description": "Countertops, cabinet exteriors, stove top, sink.", "base_price": 150},
                {"name": "Balcony", "description": "Sweeping and mopping, wiping railings and parapet.", "base_price": 125},
                {"name": "Fan Cleaning", "description": "Dust removal from blades and motor body (Ladder required).", "base_price": 125},
                {"name": "Kitchen Cabinet", "description": "Interior and exterior wipe, reorganizing contents.", "base_price": 750}
            ],
            "Organization & Prep": [
                {"name": "Packing And Unpacking", "description": "Clothes, toys, kitchen items, labelling boxes.", "base_price": 125},
                {"name": "Utensils", "description": "Washing, drying, and placing utensils in rack.", "base_price": 125},
                {"name": "Kitchen Preparation", "description": "Chopping veggies, kneading dough, sorting ingredients.", "base_price": 125},
                {"name": "Complete Wardrobe", "description": "Emptying, interior cleaning, folding and rearranging clothes.", "base_price": 750},
                {"name": "Ironing And Folding", "description": "Neat pressing and folding for daily wear garments.", "base_price": 125},
                {"name": "Laundry", "description": "Machine wash, detergent loading, hanging to dry.", "base_price": 125}
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
                    image_url="assets/premium/default.png",
                    is_active=True
                )
                db.session.add(service)

        db.session.commit()
        return jsonify({"message": "Custom 17 Snappito services seeded successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500"""

start_idx = text.find("@app.route('/api/seed/services', methods=['POST'])")
end_idx = text.find("@app.route('/api/service/book', methods=['POST'])")

if start_idx != -1 and end_idx != -1:
    text = text[:start_idx] + new_seeder + "\n    \n" + text[end_idx:]

with open(backend_path, 'w') as f:
    f.write(text)

print("Updated backend.py!")
