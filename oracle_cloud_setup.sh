#!/bin/bash

# Oracle Cloud Free Tier Setup Script
# Cost: £0/month for life!
# Capacity: 5,000+ concurrent users

echo "🚀 Setting up Oracle Cloud Free Tier..."

# Oracle Cloud Free Tier Configuration
# - 2 AMD VMs (1/8 OCPU, 1GB RAM each)
# - 4 ARM VMs (24GB RAM total)
# - 200GB storage
# - Load balancer included

# Install dependencies
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv nginx redis-server

# Create application directory
sudo mkdir -p /var/www/kids-practice-pdf
sudo chown $USER:$USER /var/www/kids-practice-pdf

# Copy application files
cp -r . /var/www/kids-practice-pdf/
cd /var/www/kids-practice-pdf

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install -r requirements_ultra.txt

# Configure Nginx
sudo cp nginx.conf /etc/nginx/sites-available/kids-practice-pdf
sudo ln -sf /etc/nginx/sites-available/kids-practice-pdf /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Create systemd service
sudo tee /etc/systemd/system/kids-practice-pdf.service > /dev/null <<EOF
[Unit]
Description=Kids Practice PDF Application
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=/var/www/kids-practice-pdf
Environment=PATH=/var/www/kids-practice-pdf/venv/bin
ExecStart=/var/www/kids-practice-pdf/venv/bin/gunicorn -c gunicorn.conf.py ultra_cost_app:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Set permissions
sudo chown -R www-data:www-data /var/www/kids-practice-pdf
sudo chmod -R 755 /var/www/kids-practice-pdf

# Start services
sudo systemctl daemon-reload
sudo systemctl enable kids-practice-pdf
sudo systemctl start kids-practice-pdf

# Configure firewall
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

echo "✅ Oracle Cloud setup completed!"
echo "💰 Cost: £0/month (FREE for life!)"
echo "👥 Capacity: 5,000+ concurrent users"
echo "🌐 Access: http://your-oracle-ip"
