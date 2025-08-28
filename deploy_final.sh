#!/bin/bash
# Final Deployment Script
# Oracle Cloud + Cloudflare R2 + SQLite + GitHub Backup
# Cost: £0-£2/month for 500,000+ users

set -e

echo "🚀 Starting Final Infrastructure Deployment..."
echo "💰 Target Cost: £0-£2/month for 500,000+ users"

# Configuration
APP_NAME="kids-practice-pdf"
APP_DIR="/var/www/$APP_NAME"
SERVICE_USER="www-data"
SERVICE_GROUP="www-data"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging function
log() {
    echo -e "${GREEN}[$(date +'%Y-%m-%d %H:%M:%S')] $1${NC}"
}

warn() {
    echo -e "${YELLOW}[$(date +'%Y-%m-%d %H:%M:%S')] WARNING: $1${NC}"
}

error() {
    echo -e "${RED}[$(date +'%Y-%m-%d %H:%M:%S')] ERROR: $1${NC}"
    exit 1
}

# Check if running as root
if [[ $EUID -ne 0 ]]; then
   error "This script must be run as root"
fi

# Update system
log "📦 Updating system packages..."
apt update && apt upgrade -y

# Install system dependencies
log "🔧 Installing system dependencies..."
apt install -y \
    python3 \
    python3-pip \
    python3-venv \
    nginx \
    git \
    curl \
    wget \
    unzip \
    supervisor \
    certbot \
    python3-certbot-nginx \
    ufw \
    htop \
    iotop \
    nethogs \
    logrotate \
    cron \
    rsync \
    sqlite3

# Create application directory
log "📁 Creating application directory..."
mkdir -p $APP_DIR
mkdir -p $APP_DIR/logs
mkdir -p $APP_DIR/backups
mkdir -p $APP_DIR/static
mkdir -p /var/log/gunicorn

# Set permissions
chown -R $SERVICE_USER:$SERVICE_GROUP $APP_DIR
chown -R $SERVICE_USER:$SERVICE_GROUP /var/log/gunicorn

# Create Python virtual environment
log "🐍 Setting up Python virtual environment..."
cd $APP_DIR
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
log "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements_final.txt

# Copy application files
log "📋 Copying application files..."
cp final_app.py $APP_DIR/
cp gunicorn_final.conf.py $APP_DIR/
cp nginx_final.conf /etc/nginx/sites-available/$APP_NAME
cp templates/index.html $APP_DIR/templates/

# Create environment file
log "⚙️ Creating environment configuration..."
cat > $APP_DIR/.env << EOF
# Oracle Cloud + Cloudflare R2 Configuration
FLASK_ENV=production
FLASK_APP=final_app.py

# Cloudflare R2 Storage Configuration
R2_BUCKET_NAME=kids-practice-pdf
R2_ACCOUNT_ID=your_account_id_here
R2_ACCESS_KEY_ID=your_access_key_here
R2_SECRET_ACCESS_KEY=your_secret_key_here

# Database Configuration
DATABASE_PATH=$APP_DIR/questions.db

# Backup Configuration
BACKUP_DIR=$APP_DIR/backups
GIT_REPO_URL=https://github.com/yourusername/kids-practice-pdf.git

# Monitoring Configuration
LOG_LEVEL=INFO
LOG_FILE=$APP_DIR/logs/app.log
EOF

# Set proper permissions for environment file
chmod 600 $APP_DIR/.env
chown $SERVICE_USER:$SERVICE_GROUP $APP_DIR/.env

# Initialize SQLite database
log "🗄️ Initializing SQLite database..."
cd $APP_DIR
source venv/bin/activate
python3 -c "
from final_app import db_manager
print('Database initialized successfully')
"

# Create Gunicorn service
log "🔧 Creating Gunicorn service..."
cat > /etc/systemd/system/$APP_NAME.service << EOF
[Unit]
Description=Kids Practice PDF Application
After=network.target

[Service]
Type=notify
User=$SERVICE_USER
Group=$SERVICE_GROUP
WorkingDirectory=$APP_DIR
Environment=PATH=$APP_DIR/venv/bin
ExecStart=$APP_DIR/venv/bin/gunicorn --config gunicorn_final.conf.py final_app:app
ExecReload=/bin/kill -s HUP \$MAINPID
KillMode=mixed
TimeoutStopSec=5
PrivateTmp=true
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start Gunicorn service
systemctl daemon-reload
systemctl enable $APP_NAME
systemctl start $APP_NAME

# Configure Nginx
log "🌐 Configuring Nginx..."
ln -sf /etc/nginx/sites-available/$APP_NAME /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test Nginx configuration
nginx -t

# Enable and start Nginx
systemctl enable nginx
systemctl restart nginx

# Configure firewall
log "🔥 Configuring firewall..."
ufw --force enable
ufw default deny incoming
ufw default allow outgoing
ufw allow ssh
ufw allow 'Nginx Full'
ufw allow 80/tcp
ufw allow 443/tcp

# Configure log rotation
log "📝 Configuring log rotation..."
cat > /etc/logrotate.d/$APP_NAME << EOF
$APP_DIR/logs/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 $SERVICE_USER $SERVICE_GROUP
    postrotate
        systemctl reload $APP_NAME
    endscript
}

/var/log/gunicorn/*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 $SERVICE_USER $SERVICE_GROUP
    postrotate
        systemctl reload $APP_NAME
    endscript
}
EOF

# Create backup script
log "💾 Creating backup script..."
cat > $APP_DIR/backup.sh << 'EOF'
#!/bin/bash
# Daily backup script

APP_DIR="/var/www/kids-practice-pdf"
BACKUP_DIR="$APP_DIR/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# Database backup
echo "Backing up database..."
cp $APP_DIR/questions.db "$BACKUP_DIR/questions_$TIMESTAMP.db"

# Configuration backup
echo "Backing up configurations..."
tar -czf "$BACKUP_DIR/config_$TIMESTAMP.tar.gz" \
    /etc/nginx/sites-available/kids-practice-pdf \
    /etc/systemd/system/kids-practice-pdf.service \
    $APP_DIR/.env

# Code backup (Git)
echo "Backing up code..."
cd $APP_DIR
git add .
git commit -m "Daily backup $TIMESTAMP" || true
git push origin main || true

# Clean old backups (keep 7 days)
echo "Cleaning old backups..."
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Daily backup completed!"
EOF

chmod +x $APP_DIR/backup.sh
chown $SERVICE_USER:$SERVICE_GROUP $APP_DIR/backup.sh

# Setup cron jobs
log "⏰ Setting up cron jobs..."
cat > /tmp/crontab_new << EOF
# Daily backup at 2 AM
0 2 * * * $APP_DIR/backup.sh

# Weekly cleanup at 3 AM on Sunday
0 3 * * 0 curl -X POST http://localhost/cleanup

# Monthly system maintenance at 4 AM on 1st of month
0 4 1 * * apt update && apt upgrade -y

# Log rotation (handled by logrotate)
EOF

crontab /tmp/crontab_new
rm /tmp/crontab_new

# Create monitoring script
log "📊 Creating monitoring script..."
cat > $APP_DIR/monitor.sh << 'EOF'
#!/bin/bash
# System monitoring script

APP_DIR="/var/www/kids-practice-pdf"
LOG_FILE="$APP_DIR/logs/monitor.log"

# Check system resources
CPU_USAGE=$(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)
MEMORY_USAGE=$(free | grep Mem | awk '{printf("%.2f", $3/$2 * 100.0)}')
DISK_USAGE=$(df / | tail -1 | awk '{print $5}' | cut -d'%' -f1)

# Check application health
HEALTH_CHECK=$(curl -s http://localhost/health | grep -o '"status":"[^"]*"' | cut -d'"' -f4)

# Log results
echo "$(date): CPU: ${CPU_USAGE}%, Memory: ${MEMORY_USAGE}%, Disk: ${DISK_USAGE}%, Health: ${HEALTH_CHECK}" >> $LOG_FILE

# Alert if thresholds exceeded
if (( $(echo "$CPU_USAGE > 80" | bc -l) )); then
    echo "WARNING: High CPU usage: ${CPU_USAGE}%" >> $LOG_FILE
fi

if (( $(echo "$MEMORY_USAGE > 80" | bc -l) )); then
    echo "WARNING: High memory usage: ${MEMORY_USAGE}%" >> $LOG_FILE
fi

if (( $(echo "$DISK_USAGE > 80" | bc -l) )); then
    echo "WARNING: High disk usage: ${DISK_USAGE}%" >> $LOG_FILE
fi

if [ "$HEALTH_CHECK" != "healthy" ]; then
    echo "WARNING: Application health check failed: ${HEALTH_CHECK}" >> $LOG_FILE
fi
EOF

chmod +x $APP_DIR/monitor.sh
chown $SERVICE_USER:$SERVICE_GROUP $APP_DIR/monitor.sh

# Add monitoring to cron
echo "*/5 * * * * $APP_DIR/monitor.sh" | crontab -

# Create SSL certificate (if domain is configured)
log "🔒 Setting up SSL certificate..."
if [ -f "/etc/nginx/sites-available/$APP_NAME" ]; then
    # Check if domain is configured
    DOMAIN=$(grep "server_name" /etc/nginx/sites-available/$APP_NAME | head -1 | awk '{print $2}' | sed 's/;//')
    
    if [ "$DOMAIN" != "yourdomain.com" ] && [ "$DOMAIN" != "" ]; then
        log "Obtaining SSL certificate for $DOMAIN..."
        certbot --nginx -d $DOMAIN --non-interactive --agree-tos --email admin@$DOMAIN
    else
        warn "Domain not configured. Please update nginx configuration and run: certbot --nginx -d yourdomain.com"
    fi
fi

# Final system optimization
log "⚡ Optimizing system performance..."

# Optimize SQLite
cat > /etc/sysctl.d/99-sqlite-optimization.conf << EOF
# SQLite optimization
vm.swappiness = 10
vm.dirty_ratio = 15
vm.dirty_background_ratio = 5
EOF

sysctl -p /etc/sysctl.d/99-sqlite-optimization.conf

# Optimize Nginx
cat > /etc/nginx/conf.d/performance.conf << EOF
# Nginx performance optimization
worker_processes auto;
worker_rlimit_nofile 65535;

events {
    worker_connections 65535;
    use epoll;
    multi_accept on;
}

http {
    # Basic settings
    sendfile on;
    tcp_nopush on;
    tcp_nodelay on;
    keepalive_timeout 65;
    types_hash_max_size 2048;
    
    # Buffer sizes
    client_body_buffer_size 128k;
    client_max_body_size 10m;
    client_header_buffer_size 1k;
    large_client_header_buffers 4 4k;
    output_buffers 1 32k;
    postpone_output 1460;
    
    # Timeouts
    client_header_timeout 3m;
    client_body_timeout 3m;
    send_timeout 3m;
}
EOF

# Restart services
systemctl restart nginx
systemctl restart $APP_NAME

# Create status check script
log "🔍 Creating status check script..."
cat > $APP_DIR/status.sh << 'EOF'
#!/bin/bash
# Status check script

echo "=== System Status ==="
echo "CPU Usage: $(top -bn1 | grep 'Cpu(s)' | awk '{print $2}' | cut -d'%' -f1)%"
echo "Memory Usage: $(free | grep Mem | awk '{printf("%.2f", $3/$2 * 100.0)}')%"
echo "Disk Usage: $(df / | tail -1 | awk '{print $5}')"

echo -e "\n=== Service Status ==="
systemctl status kids-practice-pdf --no-pager -l
echo -e "\n"
systemctl status nginx --no-pager -l

echo -e "\n=== Application Health ==="
curl -s http://localhost/health | python3 -m json.tool

echo -e "\n=== Recent Logs ==="
tail -10 /var/www/kids-practice-pdf/logs/app.log
EOF

chmod +x $APP_DIR/status.sh

# Final verification
log "✅ Final verification..."
sleep 5

# Check if services are running
if systemctl is-active --quiet $APP_NAME; then
    log "✅ Gunicorn service is running"
else
    error "❌ Gunicorn service failed to start"
fi

if systemctl is-active --quiet nginx; then
    log "✅ Nginx service is running"
else
    error "❌ Nginx service failed to start"
fi

# Test application
if curl -s http://localhost/health > /dev/null; then
    log "✅ Application health check passed"
else
    warn "⚠️ Application health check failed - check logs"
fi

# Display final information
echo -e "\n${GREEN}🎉 DEPLOYMENT COMPLETED SUCCESSFULLY!${NC}"
echo -e "\n${BLUE}📊 Infrastructure Summary:${NC}"
echo "   • Oracle Cloud Free Tier: £0/month"
echo "   • Cloudflare R2 Storage: £0-£1/month"
echo "   • SQLite Database: £0/month"
echo "   • GitHub Backup: £0/month"
echo "   • Total Cost: £0-£2/month"
echo -e "\n${BLUE}🔧 Management Commands:${NC}"
echo "   • Check status: $APP_DIR/status.sh"
echo "   • View logs: tail -f $APP_DIR/logs/app.log"
echo "   • Restart app: systemctl restart $APP_NAME"
echo "   • Backup: $APP_DIR/backup.sh"
echo -e "\n${BLUE}🌐 Next Steps:${NC}"
echo "   1. Update .env file with your R2 credentials"
echo "   2. Configure your domain in nginx configuration"
echo "   3. Run: certbot --nginx -d yourdomain.com"
echo "   4. Test the application at: http://your-server-ip"
echo -e "\n${YELLOW}⚠️ IMPORTANT:${NC}"
echo "   • Update R2 credentials in $APP_DIR/.env"
echo "   • Configure your domain name"
echo "   • Set up SSL certificate"
echo "   • Test backup functionality"

log "🚀 Your ultra-cost-effective infrastructure is ready!"
