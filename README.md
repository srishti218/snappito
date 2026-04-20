# Snappito Project

A premium home services booking platform with a Python Flask backend and a modern Vanilla JS frontend.

## 🚀 Getting Started

This project is optimized for both **macOS** and **Ubuntu**. Note that the ports and URL configurations are standardized to avoid platform conflicts.

### 1. Prerequisites
- Python 3.10+
- pip (Python package manager)

---

### 2. Backend Setup (`Port 5001`)

**Why Port 5001?** 
On macOS Monterey and later, Port 5000 is reserved for local system services (AirPlay). To ensure the app runs on both Mac and Ubuntu without errors, we use **5001** globally.

```bash
cd backend
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure Database
# IMPORTANT: Ensure the DATABASE_URL in backend/.env points to your local absolute path.
# Example (Ubuntu): DATABASE_URL=sqlite:////home/varun/snappito/backend/dev.db

# 3. Start the server
python3 backend.py
```

---

### 3. Frontend Setup (`Port 8000`)

We use a custom `start_server.py` helper in the root directory.

**Why use `start_server.py`?**
- **Clean URLs**: it allows you to access pages without `.html` extensions (e.g., `/dashboard` instead of `/dashboard.html`).
- **Standardization**: Ensures the frontend always looks for the backend on the correct port (5001).

```bash
# From the project root
python3 start_server.py
```
*Access the app at: [http://localhost:8000](http://localhost:8000)*

---

### 📂 Key Directory structure
- `/` (Root): Frontend HTML pages and `start_server.py`.
- `/src`: Modular JavaScript logic, components, and services.
- `/backend`: Flask API, environment configuration, and SQLite database.

### 🧪 Test Credentials
| Role | Email | Password |
| :--- | :--- | :--- |
| **Admin** | `admin@snappito.com` | *[Provided in private]* |
| **Professional** | `pro@snappito.com` | `pro-password-2026` |
| **User** | `test@example.com` | `password123` |


