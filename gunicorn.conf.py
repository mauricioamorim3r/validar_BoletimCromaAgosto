#!/usr/bin/env python3
"""
Gunicorn configuration for Render deployment
"""
import os

# Server socket
bind = f"0.0.0.0:{os.environ.get('PORT', 10000)}"
backlog = 2048

# Worker processes
workers = 2
worker_class = "sync"
worker_connections = 1000
timeout = 30
keepalive = 2

# Logging
loglevel = "info"
accesslog = "-"
errorlog = "-"

# Process naming
proc_name = "boletins-cromatograficos"

# Application
wsgi_app = "app:app"

# SSL/TLS (if needed)
# keyfile = None
# certfile = None

# Security
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Performance
preload_app = True
max_requests = 1000
max_requests_jitter = 50