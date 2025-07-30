# 🚀 VoidSight Analytics - Production Deployment Guide

## 📋 Prerequisites

### System Requirements
- **Python**: 3.8+ 
- **RAM**: 2GB minimum, 4GB recommended
- **Storage**: 10GB minimum
- **CPU**: 2 cores minimum

### Required Services
- **Database**: PostgreSQL 12+ (recommended) or SQLite for small deployments
- **Cache**: Redis 6+ (optional but recommended)
- **Web Server**: Nginx (recommended) or Apache
- **Process Manager**: Gunicorn (included) or uWSGI

---

## 🔧 Quick Production Setup

### Option 1: Docker Deployment (Recommended)

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/voidsight-analytics.git
cd voidsight-analytics

# 2. Copy environment template
cp .env.production .env

# 3. Edit environment variables
nano .env
# Update SECRET_KEY, DATABASE_URL, etc.

# 4. Deploy with Docker
docker-compose -f docker-compose.yml up -d

# 5. Your app is now running at http://localhost
```

### Option 2: Manual Server Setup

```bash
# 1. Clone and setup
git clone https://github.com/yourusername/voidsight-analytics.git
cd voidsight-analytics

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Configure environment
cp .env.production .env
# Edit .env with your settings

# 5. Initialize database (if using PostgreSQL)
python -c "from app import app, db; app.app_context().push(); db.create_all()"

# 6. Run with Gunicorn
gunicorn --bind 0.0.0.0:8000 --workers 4 app:app
```

---

## ⚙️ Environment Configuration

### 1. Copy and edit environment file:
```bash
cp .env.production .env
```

### 2. Required settings to change:

```bash
# Security (Generate new keys!)
SECRET_KEY=your-unique-32-char-secret-key
SECURITY_PASSWORD_SALT=your-unique-16-char-salt

# Database (if using PostgreSQL)
DATABASE_URL=postgresql://username:password@localhost:5432/voidsight

# Email (for notifications)
MAIL_USERNAME=your-email@domain.com
MAIL_PASSWORD=your-app-password
```

### 3. Generate secure keys:
```bash
# Generate SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Generate SECURITY_PASSWORD_SALT  
python -c "import secrets; print(secrets.token_urlsafe(16))"
```

---

## 🐳 Docker Production Deployment

### 1. Docker Compose Setup (Recommended)

```yaml
# docker-compose.prod.yml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:8000"
    environment:
      - FLASK_ENV=production
    env_file:
      - .env
    depends_on:
      - db
      - redis
    restart: unless-stopped

  db:
    image: postgres:14
    environment:
      POSTGRES_DB: voidsight
      POSTGRES_USER: voidsight
      POSTGRES_PASSWORD: your-secure-password
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  redis:
    image: redis:7-alpine
    restart: unless-stopped

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - /etc/letsencrypt:/etc/letsencrypt
    depends_on:
      - web
    restart: unless-stopped

volumes:
  postgres_data:
```

### 2. Deploy:
```bash
docker-compose -f docker-compose.prod.yml up -d
```

---

## 🌐 Nginx Configuration

### Create `/etc/nginx/sites-available/voidsight`:

```nginx
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    location /static/ {
        alias /var/www/voidsight/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
```

### Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/voidsight /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## 🔒 SSL Certificate Setup

### Using Let's Encrypt (Free):

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal (already configured by certbot)
sudo systemctl status certbot.timer
```

---

## 🗄️ Database Setup

### PostgreSQL (Recommended):

```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib

# Create database and user
sudo -u postgres psql
CREATE DATABASE voidsight;
CREATE USER voidsight WITH ENCRYPTED PASSWORD 'your-secure-password';
GRANT ALL PRIVILEGES ON DATABASE voidsight TO voidsight;
\q

# Update .env file
DATABASE_URL=postgresql://voidsight:your-secure-password@localhost:5432/voidsight
```

### Initialize tables:
```bash
python -c "from app import app, db; app.app_context().push(); db.create_all()"
```

---

## 📊 Monitoring & Logging

### 1. Application Logs:
```bash
# Create log directory
sudo mkdir -p /var/log/voidsight
sudo chown $USER:$USER /var/log/voidsight

# Configure in .env
LOG_FILE=/var/log/voidsight/app.log
LOG_LEVEL=WARNING
```

### 2. System Service (Systemd):

Create `/etc/systemd/system/voidsight.service`:

```ini
[Unit]
Description=VoidSight Analytics
After=network.target

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/voidsight
Environment=PATH=/opt/voidsight/venv/bin
ExecStart=/opt/voidsight/venv/bin/gunicorn --bind 127.0.0.1:8000 --workers 4 app:app
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable voidsight
sudo systemctl start voidsight
sudo systemctl status voidsight
```

---

## 🚀 Performance Optimization

### 1. Gunicorn Configuration:

Create `gunicorn.conf.py`:
```python
bind = "127.0.0.1:8000"
workers = 4
worker_class = "gevent"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 120
keepalive = 2
preload_app = True
```

### 2. Redis Caching:
```bash
# Install Redis
sudo apt install redis-server

# Update .env
REDIS_URL=redis://localhost:6379/0
ENABLE_CACHE=True
```

---

## 🔐 Security Checklist

- [ ] **SSL/HTTPS enabled** with valid certificate
- [ ] **DEBUG=False** in production environment
- [ ] **Secure SECRET_KEY** generated and set
- [ ] **Database password** is strong and unique
- [ ] **Firewall configured** (only ports 80, 443, 22 open)
- [ ] **Regular backups** configured
- [ ] **Security headers** enabled in Nginx
- [ ] **Rate limiting** enabled
- [ ] **Log monitoring** set up

---

## 📋 Backup Strategy

### 1. Database Backup:
```bash
# Create backup script
#!/bin/bash
BACKUP_DIR="/opt/backups/voidsight"
DATE=$(date +%Y%m%d_%H%M%S)
pg_dump voidsight > "$BACKUP_DIR/voidsight_$DATE.sql"
gzip "$BACKUP_DIR/voidsight_$DATE.sql"

# Keep only last 30 days
find "$BACKUP_DIR" -name "*.gz" -mtime +30 -delete
```

### 2. Automated Backups:
```bash
# Add to crontab
crontab -e

# Daily backup at 2 AM
0 2 * * * /opt/scripts/backup_voidsight.sh
```

---

## 🆘 Troubleshooting

### Common Issues:

1. **App won't start**:
   ```bash
   # Check logs
   sudo journalctl -u voidsight -f
   
   # Check environment
   cd /opt/voidsight && source venv/bin/activate
   python -c "from config import get_config; print(get_config())"
   ```

2. **Database connection errors**:
   ```bash
   # Test database connection
   psql -h localhost -U voidsight -d voidsight
   
   # Check PostgreSQL status
   sudo systemctl status postgresql
   ```

3. **SSL certificate issues**:
   ```bash
   # Renew certificate
   sudo certbot renew
   
   # Check certificate
   sudo certbot certificates
   ```

---

## 📞 Support

- **Documentation**: [GitHub Wiki](https://github.com/yourusername/voidsight-analytics/wiki)
- **Issues**: [GitHub Issues](https://github.com/yourusername/voidsight-analytics/issues)
- **Email**: support@voidsight.dev

---

## 📈 Scaling for High Traffic

When you outgrow a single server:

1. **Load Balancer**: Multiple app servers behind Nginx/HAProxy
2. **Database**: PostgreSQL with read replicas
3. **Cache**: Redis Cluster or ElastiCache
4. **CDN**: CloudFlare or AWS CloudFront for static assets
5. **Monitoring**: Prometheus + Grafana

**Estimated Capacity**: Single server handles ~1,000 concurrent users with proper optimization.