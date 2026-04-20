#!/bin/bash

# =================================================================
# Snappito Production AWS Setup Script
# =================================================================

set -e # Exit on any error

echo "🚀 Starting Automated Production Deployment..."

# 1. System Updates & Dependencies
echo "📦 Installing system packages..."
sudo apt-get update -y
sudo apt-get install -y python3-pip python3-venv nginx git libpq-dev

# 2. Project Directory Setup
# We assume this script is run from the root of the cloned repo
PROJECT_ROOT=$(pwd)
echo "📍 Project Root detected at: $PROJECT_ROOT"

# 3. Frontend Deployment
echo "🌐 Deploying frontend to /var/www/snappito..."
sudo mkdir -p /var/www/snappito
sudo cp -r index.html login.html signup.html dashboard.html booking.html service-detail.html admin.html config.js index.css src/ /var/www/snappito/
sudo chown -R www-data:www-data /var/www/snappito

# 4. Backend Environment Setup (venv)
echo "🐍 Setting up Python Virtual Environment..."
cd $PROJECT_ROOT/backend
python3 -m venv venv
source venv/bin/activate

echo "📥 Installing Production Dependencies..."
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn psycopg2-binary
deactivate

# 5. Application Service (Systemd)
echo "⚙️ Configuring Systemd Background Service..."
# Update the service file with the actual path if it differs
sudo cp $PROJECT_ROOT/deployment/snappito-backend.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable snappito-backend
sudo systemctl restart snappito-backend

# 6. Web Server (Nginx) Configuration
echo "🔗 Linking Nginx configuration..."
sudo cp $PROJECT_ROOT/deployment/snappito.conf /etc/nginx/sites-available/snappito
sudo ln -sf /etc/nginx/sites-available/snappito /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

echo "🛡️ Checking Nginx config and restarting..."
sudo nginx -t
sudo systemctl restart nginx

echo "================================================================="
echo "✅ DEPLOYMENT SETUP COMPLETE!"
echo "================================================================="
echo "NEXT STEPS:"
echo "1. Go to RDS Security Groups and allow EC2 to Port 5432."
echo "2. Edit $PROJECT_ROOT/backend/.env with your RDS credentials."
echo "3. Run 'sudo systemctl restart snappito-backend' after editing .env."
echo "================================================================="
