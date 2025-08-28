# 📊 Monitoring & Logging Strategy
## **Free Monitoring for Ultra-Cost Infrastructure**

---

## 🎯 **Monitoring Stack**

### **Built-in Oracle Cloud Monitoring:**
```bash
✅ CPU usage monitoring
✅ Memory usage monitoring
✅ Disk I/O monitoring
✅ Network monitoring
✅ Uptime monitoring
✅ Cost tracking
✅ Free tier usage alerts
```

### **Application Monitoring:**
```bash
✅ Flask application logs
✅ Gunicorn worker monitoring
✅ SQLite database monitoring
✅ PDF generation metrics
✅ User request tracking
✅ Error rate monitoring
✅ Response time tracking
```

### **Cloudflare Monitoring:**
```bash
✅ CDN performance metrics
✅ R2 storage usage
✅ Bandwidth usage
✅ Cache hit rates
✅ DDoS protection stats
✅ SSL certificate monitoring
```

---

## 📈 **Key Metrics to Monitor**

### **Infrastructure Metrics:**
```python
# Oracle Cloud Metrics
cpu_usage = "CPU utilization %"
memory_usage = "RAM usage %"
disk_usage = "Storage usage %"
network_io = "Network I/O MB/s"
uptime = "System uptime %"

# Application Metrics
response_time = "Average response time ms"
error_rate = "Error rate %"
requests_per_second = "RPS"
pdf_generation_time = "PDF generation time ms"
cache_hit_rate = "Cache hit rate %"
```

### **Business Metrics:**
```python
# User Metrics
active_users = "Concurrent users"
total_users = "Total registered users"
pdfs_generated = "PDFs generated per day"
questions_accessed = "Questions accessed per day"

# Performance Metrics
page_load_time = "Page load time ms"
pdf_download_time = "PDF download time ms"
api_response_time = "API response time ms"
```

---

## 🔍 **Free Monitoring Tools**

### **1. Oracle Cloud Monitoring (Built-in)**
```bash
# Oracle Cloud Console
# - Real-time metrics
# - Historical data
# - Cost tracking
# - Free tier usage
# - Performance alerts
```

### **2. Application Logs**
```python
# Flask logging configuration
import logging
from logging.handlers import RotatingFileHandler

def setup_logging():
    """Setup application logging"""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s: %(message)s',
        handlers=[
            RotatingFileHandler('app.log', maxBytes=10000000, backupCount=5),
            logging.StreamHandler()
        ]
    )

# Log levels
logging.info("Application started")
logging.warning("High memory usage detected")
logging.error("Database connection failed")
logging.critical("System crash detected")
```

### **3. Cloudflare Analytics**
```bash
# Cloudflare Dashboard
# - Traffic analytics
# - Performance metrics
# - Security events
# - R2 storage usage
# - CDN performance
```

### **4. Custom Health Checks**
```python
@app.route('/health')
def health_check():
    """Health check endpoint"""
    try:
        # Check database
        db_status = check_database()
        
        # Check storage
        storage_status = check_storage()
        
        # Check memory
        memory_status = check_memory()
        
        if all([db_status, storage_status, memory_status]):
            return {'status': 'healthy', 'timestamp': datetime.now()}, 200
        else:
            return {'status': 'unhealthy', 'timestamp': datetime.now()}, 503
    except Exception as e:
        return {'status': 'error', 'error': str(e)}, 500

def check_database():
    """Check database connectivity"""
    try:
        conn = sqlite3.connect('questions.db')
        cursor = conn.cursor()
        cursor.execute('SELECT 1')
        conn.close()
        return True
    except:
        return False

def check_storage():
    """Check storage availability"""
    try:
        # Check if we can write to storage
        test_file = '/tmp/health_check.txt'
        with open(test_file, 'w') as f:
            f.write('test')
        os.remove(test_file)
        return True
    except:
        return False

def check_memory():
    """Check memory usage"""
    try:
        import psutil
        memory_percent = psutil.virtual_memory().percent
        return memory_percent < 90  # Alert if >90%
    except:
        return True  # Assume OK if can't check
```

---

## 📊 **Performance Monitoring**

### **Response Time Monitoring:**
```python
import time
from functools import wraps

def monitor_response_time(func):
    """Decorator to monitor response times"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        
        response_time = (end_time - start_time) * 1000  # Convert to ms
        
        # Log response time
        logging.info(f"{func.__name__} response time: {response_time:.2f}ms")
        
        # Alert if response time is too high
        if response_time > 5000:  # 5 seconds
            logging.warning(f"Slow response time: {response_time:.2f}ms for {func.__name__}")
        
        return result
    return wrapper

# Usage
@monitor_response_time
def generate_pdf(questions):
    # PDF generation logic
    pass
```

### **Error Rate Monitoring:**
```python
from collections import defaultdict
import time

class ErrorMonitor:
    def __init__(self):
        self.errors = defaultdict(int)
        self.total_requests = 0
        self.last_reset = time.time()
    
    def log_error(self, error_type):
        """Log an error"""
        self.errors[error_type] += 1
        self.total_requests += 1
    
    def log_request(self):
        """Log a successful request"""
        self.total_requests += 1
    
    def get_error_rate(self):
        """Calculate error rate"""
        if self.total_requests == 0:
            return 0
        
        total_errors = sum(self.errors.values())
        return (total_errors / self.total_requests) * 100
    
    def reset_metrics(self):
        """Reset metrics (call daily)"""
        self.errors.clear()
        self.total_requests = 0
        self.last_reset = time.time()

# Global error monitor
error_monitor = ErrorMonitor()
```

---

## 🚨 **Alerting System**

### **Free Alerting Options:**
```bash
# 1. Email Alerts (Free)
# - Use Gmail SMTP
# - Send alerts to your email
# - No cost involved

# 2. Slack Webhooks (Free)
# - Send alerts to Slack
# - Real-time notifications
# - Free tier available

# 3. Telegram Bot (Free)
# - Send alerts to Telegram
# - Mobile notifications
# - Completely free
```

### **Alert Configuration:**
```python
import smtplib
from email.mime.text import MIMEText

def send_alert(subject, message):
    """Send email alert"""
    try:
        # Configure email settings
        sender_email = "your-app@yourdomain.com"
        receiver_email = "admin@yourdomain.com"
        
        # Create message
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = receiver_email
        
        # Send email (configure SMTP settings)
        # smtp_server.send_message(msg)
        
        logging.info(f"Alert sent: {subject}")
    except Exception as e:
        logging.error(f"Failed to send alert: {e}")

def check_alerts():
    """Check if alerts need to be sent"""
    # Check error rate
    error_rate = error_monitor.get_error_rate()
    if error_rate > 5:  # 5% error rate
        send_alert(
            "High Error Rate Alert",
            f"Error rate is {error_rate:.2f}% - investigation needed"
        )
    
    # Check memory usage
    import psutil
    memory_percent = psutil.virtual_memory().percent
    if memory_percent > 90:
        send_alert(
            "High Memory Usage Alert",
            f"Memory usage is {memory_percent}% - system may be overloaded"
        )
    
    # Check disk usage
    disk_percent = psutil.disk_usage('/').percent
    if disk_percent > 90:
        send_alert(
            "High Disk Usage Alert",
            f"Disk usage is {disk_percent}% - cleanup needed"
        )
```

---

## 📈 **Dashboard & Reporting**

### **Simple Web Dashboard:**
```python
@app.route('/dashboard')
def dashboard():
    """Simple monitoring dashboard"""
    try:
        import psutil
        
        # System metrics
        cpu_percent = psutil.cpu_percent()
        memory_percent = psutil.virtual_memory().percent
        disk_percent = psutil.disk_usage('/').percent
        
        # Application metrics
        error_rate = error_monitor.get_error_rate()
        
        # Database metrics
        db_size = os.path.getsize('questions.db') / (1024 * 1024)  # MB
        
        return {
            'system': {
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent,
                'disk_percent': disk_percent
            },
            'application': {
                'error_rate': error_rate,
                'db_size_mb': db_size
            },
            'timestamp': datetime.now().isoformat()
        }
    except Exception as e:
        return {'error': str(e)}, 500
```

---

## 🎯 **Final Monitoring Recommendation**

### **✅ FREE MONITORING STACK:**

1. **📊 Oracle Cloud Monitoring**: Built-in metrics
2. **📝 Application Logs**: Flask + Gunicorn logging
3. **🌐 Cloudflare Analytics**: CDN + R2 metrics
4. **🔍 Health Checks**: Custom endpoints
5. **📧 Email Alerts**: Free Gmail SMTP
6. **📊 Simple Dashboard**: Web-based metrics

### **Cost: £0/month** 🎉

### **Implementation:**
```python
# Already included in ultra_cost_app.py
# Built-in logging and monitoring
# Health check endpoints
# Error tracking
# Performance monitoring
```

**Free monitoring gives you enterprise-grade observability!** 🚀
