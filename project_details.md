# Snappito Project Context & History

This document serves as a comprehensive briefing for any AI assistant or developer joining the Snappito project. It summarizes the project's purpose, technical evolution, and current state.

## 🚀 Project Overview
**Snappito** is a premium, high-fidelity home service aggregation platform. It allows users to book professional cleaning (bathroom, kitchen, fridge), organization (wardrobe, packing), and maintenance (fans, windows) services through a streamlined Single Page Application (SPA) dashboard.

---

## 🛠 Technical Stack
- **Frontend**: Vanilla HTML5, CSS3 (Modern UI with Glassmorphism), and Modular JavaScript (ES6).
- **Backend**: Python Flask (v3.0+) with RESTful API architecture.
- **Database**: SQLite (local dev) using SQLAlchemy ORM.
- **Authentication**: JWT-based (Flask-JWT-Extended) with PBKDF2:SHA256 password hashing.
- **Integrations**: Razorpay (Placeholder/API ready), Indian Postal Pincode API for auto-fill.

---

## 📂 Repository Structure (Post-Refactor)
The project follows a "Root-Entry / Modular-Source" architecture for maximum simplicity and reliable pathing:
- **`/` (Root)**: Core entry points (`index.html`, `dashboard.html`, `booking.html`, `login.html`, `signup.html`).
- **`src/app/`**: Orchestration logic for each page (e.g., `Dashboard.js`, `Home.js`).
- **`src/features/`**: Feature-specific logic (e.g., `catalog/`, `booking/`).
- **`src/services/`**: API abstraction layers (`apiClient.js`, `authService.js`, `walletService.js`).
- **`src/assets/`**: Images and static assets.
- **`backend/`**: Flask application, migrations, and the active `dev.db` SQLite file.

---

## 📜 Development History (Major Milestones)

### 1. Authentication Stabilization
- **Problem**: Incompatibility with `hashlib.scrypt` on certain OS versions and missing DOM IDs in login forms.
- **Fix**: Standardized on `pbkdf2:sha256` hashing and corrected ID selectors in the frontend to ensure stable login/signup.

### 2. Dashboard SPA Navigation
- **Problem**: Browser caching and module-loading race conditions caused sidebars to fail when switching sections (Bookings vs Addresses).
- **Fix**: Implemented a "Blunt Force" inline `switchSection` function in `dashboard.html` that manually toggles visibility via `display: none/block`.

### 3. Service Catalog Synchronization
- **Problem**: Incomplete or missing service details.
- **Fix**: Overhauled `serviceData.js` and `backend/seed_script.py` to match the 17-service "Master Table" provided by the user. Added dynamic "Include/Exclude" lists and pricing tiers.

### 4. Pincode Auto-Fill
- **Feature**: Integrated the Indian Postal Pincode API in the address modal. Typing a 6-digit pincode now automatically populates the **City** and **State** fields.

### 5. Repository Cleanup
- **Action**: Removed legacy `frontend/` folders, empty `src/` subdirectories, and redundant `dev.db` files. Consolidated all entry points to the root for better deployment reliability.

---

## 📍 Current Status & "To-Do"
- [x] **Authentication**: Fully functional and stable.
- [x] **Catalog**: Complete, matches business requirements.
- [x] **Dashboard**: Reliable navigation between Overview, Bookings, and Address management.
- [x] **Checkout**: Integration with `booking.html` is ready.
- [ ] **Payments**: Razorpay logic is in place (placeholders) but requires live API credentials for production.
- [ ] **Professional App**: Future scope includes a separate dashboard for service providers.

---

## 💡 Quick Tips for the Next AI
1. **Database Location**: Always use the absolute path to `backend/dev.db` in `.env` to prevent "missing tables" errors.
2. **Navigation Fixes**: NEVER move the `switchSection` function from `dashboard.html` back into a module without handling the caching issue.
3. **Seeding**: If the catalog is empty, run `python3 backend/seed_script.py` after activating the venv in the `backend/` folder.

**Developed with 💚 by Antigravity AI.**
