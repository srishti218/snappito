# Snappito Project

A modern, fast, and secure home services booking platform.

## Project Structure

- **`/backend`**: Python Flask API, database models, and seeding logic.
- **`/frontend`**: The production-ready UI, including HTML, CSS, JavaScript, and assets.
- **`/deployment`**: Infrastructure configuration files (Nginx, etc.).

## Development

### Running the Backend
```bash
cd backend
# Install dependencies
pip install -r requirements.txt
# Start the server
python3 backend.py
```

### Running the Frontend
```bash
cd frontend
# Start the local server with Clean URL support
python3 -c \"import http.server, os; class SmartHandler(http.server.SimpleHTTPRequestHandler): ...\"
```
