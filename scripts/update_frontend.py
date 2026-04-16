import json

services = [
    {
      "id": "bathroom-cleaning", "title": "Bathroom Cleaning", "price": 150, "duration": "30 mins - 1 hr",
      "includes": [
        "Cleaning of toilet bowl (inside and rim)", "Cleaning of washbasin and faucet",
        "Wiping bathroom tiles and visible surfaces", "Cleaning taps and fixtures",
        "Sweeping and mopping bathroom floor", "Final wipe-down and deodorising"
      ],
      "excludes": [
        "Deep cleaning (e.g., tile grout scrubbing)", "Removal of heavy mold or hard water stains",
        "Use of acid-based or strong descaling chemicals", "Cleaning mirrors or storage interiors",
        "Cleaning shower curtains or drains", "Shifting or relocating heavy items"
      ],
      "requiresCustomerEquipment": False, "isActive": True
    },
    {
      "id": "fridge-cleaning", "title": "Fridge Cleaning", "price": 150, "duration": "45 mins - 1 hr",
      "includes": [
        "Service includes cleaning of one refrigerator unit only",
        "Estimated cleaning time depends on fridge size", "Switching off the fridge before cleaning",
        "Removing food items and placing them safely aside", "Discarding expired or spoiled items (as instructed)",
        "Cleaning shelves, trays, drawers, and compartments", "Wiping interior surfaces (walls, door panel, rubber lining)",
        "Basic deodorising of fridge interior", "Cleaning fridge exterior (front and sides only)",
        "Drying surfaces before placing items back", "Replacing food items neatly into the fridge"
      ],
      "excludes": [
        "Moving or lifting the refrigerator", "Cleaning the back panel or condenser coils",
        "Repair or servicing of the fridge", "Handling frozen items requiring defrosting beyond service time",
        "Cleaning deep stains caused by long-term neglect", "Use of special chemicals or deodorising products",
        "Organizing food by diet, expiry system, or labelling", "Disposal of garbage outside the home",
        "Deep freezer cleaning is not included in the service", "Service may be paused if scope exceeds inclusions",
        "Meat will not be handled by our professional due to hygiene conditions"
      ],
      "requiresCustomerEquipment": False, "isActive": True
    },
    {
      "id": "packing-and-unpacking", "title": "Packing And Unpacking", "price": 125, "duration": "30 mins - 1 hr",
      "includes": [
        "Packing or unpacking clothes, shoes, books, toys, and linens", "Packing or unpacking kitchen items and dry groceries",
        "Folding and organising items before packing", "Placing items into boxes, suitcases, or cupboards",
        "Labelling boxes (room-wise / item-wise)", "Light dusting or surface wipe before placing items",
        "Basic organisation using existing storage"
      ],
      "excludes": [
        "Heavy lifting or moving furniture", "Carrying boxes up or down stairs",
        "Handling jewellery, cash, documents, or valuables", "Packing fragile antiques or artwork",
        "Furniture dismantling or assembly", "Tools, packing materials, boxes, or tapes",
        "Decluttering advice or space planning", "Electrical, plumbing, or carpentry work",
        "Transporting items outside your home"
      ],
      "requiresCustomerEquipment": False, "isActive": True
    },
    {
      "id": "utensils", "title": "Utensils", "price": 125, "duration": "30 mins - 1 hr",
      "includes": [
        "Washing utensils with customer-provided supplies", "Drying and placing utensils in rack",
        "Cleaning the sink and surrounding area after completion"
      ],
      "excludes": [
        "Cleaning other kitchen areas (slabs, tiles, etc.)", "Taking out kitchen garbage or waste disposal",
        "Deep cleaning of burnt or heavily stained utensils"
      ],
      "requiresCustomerEquipment": False, "isActive": True
    },
    {
      "id": "kitchen-preparation", "title": "Kitchen Preparation", "price": 125, "duration": "30 mins - 1 hr",
      "includes": [
        "Washing and peeling vegetables", "Chopping vegetables as per customer instruction",
        "Kneading dough using customer-provided flour and water", "Sorting prepared items into bowls/containers",
        "Basic cleaning of the cutting area after preparation"
      ],
      "excludes": [
        "Cooking or full meal preparation", "Washing large quantities of utensils or full kitchen cleaning",
        "Grinding or food processing using appliances", "Cutting meat or frozen items",
        "Preparing decorative/restaurant-style cuts", "Arranging food inside refrigerator or kitchen storage"
      ],
      "requiresCustomerEquipment": False, "isActive": True
    },
    {
      "id": "dusting-and-wiping", "title": "Dusting And Wiping", "price": 125, "duration": "30 mins - 1 hr",
      "includes": [
        "Dry dusting of furniture surfaces and shelves", "Dusting of corners and reachable surfaces",
        "Dusting of light fixtures (bulbs and tube lights – exterior only)", "Dusting of electrical switches and plug points",
        "Minor bed adjustment to dust underneath (if easily movable)"
      ],
      "excludes": [
        "Dusting of ceiling fans", "Cleaning of windows or window sills",
        "Dusting in balcony or terrace areas", "Wet cleaning of furniture or electrical items",
        "Moving heavy furniture or appliances"
      ],
      "requiresCustomerEquipment": False, "isActive": True
    },
    {
      "id": "sweeping-and-mopping", "title": "Sweeping And Mopping", "price": 125, "duration": "30 mins - 1 hr",
      "includes": [
        "Sweeping and mopping floors in selected rooms", "Removing dust and loose dirt",
        "Moving light items (like chairs) for cleaning access"
      ],
      "excludes": [
        "Balcony or outdoor cleaning", "Deep cleaning / stain removal / polishing",
        "Moving heavy furniture (beds, cupboards)", "Carpet or rug vacuum cleaning"
      ],
      "requiresCustomerEquipment": False, "isActive": True
    },
    {
      "id": "pre-party-express-clean", "title": "Pre-party Express Clean", "price": 375, "duration": "90 mins",
      "includes": [
        "Living room & dining cleaning", "Kitchen surface cleaning",
        "Bathroom cleaning", "Full house sweeping & mopping",
        "Trash removal", "Basic utensil cleaning"
      ],
      "excludes": [
        "Upholstery / appliance interiors / chimneys / balcony exteriors", "Heavy grease or deep stain cleaning",
        "Construction debris or bulk waste removal", "Extra work beyond 90 minutes"
      ],
      "requiresCustomerEquipment": False, "isActive": True
    },
    {
      "id": "complete-wardrobe", "title": "Complete Wardrobe", "price": 750, "duration": "180 mins",
      "includes": [
        "Service duration is 180 mins", "Interior wardrobe cleaning",
        "Emptying and rearranging clothes", "Cleaning handles & edges",
        "Dry dusting of shelves and surfaces"
      ],
      "excludes": [
        "Washing or cleaning clothes", "Ironing",
        "Polishing wardrobe surface", "Moving heavy furniture/appliances"
      ],
      "requiresCustomerEquipment": False, "isActive": True
    },
    {
      "id": "after-party-express-clean", "title": "After-party Express Clean", "price": 375, "duration": "90 mins",
      "includes": [
        "90 mins service time", "Floor & spill cleanup",
        "Trash + bottle disposal", "Kitchen reset (counter, sink, stove top, utensils)",
        "Bathroom clean", "Living room tidy", "Full house floor sweeping & mopping"
      ],
      "excludes": [
        "Vomit cleaning, upholstery/appliance interiors, chimneys, or balcony exteriors",
        "Heavy grease or stains cleaning, removal of construction debris, and bulk waste",
        "Tasks outside the defined package scope and work beyond the booked time"
      ],
      "requiresCustomerEquipment": False, "isActive": True
    },
    {
      "id": "ironing-and-folding", "title": "Ironing And Folding", "price": 125, "duration": "30 mins - 1 hr",
      "includes": [
        "Ironing of daily wear clothes such as shirts/t-shirts/trousers and similar garments",
        "Neat folding of ironed clothes after completion"
      ],
      "excludes": [
        "Steam Ironing", "Blazers or coat sarees",
        "Party wear or delicate designer garments", "Bedsheets or curtains",
        "Washing or hand-washing of clothes", "Drying clothes (sun-dry or indoor drying)",
        "Arranging clothes inside wardrobe or cupboards", "Dirty clothes will not be pressed"
      ],
      "requiresCustomerEquipment": False, "isActive": True
    },
    {
      "id": "windows-cleaning", "title": "Windows Cleaning", "price": 125, "duration": "30 mins - 1 hr",
      "includes": [
        "Surface dust removal from window mesh/screens", "Wiping window sills if accessible from inside",
        "Light cleaning of interior window tracks/sliding channels"
      ],
      "excludes": [
        "Exterior window glass outside cleaning", "Cleaning of any other surfaces (walls/furniture/balcony)",
        "Balcony/outside window access", "Removal of old stains/paint marks or hard deposits",
        "Deep scrubbing of tracks or grooves"
      ],
      "requiresCustomerEquipment": False, "isActive": True
    },
    {
      "id": "laundry", "title": "Laundry", "price": 125, "duration": "30 mins - 1 hr",
      "includes": [
        "Washing clothes using the customer’s washing machine", "Adding detergent in the correct compartment",
        "Selecting appropriate wash mode based on fabric type", "Hanging washed clothes for drying"
      ],
      "excludes": [
        "Hand-washing of delicate garments", "Ironing or folding clothes",
        "Arranging clothes inside wardrobes", "Stain treatment or special garment care",
        "Washing machine cleaning or repair"
      ],
      "requiresCustomerEquipment": False, "isActive": True
    },
    {
      "id": "kitchen-cleaning", "title": "Kitchen Cleaning", "price": 150, "duration": "30 mins - 1 hr",
      "includes": [
        "Wiping and cleaning kitchen countertops or slabs", "Cleaning exterior surfaces of kitchen cabinets (top and bottom)",
        "Cleaning exterior surfaces of the cooking stove (burners/knobs/drip trays)", "Wiping visible kitchen wall tiles",
        "Cleaning exterior of the sink"
      ],
      "excludes": [
        "Washing or soaking utensils and dishes", "Rearranging or storing utensils inside cabinets",
        "Taking out kitchen garbage or waste", "Cleaning interiors of appliances such as chimneys/microwaves/refrigerators/ovens or air fryers"
      ],
      "requiresCustomerEquipment": False, "isActive": True
    },
    {
      "id": "balcony", "title": "Balcony", "price": 125, "duration": "30 mins - 1 hr",
      "includes": [
        "Sweeping and mopping of balcony floor", "Cleaning and wiping of balcony railings/grills",
        "Cleaning and wiping of balcony parapet/parapet wall", "Dusting of accessible balcony surfaces (tables/chairs - if light and reachable)"
      ],
      "excludes": [
        "Cleaning of balcony walls or ceiling", "Watering plants or gardening/plant care",
        "Cleaning terrace/roof areas or exterior building walls", "Moving heavy furniture or large plant pots"
      ],
      "requiresCustomerEquipment": False, "isActive": True
    },
    {
      "id": "fan-cleaning", "title": "Fan Cleaning", "price": 125, "duration": "30 mins - 1 hr",
      "includes": [
        "Dust removal from fan blades and motor body (exterior only)", "Wiping of fan blades and accessible parts",
        "Cleaning of fallen dust from floor and surrounding area"
      ],
      "excludes": [
        "Cleaning of other room surfaces, furniture, or walls", "Professional will not be carrying a ladder, please provide one",
        "Cleaning fans that require unsafe access or unstable ladder setup", "Disassembly of fan or motor cleaning",
        "Deep cleaning of internal fan parts", "Cleaning of exhaust/pedestal or table fans",
        "Moving heavy furniture to reach the fan"
      ],
      "requiresCustomerEquipment": True, "equipmentTitle": "Ladder Required", "equipmentDesc": "Please ensure a safe, stable ladder is available at home before the appointment.", "confirmText": "I confirm I have a safe and stable ladder available at home.", "isActive": True
    },
    {
      "id": "kitchen-cabinet", "title": "Kitchen Cabinet", "price": 750, "duration": "180 mins",
      "includes": [
        "Service duration is 180 mins", "Interior cleaning",
        "Dry and wet wipe", "Emptying & rearranging cabinet stuff",
        "Exterior cleaning"
      ],
      "excludes": [
        "Deep oil or grease removal", "Washing of utensils or food items",
        "Cabinet repair or repainting", "Cement stains, rust stains, hard water stain"
      ],
      "requiresCustomerEquipment": False, "isActive": True
    }
]

import re

# Update service-detail.html SERVICES constant
html_path = "/Users/apple/Varun/snappito/frontend/service-detail.html"
with open(html_path, 'r') as f:
    html = f.read()

# Replace the SERVICES = [ ... ]; block
services_json = json.dumps(services, indent=4)
new_services_js = f"const SERVICES = {services_json};\n"

start_idx = html.find("const SERVICES = [")
end_idx = html.find("  // ─── Theme Persistence (Anti-Flicker) ───────────────────────")

if start_idx != -1 and end_idx != -1:
    html = html[:start_idx] + new_services_js + "  // " + html[end_idx:]

# Ensure new Footer & CSS changes are incorporated in the HTML
html = re.sub(
    r'<footer class="footer-section".*?</footer>', 
    '''<footer id="contact" style="background-color: #064e3b; color: white; padding: 80px 20px 40px; text-align: center; margin-top: 40px;">
  <div style="display: flex; gap: 16px; justify-content: center; flex-wrap: wrap; margin-bottom: 20px;">
    <a href="tel:8747858018" style="text-decoration:none; display: inline-flex; align-items: center; gap: 8px; background: #ffffff; color: #064e3b; padding: 12px 24px; border-radius: 50px; font-weight: 700;">
      <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"></path></svg>
      Call: 87478 58018
    </a>
    <a href="https://wa.me/918747858018" target="_blank" style="text-decoration:none; display: inline-flex; align-items: center; gap: 8px; background: #ffffff; color: #064e3b; padding: 12px 24px; border-radius: 50px; font-weight: 700;">
      💬 WhatsApp
    </a>
  </div>
  <p style="margin-top: 40px; padding-top: 24px; border-top: 1px solid rgba(255,255,255,0.1); color: rgba(255,255,255,0.6); font-size: 14px;">© 2026 Snappito. All rights reserved.</p>
</footer>''', 
    html,
    flags=re.DOTALL
)

# Replace dark mode lines
html = re.sub(
    r'\s+body\.dark-mode.*?(/\* ─── Reset ──────────────────────────────────────────────────── \*/)',
    r'\n    \1',
    html,
    flags=re.DOTALL
)

# Background styling update inside body {
html = re.sub(
    r'(body\s*{\s*font-family:\s*\'Inter\',\s*sans-serif;\s*color:\s*var\(--text-main\);\s*background:\s*)var\(--bg-color\);(.*?)}',
    r'\1linear-gradient(135deg, #e6fdf2 0%, #ffffff 40%, #ffffff 100%);\2}',
    html,
    flags=re.DOTALL
)

with open(html_path, 'w') as f:
    f.write(html)

print("Updated service-detail.html!")
