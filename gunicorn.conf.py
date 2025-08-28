# Gunicorn configuration for cost-effective production deployment
# Optimized for $30-40/month VPS with 10k+ concurrent users

import multiprocessing
import os

# Server socket
bind = "0.0.0.0:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1  # Optimal for most VPS
worker_class = "gevent"  # Async workers for better concurrency
worker_connections = 1000  # High connection limit
max_requests = 1000  # Restart workers periodically
max_requests_jitter = 100  # Add randomness to restarts

# Timeouts
timeout = 30
keepalive = 2
graceful_timeout = 30

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "kids-practice-pdf"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Performance
preload_app = True
sendfile = True

# Environment
raw_env = [
    "FLASK_ENV=production",
    "FLASK_DEBUG=0"
]

# SSL (if using Cloudflare)
forwarded_allow_ips = "*"

# Memory optimization
max_requests_jitter = 50
worker_tmp_dir = "/dev/shm"  # Use RAM for temporary files

# Health check
check_config = True
