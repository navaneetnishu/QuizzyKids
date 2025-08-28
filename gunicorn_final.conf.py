# Final Gunicorn Configuration
# Oracle Cloud + Cloudflare R2 + SQLite + GitHub Backup
# Optimized for £0-£2/month infrastructure

import multiprocessing
import os

# Server socket
bind = "127.0.0.1:8000"
backlog = 2048

# Worker processes
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
preload_app = True

# Timeouts
timeout = 30
keepalive = 2
graceful_timeout = 30

# Logging
accesslog = "/var/log/gunicorn/access.log"
errorlog = "/var/log/gunicorn/error.log"
loglevel = "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(D)s'

# Process naming
proc_name = "kids-practice-pdf"

# User/Group
user = "www-data"
group = "www-data"

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Performance
worker_tmp_dir = "/dev/shm"
forwarded_allow_ips = "*"

# SSL (if using Let's Encrypt)
# keyfile = "/etc/ssl/private/yourdomain.com.key"
# certfile = "/etc/ssl/certs/yourdomain.com.crt"

# Environment variables
raw_env = [
    "FLASK_ENV=production",
    "FLASK_APP=final_app.py"
]

# Pre-fork hooks
def on_starting(server):
    """Called just after the server is started"""
    server.log.info("Kids Practice PDF Server Starting...")

def on_reload(server):
    """Called to reload the server"""
    server.log.info("Kids Practice PDF Server Reloading...")

def worker_int(worker):
    """Called just after a worker has been initialized"""
    worker.log.info("Worker %s initialized", worker.pid)

def pre_fork(server, worker):
    """Called just before a worker has been forked"""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_fork(server, worker):
    """Called just after a worker has been forked"""
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def post_worker_init(worker):
    """Called just after a worker has initialized the application"""
    worker.log.info("Worker initialized (pid: %s)", worker.pid)

def worker_abort(worker):
    """Called when a worker received SIGABRT signal"""
    worker.log.info("Worker aborted (pid: %s)", worker.pid)

def pre_exec(server):
    """Called just before a new master process is forked"""
    server.log.info("Forked child, re-executing.")

def when_ready(server):
    """Called just after the server is started"""
    server.log.info("Server is ready. Spawning workers")

def worker_exit(server, worker):
    """Called when a worker exits"""
    server.log.info("Worker exited (pid: %s)", worker.pid)

def on_exit(server):
    """Called just before exiting"""
    server.log.info("Server exiting...")

# Create log directory
os.makedirs("/var/log/gunicorn", exist_ok=True)
