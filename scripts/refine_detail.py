import json
import re

html_path = "/Users/apple/Varun/snappito/frontend/service-detail.html"
with open(html_path, 'r') as f:
    html = f.read()

# 1. Define the updated SERVICES data with tiers
services = [
    {
      "id": "bathroom-cleaning", "title": "Bathroom Cleaning",
      "tiers": [{"name": "Express", "duration": "30 mins", "price": 150}, {"name": "Standard", "duration": "1 hr", "price": 300}],
      "includes": ["Cleaning of toilet bowl", "Cleaning of washbasin and faucet", "Wiping bathroom tiles", "Cleaning taps and fixtures", "Sweeping and mopping floor", "Final wipe-down and deodorising"],
      "excludes": ["Deep cleaning (grout scrubbing)", "Removal of heavy mold", "Use of acid chemicals", "Cleaning mirrors/storage", "Cleaning shower curtains", "Shifting heavy items"],
    },
    {
      "id": "fridge-cleaning", "title": "Fridge Cleaning",
      "tiers": [{"name": "Express", "duration": "45 mins", "price": 150}, {"name": "Standard", "duration": "1 hr", "price": 250}],
      "includes": ["Clean one refrigerator unit", "Remove food items safely", "Discard expired items", "Clean shelves and trays", "Wipe interior surfaces", "Basic deodorising", "Clean exterior", "Drying surfaces"],
      "excludes": ["Moving refrigerator", "Cleaning back panel/coils", "Repair or servicing", "Handling frozen items", "Deep stain cleaning", "Special chemicals", "Organizing by diet", "Deep freezer cleaning"],
    },
    {
      "id": "packing-and-unpacking", "title": "Packing And Unpacking",
      "tiers": [{"name": "Express", "duration": "30 mins", "price": 125}, {"name": "Standard", "duration": "1 hr", "price": 250}],
      "includes": ["Packing clothes/books/toys", "Packing kitchen items", "Folding and organising", "Placing into boxes", "Labelling boxes", "Light dusting", "Basic organisation"],
      "excludes": ["Heavy lifting", "Carrying boxes up stairs", "Handling valuables", "Packing fragile antiques", "Furniture dismantling", "Providing packing materials", "Electrical/plumbing work"],
    },
    {
      "id": "utensils", "title": "Utensils",
      "tiers": [{"name": "Express", "duration": "30 mins", "price": 125}, {"name": "Standard", "duration": "1 hr", "price": 250}],
      "includes": ["Washing utensils", "Drying and placing in rack", "Cleaning sink area"],
      "excludes": ["Cleaning other kitchen areas", "Taking out garbage", "Deep cleaning burnt utensils"],
    },
    {
      "id": "kitchen-preparation", "title": "Kitchen Preparation",
      "tiers": [{"name": "Express", "duration": "30 mins", "price": 125}, {"name": "Standard", "duration": "1 hr", "price": 250}],
      "includes": ["Washing/peeling vegetables", "Chopping vegetables", "Kneading dough", "Sorting into containers", "Basic cleaning of area"],
      "excludes": ["Cooking or full meal prep", "Washing large quantities", "Food processing", "Cutting meat", "Preparing decorative cuts"],
    },
    {
      "id": "dusting-and-wiping", "title": "Dusting And Wiping",
      "tiers": [{"name": "Express", "duration": "30 mins", "price": 125}, {"name": "Standard", "duration": "1 hr", "price": 250}],
      "includes": ["Dry dusting furniture", "Dusting corners", "Dusting light fixtures", "Dusting electrical switches", "Minor bed adjustment"],
      "excludes": ["Dusting ceiling fans", "Cleaning windows", "Balcony dusting", "Wet cleaning", "Moving heavy furniture"],
    },
    {
      "id": "sweeping-and-mopping", "title": "Sweeping And Mopping",
      "tiers": [{"name": "Express", "duration": "30 mins", "price": 125}, {"name": "Standard", "duration": "1 hr", "price": 250}],
      "includes": ["Sweeping and mopping floors", "Removing dust/dirt", "Moving light items"],
      "excludes": ["Balcony/outdoor cleaning", "Deep cleaning/polishing", "Moving heavy furniture", "Carpet vacuuming"],
    },
    {
      "id": "pre-party-express-clean", "title": "Pre-party Express Clean",
      "tiers": [{"name": "Basic", "duration": "90 mins", "price": 375}],
      "includes": ["Living room & dining", "Kitchen surfaces", "Bathroom cleaning", "Full house sweep/mop", "Trash removal", "Basic utensils"],
      "excludes": ["Upholstery/interior appliances", "Heavy grease", "Construction debris", "Extra work beyond 90m"],
    },
    {
      "id": "complete-wardrobe", "title": "Complete Wardrobe",
      "tiers": [{"name": "Standard", "duration": "180 mins", "price": 750}],
      "includes": ["Interior wardrobe cleaning", "Emptying and rearranging", "Cleaning handles & edges", "Dry dusting shelves"],
      "excludes": ["Washing clothes", "Ironing", "Polishing surface", "Moving heavy furniture"],
    },
    {
      "id": "after-party-express-clean", "title": "After-party Express Clean",
      "tiers": [{"name": "Basic", "duration": "90 mins", "price": 375}],
      "includes": ["Floor & spill cleanup", "Trash + bottle disposal", "Kitchen reset", "Bathroom clean", "Living room tidy", "Full house sweep/mop"],
      "excludes": ["Vomit cleaning", "Heavy grease", "Tasks outside scope"],
    },
    {
      "id": "ironing-and-folding", "title": "Ironing And Folding",
      "tiers": [{"name": "Express", "duration": "30 mins", "price": 125}, {"name": "Standard", "duration": "1 hr", "price": 250}],
      "includes": ["Ironing daily wear", "Neat folding"],
      "excludes": ["Steam Ironing", "Blazers/coats", "Party wear", "Hand-washing", "Arranging inside wardrobe"],
    },
    {
      "id": "windows-cleaning", "title": "Windows Cleaning",
      "tiers": [{"name": "Express", "duration": "30 mins", "price": 125}, {"name": "Standard", "duration": "1 hr", "price": 250}],
      "includes": ["Dust from mesh", "Wiping window sills", "Cleaning interior tracks"],
      "excludes": ["Exterior glass cleaning", "Balcony access", "Removal of old stains", "Deep scrubbing"],
    },
    {
      "id": "laundry", "title": "Laundry",
      "tiers": [{"name": "Express", "duration": "30 mins", "price": 125}, {"name": "Standard", "duration": "1 hr", "price": 250}],
      "includes": ["Washing using machine", "Adding detergent", "Selecting wash mode", "Hanging for drying"],
      "excludes": ["Hand-washing", "Ironing or folding", "Stain treatment", "Machine cleaning/repair"],
    },
    {
      "id": "kitchen-cleaning", "title": "Kitchen Cleaning",
      "tiers": [{"name": "Express", "duration": "30 mins", "price": 150}, {"name": "Standard", "duration": "1 hr", "price": 300}],
      "includes": ["Countertops/slabs", "Cabinet exteriors", "Stove exterior", "Wall tiles", "Exterior of sink"],
      "excludes": ["Washing utensils", "Rearranging contents", "Taking out garbage", "Appliance interiors"],
    },
    {
      "id": "balcony", "title": "Balcony",
      "tiers": [{"name": "Express", "duration": "30 mins", "price": 125}, {"name": "Standard", "duration": "1 hr", "price": 250}],
      "includes": ["Sweep and mop floor", "Railings and grills", "Parapet wall", "Dusting light furniture"],
      "excludes": ["Cleaning walls/ceiling", "Watering plants", "Terrace areas", "Moving heavy pots"],
    },
    {
      "id": "fan-cleaning", "title": "Fan Cleaning",
      "tiers": [{"name": "Express", "duration": "30 mins", "price": 125}, {"name": "Standard", "duration": "1 hr", "price": 250}],
      "includes": ["Dust from blades/motor", "Wiping blades", "Cleaning floor area"],
      "excludes": ["Other room surfaces", "Ladder not provided", "Internal parts", "Moving furniture"],
      "requiresCustomerEquipment": True, "equipmentTitle": "Ladder Required", "equipmentDesc": "Please provide a safe ladder.", "confirmText": "I have a ladder."
    },
    {
      "id": "kitchen-cabinet", "title": "Kitchen Cabinet",
      "tiers": [{"name": "Standard", "duration": "180 mins", "price": 750}],
      "includes": ["Interior cleaning", "Dry/wet wipe", "Emptying/rearranging", "Exterior cleaning"],
      "excludes": ["Deep oil/grease", "Washing utensils", "Repair/repainting", "Hard stains"],
    }
]

# 2. Re-replace the script section
script_start = html.find("const SERVICES = [")
script_end = html.find("  // ─── Booking ───────────────────────────────────────────────────")

if script_start != -1 and script_end != -1:
    new_script = f"""const SERVICES = {json.dumps(services, indent=4)};

  let currentService = null;
  let currentTier = null;
  let equipmentConfirmed = false;

  const heroTitle      = document.getElementById('hero-title');
  const heroImg        = document.getElementById('hero-img').querySelector('img');
  const heroPrice      = document.getElementById('hero-price');
  const heroDuration   = document.getElementById('hero-duration');
  const includesList   = document.getElementById('includes-list');
  const excludesList   = document.getElementById('excludes-list');
  const tierContainer  = document.getElementById('tier-selector-container');
  
  const equipmentAlert = document.getElementById('equipment-alert');
  const equipmentTitle = document.getElementById('equipment-title');
  const equipmentDesc  = document.getElementById('equipment-desc');
  const confirmBlock   = document.getElementById('confirm-block');
  const confirmText    = document.getElementById('confirm-text');
  const heroBookBtn    = document.getElementById('hero-book-btn');
  const ladderConfirm  = document.getElementById('ladder-confirm');

  const SERVICE_IMAGES = {{
    "bathroom-cleaning": "assets/premium/bathroom.png",
    "fridge-cleaning": "https://images.unsplash.com/photo-1584622781564-1d9876a13d00?auto=format&fit=crop&q=80&w=1200",
    "kitchen-cleaning": "assets/premium/kitchen.png",
    "fan-cleaning": "assets/premium/fan.png",
    "windows-cleaning": "assets/premium/window.png",
    "laundry": "assets/premium/laundry.png",
    "utensils": "assets/premium/dishwashing.png",
    "sweeping-and-mopping": "assets/premium/sweeping-mopping.png",
    "default": "https://images.unsplash.com/photo-1581578731548-c64695cc6954?auto=format&fit=crop&q=80&w=1200"
  }};

  ladderConfirm.addEventListener('change', () => {{
    equipmentConfirmed = ladderConfirm.checked;
    confirmBlock.classList.toggle('checked', equipmentConfirmed);
    updateBookBtn();
  }});

  function updateBookBtn() {{
    if (!currentService || !currentTier) {{ heroBookBtn.disabled = true; return; }}
    const needsConfirm = currentService.requiresCustomerEquipment;
    const isDisabled   = needsConfirm && !equipmentConfirmed;
    heroBookBtn.disabled = isDisabled;
    if (isDisabled) {{
      heroBookBtn.classList.remove('active');
      heroBookBtn.style.background = '#ccc';
    }} else {{
      heroBookBtn.classList.add('active');
      heroBookBtn.style.background = '#ffb74d';
    }}
  }}

  function selectTier(index) {{
    currentTier = currentService.tiers[index];
    document.querySelectorAll('.tier-btn').forEach((btn, i) => {{
        btn.classList.toggle('active', i === index);
    }});
    heroPrice.innerHTML = `₹${{currentTier.price.toLocaleString('en-IN')}}`;
    heroDuration.textContent = currentTier.duration;
    updateBookBtn();
  }}

  function renderService(service) {{
    currentService = service;
    equipmentConfirmed = false;
    ladderConfirm.checked = false;

    heroTitle.textContent = service.title;
    const targetImg = SERVICE_IMAGES[service.id] || SERVICE_IMAGES.default;
    heroImg.src = targetImg;
    
    // Tiers
    tierContainer.innerHTML = service.tiers.map((t, index) => `
        <button class="tier-btn" onclick="selectTier(${{index}})">
            <span class="t-name">${{t.name}}</span>
            <span class="t-desc">${{t.duration}}</span>
        </button>
    `).join('');
    
    // Auto select standard (index 1) if available, otherwise 0
    const startIdx = service.tiers.length > 1 ? 1 : 0;
    selectTier(startIdx);

    // Includes (Green Check)
    includesList.innerHTML = service.includes.map(item => `
      <div class="list-item">
        <span style="color: #064e3b; font-weight: bold; margin-right: 8px;">✔</span>
        <span>${{escHtml(item)}}</span>
      </div>
    `).join('');

    // Excludes (Red/Gray Cross)
    excludesList.innerHTML = service.excludes.map(item => `
      <div class="list-item">
        <span style="color: #ef4444; font-weight: bold; margin-right: 8px; font-size: 14px;">✘</span>
        <span style="color: #6b7280;">${{escHtml(item)}}</span>
      </div>
    `).join('');

    const hasEquip = service.requiresCustomerEquipment;
    equipmentAlert.classList.toggle('hidden', !hasEquip);
    confirmBlock.classList.toggle('hidden', !hasEquip);
    
    if (hasEquip) {{
      equipmentTitle.textContent = service.equipmentTitle || "Ladder Required";
      equipmentDesc.textContent  = service.equipmentDesc  || "Professional doesn't carry a ladder.";
      confirmText.textContent    = service.confirmText    || "I have a ladder.";
    }}
    window.scrollTo({{ top: 0, behavior: 'auto' }});
  }}

  function handleBook() {{
    if (!currentService || !currentTier) return;
    const params = new URLSearchParams({{
      service_id: currentService.id,
      service:    currentService.title,
      tier:       currentTier.name,
      price:      currentTier.price,
      duration:   currentTier.duration
    }});
    window.location.href = `/booking?${{params.toString()}}`;
  }}
"""
    html = html[:script_start] + new_script + "  " + html[script_end:]

with open(html_path, 'w') as f:
    f.write(html)
