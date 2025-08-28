#!/bin/bash

# Production deployment script for cost-effective scaling
# Target: $30-40/month with 10k+ concurrent users

set -e

echo "🚀 Deploying Kids Practice PDF to Production..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
APP_NAME="kids-practice-pdf"
APP_DIR="/var/www/$APP_NAME"
SERVICE_NAME="kids-practice-pdf"
DOMAIN="your-domain.com"

# Update system
echo -e "${YELLOW}📦 Updating system packages...${NC}"
sudo apt update && sudo apt upgrade -y

# Install dependencies
echo -e "${YELLOW}📦 Installing system dependencies...${NC}"
sudo apt install -y python3 python3-pip python3-venv nginx redis-server supervisor

# Create application directory
echo -e "${YELLOW}📁 Creating application directory...${NC}"
sudo mkdir -p $APP_DIR
sudo chown $USER:$USER $APP_DIR

# Copy application files
echo -e "${YELLOW}📋 Copying application files...${NC}"
cp -r . $APP_DIR/
cd $APP_DIR

# Create virtual environment
echo -e "${YELLOW}🐍 Setting up Python virtual environment...${NC}"
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
echo -e "${YELLOW}📦 Installing Python dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements_production.txt

# Configure Redis
echo -e "${YELLOW}🔴 Configuring Redis...${NC}"
sudo systemctl enable redis-server
sudo systemctl start redis-server

# Configure Nginx
echo -e "${YELLOW}🌐 Configuring Nginx...${NC}"
sudo cp nginx.conf /etc/nginx/sites-available/$APP_NAME
sudo ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default
sudo nginx -t
sudo systemctl restart nginx

# Create systemd service
echo -e "${YELLOW}⚙️ Creating systemd service...${NC}"
sudo tee /etc/systemd/system/$SERVICE_NAME.service > /dev/null <<EOF
[Unit]
Description=Kids Practice PDF Application
After=network.target

[Service]
Type=exec
User=www-data
Group=www-data
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/gunicorn -c gunicorn.conf.py production_app:app
ExecReload=/bin/kill -s HUP \$MAINPID
Restart=always
RestartSec=3

[Install]
WantedBy=multi-user.target
EOF

# Set permissions
echo -e "${YELLOW}🔐 Setting permissions...${NC}"
sudo chown -R www-data:www-data $APP_DIR
sudo chmod -R 755 $APP_DIR

# Start services
echo -e "${YELLOW}🚀 Starting services...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl start $SERVICE_NAME

# Configure firewall
echo -e "${YELLOW}🔥 Configuring firewall...${NC}"
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw --force enable

# Setup monitoring
echo -e "${YELLOW}📊 Setting up monitoring...${NC}"
sudo apt install -y htop iotop

# Create log rotation
echo -e "${YELLOW}📝 Setting up log rotation...${NC}"
sudo tee /etc/logrotate.d/$SERVICE_NAME > /dev/null <<EOF
$APP_DIR/*.log {
    daily
    missingok
    rotate 7
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
    postrotate
        systemctl reload $SERVICE_NAME
    endscript
}
EOF

# Setup backup script
echo -e "${YELLOW}💾 Setting up backup script...${NC}"
sudo tee /usr/local/bin/backup-$APP_NAME.sh > /dev/null <<EOF
#!/bin/bash
BACKUP_DIR="/var/backups/$APP_NAME"
mkdir -p \$BACKUP_DIR
DATE=\$(date +%Y%m%d_%H%M%S)
tar -czf \$BACKUP_DIR/backup_\$DATE.tar.gz -C $APP_DIR .
find \$BACKUP_DIR -name "backup_*.tar.gz" -mtime +7 -delete
EOF

sudo chmod +x /usr/local/bin/backup-$APP_NAME.sh

# Add to crontab
echo -e "${YELLOW}⏰ Setting up automated backups...${NC}"
(crontab -l 2>/dev/null; echo "0 2 * * * /usr/local/bin/backup-$APP_NAME.sh") | crontab -

# Health check
echo -e "${YELLOW}🏥 Running health check...${NC}"
sleep 5
if curl -f http://localhost/health > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Application is running successfully!${NC}"
else
    echo -e "${RED}❌ Application health check failed${NC}"
    sudo systemctl status $SERVICE_NAME
    exit 1
fi

# Final instructions
echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo -e "${YELLOW}📋 Next steps:${NC}"
echo "1. Update DNS to point $DOMAIN to this server"
echo "2. Configure Cloudflare for CDN and SSL"
echo "3. Set up Backblaze B2 for PDF storage"
echo "4. Configure environment variables"
echo ""
echo -e "${YELLOW}🔗 Useful commands:${NC}"
echo "sudo systemctl status $SERVICE_NAME"
echo "sudo systemctl restart $SERVICE_NAME"
echo "sudo journalctl -u $SERVICE_NAME -f"
echo "sudo nginx -t && sudo systemctl reload nginx"
echo ""
echo -e "${GREEN}💰 Estimated monthly cost: $30-40${NC}"
echo -e "${GREEN}👥 Expected capacity: 10,000+ concurrent users${NC}"
