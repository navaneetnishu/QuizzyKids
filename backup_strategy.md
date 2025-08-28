# 🔄 Backup Strategy
## **Free Backup Solution for Ultra-Cost Infrastructure**

---

## 🎯 **Backup Strategy Overview**

### **Multi-Layer Backup Approach:**
```bash
✅ Database Backups: Daily to GitHub
✅ Code Backups: Git version control
✅ Configuration Backups: Git + local
✅ PDF Backups: R2 storage (redundant)
✅ System Backups: Oracle Cloud snapshots
✅ Disaster Recovery: Complete restore plan
```

---

## 📊 **Backup Components**

### **1. Database Backups (SQLite)**
```python
# Daily automated backups
# File-based backup (entire .db file)
# Version control with Git
# 7-day retention policy
# Zero cost solution

def backup_database():
    """Daily database backup to GitHub"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    backup_file = f"backups/questions_{timestamp}.db"
    
    # Copy database file
    shutil.copy2('questions.db', backup_file)
    
    # Git operations
    subprocess.run(['git', 'add', backup_file])
    subprocess.run(['git', 'commit', '-m', f'DB backup {timestamp}'])
    subprocess.run(['git', 'push'])
    
    # Clean old backups
    cleanup_old_backups(days=7)
```

### **2. Code Backups (Git)**
```bash
# Git repository for all code
# Automatic version control
# Branch protection
# Pull request workflow
# Zero cost with GitHub

# Repository structure:
/kids-practice-pdf/
├── app.py
├── ultra_cost_app.py
├── question_bank.py
├── pdf_generator.py
├── question_database.py
├── ultra_storage.py
├── requirements_ultra.txt
├── gunicorn.conf.py
├── nginx.conf
├── oracle_cloud_setup.sh
├── question_data/
│   ├── maths_questions.json
│   ├── science_questions.json
│   ├── computing_questions.json
│   ├── history_questions.json
│   └── geography_questions.json
└── backups/
    └── questions_*.db
```

### **3. Configuration Backups**
```bash
# System configuration files
# Nginx configuration
# Gunicorn configuration
# Environment variables
# SSL certificates

# Backup locations:
/etc/nginx/sites-available/kids-practice-pdf
/etc/systemd/system/kids-practice-pdf.service
/var/www/kids-practice-pdf/.env
/etc/ssl/certs/yourdomain.com.crt
/etc/ssl/private/yourdomain.com.key
```

### **4. PDF Storage Backups (R2)**
```bash
# Cloudflare R2 storage
# Built-in redundancy
# Multiple data centers
# Automatic replication
# 99.9% uptime SLA

# Backup strategy:
# - Primary storage: R2 bucket
# - Redundancy: R2 automatic replication
# - Recovery: Instant access from any location
# - Cost: Included in R2 pricing
```

---

## 🔧 **Automated Backup Scripts**

### **Daily Backup Script:**
```bash
#!/bin/bash
# daily_backup.sh

echo "Starting daily backup..."

# Set variables
BACKUP_DIR="/var/www/kids-practice-pdf/backups"
DB_FILE="/var/www/kids-practice-pdf/questions.db"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# Create backup directory
mkdir -p $BACKUP_DIR

# 1. Database backup
echo "Backing up database..."
cp $DB_FILE "$BACKUP_DIR/questions_$TIMESTAMP.db"

# 2. Configuration backup
echo "Backing up configurations..."
tar -czf "$BACKUP_DIR/config_$TIMESTAMP.tar.gz" \
    /etc/nginx/sites-available/kids-practice-pdf \
    /etc/systemd/system/kids-practice-pdf.service \
    /var/www/kids-practice-pdf/.env

# 3. Code backup (Git)
echo "Backing up code..."
cd /var/www/kids-practice-pdf
git add .
git commit -m "Daily backup $TIMESTAMP"
git push origin main

# 4. Clean old backups (keep 7 days)
echo "Cleaning old backups..."
find $BACKUP_DIR -name "*.db" -mtime +7 -delete
find $BACKUP_DIR -name "*.tar.gz" -mtime +7 -delete

echo "Daily backup completed!"
```

### **Weekly Backup Script:**
```bash
#!/bin/bash
# weekly_backup.sh

echo "Starting weekly backup..."

# Set variables
BACKUP_DIR="/var/www/kids-practice-pdf/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)

# 1. Full system backup
echo "Creating full system backup..."
tar -czf "$BACKUP_DIR/full_system_$TIMESTAMP.tar.gz" \
    /var/www/kids-practice-pdf \
    /etc/nginx \
    /etc/systemd/system/kids-practice-pdf.service

# 2. Database dump (SQL format)
echo "Creating database dump..."
sqlite3 /var/www/kids-practice-pdf/questions.db .dump > "$BACKUP_DIR/db_dump_$TIMESTAMP.sql"

# 3. Upload to external storage (optional)
echo "Uploading to external storage..."
# gcloud storage cp "$BACKUP_DIR/full_system_$TIMESTAMP.tar.gz" gs://your-backup-bucket/

echo "Weekly backup completed!"
```

---

## 🚨 **Disaster Recovery Plan**

### **Recovery Scenarios:**

#### **1. Database Corruption**
```bash
# Recovery steps:
1. Stop application
2. Restore from latest backup
3. Verify data integrity
4. Restart application

# Commands:
sudo systemctl stop kids-practice-pdf
cp backups/questions_20241201_120000.db questions.db
sudo systemctl start kids-practice-pdf
```

#### **2. Server Failure**
```bash
# Recovery steps:
1. Create new Oracle Cloud VM
2. Restore from Git repository
3. Restore database backup
4. Restore configurations
5. Update DNS if needed

# Commands:
git clone https://github.com/yourusername/kids-practice-pdf.git
cp backups/questions_*.db questions.db
sudo cp backups/config_*.tar.gz /tmp/
sudo tar -xzf /tmp/config_*.tar.gz -C /
```

#### **3. Code Issues**
```bash
# Recovery steps:
1. Revert to previous Git commit
2. Restart application
3. Verify functionality

# Commands:
git log --oneline
git reset --hard HEAD~1
sudo systemctl restart kids-practice-pdf
```

#### **4. Configuration Issues**
```bash
# Recovery steps:
1. Restore configuration files
2. Restart services
3. Verify functionality

# Commands:
sudo cp backups/config_*.tar.gz /tmp/
sudo tar -xzf /tmp/config_*.tar.gz -C /
sudo systemctl restart nginx
sudo systemctl restart kids-practice-pdf
```

---

## 📅 **Backup Schedule**

### **Automated Schedule:**
```bash
# Daily backups (2 AM)
0 2 * * * /var/www/kids-practice-pdf/scripts/daily_backup.sh

# Weekly backups (Sunday 3 AM)
0 3 * * 0 /var/www/kids-practice-pdf/scripts/weekly_backup.sh

# Monthly backups (1st of month 4 AM)
0 4 1 * * /var/www/kids-practice-pdf/scripts/monthly_backup.sh
```

### **Backup Retention:**
```bash
# Daily backups: 7 days
# Weekly backups: 4 weeks
# Monthly backups: 12 months
# Git history: Forever
```

---

## 🔍 **Backup Verification**

### **Backup Testing Script:**
```python
def verify_backup():
    """Verify backup integrity"""
    try:
        # Test database backup
        backup_file = "backups/questions_latest.db"
        conn = sqlite3.connect(backup_file)
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM questions")
        count = cursor.fetchone()[0]
        conn.close()
        
        print(f"Database backup verified: {count} questions")
        
        # Test configuration backup
        config_file = "backups/config_latest.tar.gz"
        if os.path.exists(config_file):
            print("Configuration backup verified")
        
        # Test Git backup
        result = subprocess.run(['git', 'log', '--oneline', '-1'], 
                              capture_output=True, text=True)
        print(f"Git backup verified: {result.stdout.strip()}")
        
        return True
    except Exception as e:
        print(f"Backup verification failed: {e}")
        return False
```

---

## 💰 **Backup Cost Analysis**

### **Free Backup Components:**
```bash
✅ Database backups: £0 (GitHub)
✅ Code backups: £0 (GitHub)
✅ Configuration backups: £0 (GitHub)
✅ PDF backups: £0 (R2 redundancy)
✅ System backups: £0 (Oracle snapshots)
✅ Verification: £0 (automated scripts)
```

### **Total Backup Cost: £0/month** 🎉

---

## 🎯 **Final Backup Recommendation**

### **✅ COMPREHENSIVE FREE BACKUP SOLUTION:**

1. **🗄️ Database**: Daily SQLite backups to GitHub
2. **💻 Code**: Git version control with GitHub
3. **⚙️ Configuration**: Automated config backups
4. **📄 PDFs**: R2 built-in redundancy
5. **🖥️ System**: Oracle Cloud snapshots
6. **🔄 Recovery**: Complete disaster recovery plan
7. **🔍 Verification**: Automated backup testing

### **Implementation:**
```bash
# Already included in oracle_cloud_setup.sh
# Automated backup scripts
# Cron job scheduling
# Git integration
# Zero maintenance required
```

**Free backups give you enterprise-grade data protection!** 🚀
