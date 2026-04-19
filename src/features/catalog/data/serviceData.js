export const SERVICES = [
    {
        "id": "bathroom-cleaning",
        "title": "Bathroom Cleaning",
        "description": "Professional cleaning of toilet, washbasin, tiles, and floor.",
        "tiers": [
            { "name": "Express", "duration": "30 mins", "price": 150 },
            { "name": "Standard", "duration": "1 hr", "price": 300 }
        ],
        "includes": [
            "Cleaning of toilet bowl (inside and rim)",
            "Cleaning of washbasin and faucet",
            "Wiping bathroom tiles and visible surfaces",
            "Cleaning taps and fixtures",
            "Sweeping and mopping bathroom floor",
            "Final wipe-down and deodorising"
        ],
        "excludes": [
            "Deep cleaning (e.g., tile grout scrubbing)",
            "Removal of heavy mold or hard water stains",
            "Use of acid-based or strong descaling chemicals",
            "Cleaning mirrors or storage interiors",
            "Cleaning shower curtains or drains",
            "Shifting or relocating heavy items"
        ]
    },
    {
        "id": "fridge-cleaning",
        "title": "Fridge Cleaning",
        "description": "Thorough cleaning of refrigerator shelves, trays, and interior walls.",
        "tiers": [
            { "name": "Basic", "duration": "45 mins", "price": 150 },
            { "name": "Standard", "duration": "1 hr", "price": 250 }
        ],
        "includes": [
            "Service includes cleaning of one refrigerator unit only",
            "Switching off the fridge before cleaning",
            "Removing food items and placing them safely aside",
            "Discarding expired or spoiled items (as instructed)",
            "Cleaning shelves, trays, drawers, and compartments",
            "Wiping interior surfaces (walls, door panel, rubber lining)",
            "Basic deodorising of fridge interior",
            "Cleaning fridge exterior (front and sides only)",
            "Drying surfaces before placing items back",
            "Replacing food items neatly into the fridge"
        ],
        "excludes": [
            "Moving or lifting the refrigerator",
            "Cleaning the back panel or condenser coils",
            "Repair or servicing of the fridge",
            "Handling frozen items requiring defrosting",
            "Deep freezer cleaning",
            "Meat handling due to hygiene conditions"
        ]
    },
    {
        "id": "packing-and-unpacking",
        "title": "Packing And Unpacking",
        "description": "Professional packing or unpacking of clothes, kitchen items, and linens.",
        "tiers": [
            { "name": "Express", "duration": "30 mins", "price": 125 },
            { "name": "Standard", "duration": "1 hr", "price": 250 }
        ],
        "includes": [
            "Packing or unpacking clothes, shoes, books, toys, and linens",
            "Packing or unpacking kitchen items and dry groceries",
            "Folding and organising items before packing",
            "Placing items into boxes, suitcases, or cupboards",
            "Labelling boxes (room-wise / item-wise)",
            "Light dusting or surface wipe",
            "Basic organisation using existing storage"
        ],
        "excludes": [
            "Heavy lifting or moving furniture",
            "Carrying boxes up or down stairs",
            "Handling jewellery, cash, or valuables",
            "Packing fragile antiques or artwork",
            "Furniture dismantling or assembly",
            "Providing packing materials (boxes, tapes, etc.)"
        ]
    },
    {
        "id": "utensils",
        "title": "Utensils",
        "description": "Washing and drying of kitchen utensils and cleaning the sink area.",
        "tiers": [
            { "name": "Express", "duration": "30 mins", "price": 125 },
            { "name": "Standard", "duration": "1 hr", "price": 250 }
        ],
        "includes": [
            "Washing utensils with customer-provided supplies",
            "Drying and placing utensils in rack",
            "Cleaning the sink and surrounding area"
        ],
        "excludes": [
            "Cleaning other kitchen areas (slabs, tiles, etc.)",
            "Taking out kitchen garbage",
            "Deep cleaning of burnt utensils"
        ]
    },
    {
        "id": "kitchen-preparation",
        "title": "Kitchen Preparation",
        "description": "Vegetable washing, peeling, chopping and dough kneading assistant.",
        "tiers": [
            { "name": "Express", "duration": "30 mins", "price": 125 },
            { "name": "Standard", "duration": "1 hr", "price": 250 }
        ],
        "includes": [
            "Washing and peeling vegetables",
            "Chopping vegetables as per instruction",
            "Kneading dough (customer provides flour/water)",
            "Sorting prepared items into containers",
            "Basic cleaning of the cutting area"
        ],
        "excludes": [
            "Cooking or full meal preparation",
            "Washing large quantities of utensils",
            "Food processing/grinding using appliances",
            "Cutting meat or frozen items"
        ]
    },
    {
        "id": "dusting-and-wiping",
        "title": "Dusting And Wiping",
        "description": "Dry dusting of furniture surfaces, shelves, and electrical switches.",
        "tiers": [
            { "name": "Express", "duration": "30 mins", "price": 125 },
            { "name": "Standard", "duration": "1 hr", "price": 250 }
        ],
        "includes": [
            "Dry dusting of furniture surfaces and shelves",
            "Dusting of corners and reachable surfaces",
            "Dusting of light fixtures (exterior only)",
            "Dusting of electrical switches and plug points",
            "Minor bed adjustment to dust underneath"
        ],
        "excludes": [
            "Dusting of ceiling fans",
            "Cleaning of windows or window sills",
            "Dusting in balcony or terrace",
            "Wet cleaning of furniture"
        ]
    },
    {
        "id": "sweeping-and-mopping",
        "title": "Sweeping And Mopping",
        "description": "Floor sweeping and mopping using customer equipment.",
        "tiers": [
            { "name": "Express", "duration": "30 mins", "price": 125 },
            { "name": "Standard", "duration": "1 hr", "price": 250 }
        ],
        "includes": [
            "Sweeping and mopping floors in selected rooms",
            "Removing dust and loose dirt",
            "Moving light items (like chairs) for access"
        ],
        "excludes": [
            "Balcony or outdoor cleaning",
            "Deep cleaning / stain removal",
            "Moving heavy furniture",
            "Carpet vacuum cleaning"
        ]
    },
    {
        "id": "pre-party-express-clean",
        "title": "Pre-party Express Clean",
        "description": "Living, dining, kitchen and bathroom refresh before your event.",
        "tiers": [
            { "name": "Standard", "duration": "90 mins", "price": 375 }
        ],
        "includes": [
            "Living room & dining cleaning",
            "Kitchen surface cleaning",
            "Bathroom cleaning",
            "Full house sweeping & mopping",
            "Trash removal",
            "Basic utensil cleaning"
        ],
        "excludes": [
            "Upholstery / interior appliances",
            "Heavy grease or deep stains",
            "Construction debris",
            "Work beyond 90 minutes"
        ]
    },
    {
        "id": "complete-wardrobe",
        "title": "Complete Wardrobe",
        "description": "Interior cleaning and neat organization of your storage spaces.",
        "tiers": [
            { "name": "Standard", "duration": "180 mins", "price": 750 }
        ],
        "includes": [
            "Interior wardrobe cleaning",
            "Emptying and rearranging clothes",
            "Cleaning handles & edges",
            "Dry dusting of shelves and surfaces"
        ],
        "excludes": [
            "Washing or cleaning clothes",
            "Ironing",
            "Polishing wardrobe surface",
            "Moving heavy furniture"
        ]
    },
    {
        "id": "after-party-express-clean",
        "title": "After-party Express Clean",
        "description": "Full home reset including trash disposal and kitchen/bathroom cleaning.",
        "tiers": [
            { "name": "Standard", "duration": "90 mins", "price": 375 }
        ],
        "includes": [
            "Floor & spill cleanup",
            "Trash + bottle disposal",
            "Kitchen reset (counter, sink, stove top)",
            "Bathroom clean",
            "Living room tidy",
            "Full house floor sweeping & mopping"
        ],
        "excludes": [
            "Vomit cleaning",
            "Upholstery/interior appliances",
            "Heavy grease or deep stains",
            "Bulk waste removal"
        ]
    },
    {
        "id": "ironing-and-folding",
        "title": "Ironing And Folding",
        "description": "Professional ironing and neat folding of daily wear garments.",
        "tiers": [
            { "name": "Express", "duration": "30 mins", "price": 125 },
            { "name": "Standard", "duration": "1 hr", "price": 250 }
        ],
        "includes": [
            "Ironing of daily wear (shirts, t-shirts, trousers)",
            "Neat folding of ironed clothes"
        ],
        "excludes": [
            "Steam Ironing",
            "Blazers, coats, or delicate sarees",
            "Party wear or designer garments",
            "Washing or drying of clothes"
        ]
    },
    {
        "id": "windows-cleaning",
        "title": "Windows Cleaning",
        "description": "Interior window mesh and track cleaning for a clearer view.",
        "tiers": [
            { "name": "Express", "duration": "30 mins", "price": 125 },
            { "name": "Standard", "duration": "1 hr", "price": 250 }
        ],
        "includes": [
            "Surface dust removal from window mesh/screens",
            "Wiping window sills (from inside)",
            "Cleaning interior window tracks/channels"
        ],
        "excludes": [
            "Exterior window glass cleaning",
            "Cleaning other surfaces (walls/furniture)",
            "Removal of old paint marks or hard deposits",
            "Deep scrubbing of tracks"
        ]
    },
    {
        "id": "laundry",
        "title": "Laundry",
        "description": "Washing machine assistant: load, detergent, and drying help.",
        "tiers": [
            { "name": "Express", "duration": "30 mins", "price": 125 },
            { "name": "Standard", "duration": "1 hr", "price": 250 }
        ],
        "includes": [
            "Washing clothes using customer's machine",
            "Adding detergent in correct compartments",
            "Selecting fabric-appropriate wash mode",
            "Hanging washed clothes for drying"
        ],
        "excludes": [
            "Hand-washing",
            "Ironing or folding",
            "Stain treatment",
            "Washing machine repair"
        ]
    },
    {
        "id": "kitchen-cleaning",
        "title": "Kitchen Cleaning",
        "description": "Cleaning of countertops, cabinets, stove exterior and tiles.",
        "tiers": [
            { "name": "Express", "duration": "30 mins", "price": 150 },
            { "name": "Standard", "duration": "1 hr", "price": 300 }
        ],
        "includes": [
            "Wiping countertops and slabs",
            "Cleaning exterior of cabinets",
            "Cleaning exterior of cooking stove",
            "Wiping visible wall tiles",
            "Cleaning exterior of sink"
        ],
        "excludes": [
            "Washing or soaking utensils",
            "Rearranging contents inside cabinets",
            "Taking out kitchen garbage",
            "Appliance interior cleaning (chimney/fridge)"
        ]
    },
    {
        "id": "balcony",
        "title": "Balcony",
        "description": "Sweeping, mopping, and railing wipe-down for your outdoor space.",
        "tiers": [
            { "name": "Express", "duration": "30 mins", "price": 125 },
            { "name": "Standard", "duration": "1 hr", "price": 250 }
        ],
        "includes": [
            "Sweeping and mopping balcony floor",
            "Cleaning and wiping railings and grills",
            "Cleaning and wiping parapet wall",
            "Dusting accessible balcony furniture"
        ],
        "excludes": [
            "Cleaning walls or ceiling",
            "Watering plants or gardening",
            "Terrace/roof areas",
            "Moving heavy pots"
        ]
    },
    {
        "id": "fan-cleaning",
        "title": "Fan Cleaning",
        "description": "Dusting and wiping of fan blades and motor bodies. Ladder required.",
        "tiers": [
            { "name": "Express", "duration": "30 mins", "price": 125 },
            { "name": "Standard", "duration": "1 hr", "price": 250 }
        ],
        "includes": [
            "Dust removal from fan blades and motor body",
            "Wiping fan blades and parts",
            "Cleaning fallen dust from floor"
        ],
        "excludes": [
            "Ladder not provided (please provide one)",
            "Cleaning exhaust or internal parts",
            "Disassembly of fan",
            "Moving heavy furniture"
        ],
        "requiresCustomerEquipment": true,
        "equipmentTitle": "Ladder Required",
        "equipmentDesc": "Please provide a safe ladder for the professional.",
        "confirmText": "I have a ladder"
    },
    {
        "id": "kitchen-cabinet",
        "title": "Kitchen Cabinet",
        "description": "Deep interior and exterior wipe-down of all kitchen storage.",
        "tiers": [
            { "name": "Standard", "duration": "180 mins", "price": 750 }
        ],
        "includes": [
            "Interior cleaning of all cabinets",
            "Dry and wet wipe",
            "Emptying & rearranging contents",
            "Exterior cabinet cleaning"
        ],
        "excludes": [
            "Deep grease removal",
            "Washing utensils",
            "Cabinet repair or repainting",
            "Hard water or rust stains"
        ]
    }
];