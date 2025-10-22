# Healthcare Patient Analytics Platform - Deployment Guide

##  Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Local Development Setup](#local-development-setup)
4. [Production Deployment](#production-deployment)
5. [Cloud Deployment](#cloud-deployment)
6. [Docker Deployment](#docker-deployment)
7. [Kubernetes Deployment](#kubernetes-deployment)
8. [Environment Configuration](#environment-configuration)
9. [Security Configuration](#security-configuration)
10. [Monitoring Setup](#monitoring-setup)
11. [Backup and Recovery](#backup-and-recovery)
12. [Troubleshooting](#troubleshooting)

##  Overview

This deployment guide provides comprehensive instructions for deploying the Healthcare Patient Analytics Platform in various environments, from local development to production cloud deployments.

### Deployment Options

1. **Local Development**: Single-machine setup for development
2. **Production Server**: Dedicated server deployment
3. **Cloud Deployment**: AWS, Azure, GCP deployment
4. **Container Deployment**: Docker and Kubernetes
5. **Serverless Deployment**: Serverless cloud functions

##  Prerequisites

### System Requirements

#### Minimum Requirements
- **CPU**: 2 cores
- **RAM**: 4 GB
- **Storage**: 20 GB
- **OS**: Linux, macOS, or Windows
- **Python**: 3.12+
- **Git**: Latest version

#### Recommended Requirements
- **CPU**: 4+ cores
- **RAM**: 8+ GB
- **Storage**: 100+ GB SSD
- **OS**: Ubuntu 20.04+ or CentOS 8+
- **Python**: 3.12+
- **Git**: Latest version

### Software Dependencies

#### Core Dependencies
- **Python 3.12+**: Primary runtime
- **Git**: Version control
- **Docker**: Containerization (optional)
- **Kubernetes**: Container orchestration (optional)

#### Python Dependencies
- **FastAPI**: Web framework
- **Streamlit**: Dashboard framework
- **Pandas**: Data processing
- **NumPy**: Numerical computing
- **Scikit-learn**: Machine learning
- **Plotly**: Visualization
- **SQLAlchemy**: Database ORM
- **Snowflake-connector-python**: Snowflake integration

##  Local Development Setup

### Step 1: Clone Repository

```bash
# Clone the repository
git clone https://github.com/joelmichaelx/healthcare-patient-analytics.git
cd healthcare-patient-analytics

# Checkout the latest version
git checkout main
```

### Step 2: Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/macOS:
source venv/bin/activate
# On Windows:
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Install development dependencies
pip install -r requirements-dev.txt

# Install monitoring dependencies
pip install -r requirements-monitoring.txt
```

### Step 4: Initialize Database

```bash
# Create and populate database
python populate_data.py

# Create optimized database for Streamlit
python create_streamlit_optimized_db.py
```

### Step 5: Start Services

```bash
# Start main dashboard
streamlit run dashboards/healthcare_streamlit_app.py --server.port 8501

# Start ML dashboard (in new terminal)
streamlit run dashboards/healthcare_ml_dashboard.py --server.port 8503

# Start streaming dashboard (in new terminal)
streamlit run dashboards/healthcare_streaming_dashboard.py --server.port 8504

# Start HIPAA dashboard (in new terminal)
streamlit run dashboards/healthcare_hipaa_dashboard.py --server.port 8505

# Start monitoring dashboard (in new terminal)
streamlit run dashboards/healthcare_monitoring_dashboard.py --server.port 8506

# Start API server (in new terminal)
python src/api/healthcare_api.py
```

### Step 6: Verify Installation

```bash
# Test the installation
python test_monitoring.py

# Check API health
curl http://localhost:8000/health

# Check dashboard access
# Open browser and navigate to:
# http://localhost:8501 - Main dashboard
# http://localhost:8503 - ML dashboard
# http://localhost:8504 - Streaming dashboard
# http://localhost:8505 - HIPAA dashboard
# http://localhost:8506 - Monitoring dashboard
```

##  Production Deployment

### Step 1: Server Preparation

#### Ubuntu/Debian Setup
```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.12
sudo apt install python3.12 python3.12-venv python3.12-dev -y

# Install system dependencies
sudo apt install git nginx supervisor -y

# Install database dependencies
sudo apt install sqlite3 postgresql-client -y
```

#### CentOS/RHEL Setup
```bash
# Update system
sudo yum update -y

# Install Python 3.12
sudo yum install python3.12 python3.12-venv python3.12-devel -y

# Install system dependencies
sudo yum install git nginx supervisor -y

# Install database dependencies
sudo yum install sqlite postgresql-client -y
```

### Step 2: Application Deployment

```bash
# Create application directory
sudo mkdir -p /opt/healthcare-analytics
sudo chown $USER:$USER /opt/healthcare-analytics

# Clone repository
cd /opt/healthcare-analytics
git clone https://github.com/joelmichaelx/healthcare-patient-analytics.git .

# Create virtual environment
python3.12 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-monitoring.txt

# Initialize database
python populate_data.py
python create_streamlit_optimized_db.py
```

### Step 3: Configure Services

#### Nginx Configuration
```nginx
# /etc/nginx/sites-available/healthcare-analytics
server {
    listen 80;
    server_name your-domain.com;

    # Main dashboard
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # ML dashboard
    location /ml {
        proxy_pass http://localhost:8503;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Streaming dashboard
    location /streaming {
        proxy_pass http://localhost:8504;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # HIPAA dashboard
    location /hipaa {
        proxy_pass http://localhost:8505;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Monitoring dashboard
    location /monitoring {
        proxy_pass http://localhost:8506;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### Supervisor Configuration
```ini
# /etc/supervisor/conf.d/healthcare-analytics.conf
[program:healthcare-main]
command=/opt/healthcare-analytics/venv/bin/streamlit run dashboards/healthcare_streamlit_app.py --server.port 8501 --server.headless true
directory=/opt/healthcare-analytics
user=healthcare
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/healthcare-analytics/main.log

[program:healthcare-ml]
command=/opt/healthcare-analytics/venv/bin/streamlit run dashboards/healthcare_ml_dashboard.py --server.port 8503 --server.headless true
directory=/opt/healthcare-analytics
user=healthcare
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/healthcare-analytics/ml.log

[program:healthcare-streaming]
command=/opt/healthcare-analytics/venv/bin/streamlit run dashboards/healthcare_streaming_dashboard.py --server.port 8504 --server.headless true
directory=/opt/healthcare-analytics
user=healthcare
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/healthcare-analytics/streaming.log

[program:healthcare-hipaa]
command=/opt/healthcare-analytics/venv/bin/streamlit run dashboards/healthcare_hipaa_dashboard.py --server.port 8505 --server.headless true
directory=/opt/healthcare-analytics
user=healthcare
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/healthcare-analytics/hipaa.log

[program:healthcare-monitoring]
command=/opt/healthcare-analytics/venv/bin/streamlit run dashboards/healthcare_monitoring_dashboard.py --server.port 8506 --server.headless true
directory=/opt/healthcare-analytics
user=healthcare
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/healthcare-analytics/monitoring.log

[program:healthcare-api]
command=/opt/healthcare-analytics/venv/bin/python src/api/healthcare_api.py
directory=/opt/healthcare-analytics
user=healthcare
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/healthcare-analytics/api.log
```

### Step 4: Start Services

```bash
# Enable and start services
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start all

# Check status
sudo supervisorctl status

# Enable Nginx
sudo systemctl enable nginx
sudo systemctl start nginx
```

##  Cloud Deployment

### AWS Deployment

#### Step 1: Prepare AWS Environment
```bash
# Install AWS CLI
pip install awscli

# Configure AWS credentials
aws configure
```

#### Step 2: Create EC2 Instance
```bash
# Create EC2 instance
aws ec2 run-instances \
  --image-id ami-0c02fb55956c7d316 \
  --instance-type t3.medium \
  --key-name your-key-pair \
  --security-group-ids sg-12345678 \
  --subnet-id subnet-12345678 \
  --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=healthcare-analytics}]'
```

#### Step 3: Configure Security Groups
```bash
# Create security group
aws ec2 create-security-group \
  --group-name healthcare-analytics-sg \
  --description "Security group for Healthcare Analytics Platform"

# Add inbound rules
aws ec2 authorize-security-group-ingress \
  --group-id sg-12345678 \
  --protocol tcp \
  --port 80 \
  --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-id sg-12345678 \
  --protocol tcp \
  --port 443 \
  --cidr 0.0.0.0/0

aws ec2 authorize-security-group-ingress \
  --group-id sg-12345678 \
  --protocol tcp \
  --port 22 \
  --cidr 0.0.0.0/0
```

#### Step 4: Deploy Application
```bash
# Connect to EC2 instance
ssh -i your-key.pem ec2-user@your-instance-ip

# Install dependencies
sudo yum update -y
sudo yum install python3.12 git nginx -y

# Clone and setup application
git clone https://github.com/joelmichaelx/healthcare-patient-analytics.git
cd healthcare-patient-analytics
python3.12 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Azure Deployment

#### Step 1: Create Resource Group
```bash
# Create resource group
az group create --name healthcare-analytics-rg --location eastus
```

#### Step 2: Create Virtual Machine
```bash
# Create VM
az vm create \
  --resource-group healthcare-analytics-rg \
  --name healthcare-analytics-vm \
  --image UbuntuLTS \
  --size Standard_B2s \
  --admin-username azureuser \
  --generate-ssh-keys
```

#### Step 3: Configure Network Security Group
```bash
# Create NSG rule for HTTP
az network nsg rule create \
  --resource-group healthcare-analytics-rg \
  --nsg-name healthcare-analytics-nsg \
  --name AllowHTTP \
  --protocol Tcp \
  --priority 1000 \
  --destination-port-range 80 \
  --access Allow

# Create NSG rule for HTTPS
az network nsg rule create \
  --resource-group healthcare-analytics-rg \
  --nsg-name healthcare-analytics-nsg \
  --name AllowHTTPS \
  --protocol Tcp \
  --priority 1001 \
  --destination-port-range 443 \
  --access Allow
```

### GCP Deployment

#### Step 1: Create Project
```bash
# Create project
gcloud projects create healthcare-analytics-project

# Set project
gcloud config set project healthcare-analytics-project
```

#### Step 2: Create Compute Instance
```bash
# Create instance
gcloud compute instances create healthcare-analytics-vm \
  --zone=us-central1-a \
  --machine-type=e2-medium \
  --image-family=ubuntu-2004-lts \
  --image-project=ubuntu-os-cloud \
  --boot-disk-size=20GB \
  --boot-disk-type=pd-standard
```

#### Step 3: Configure Firewall
```bash
# Create firewall rule
gcloud compute firewall-rules create allow-http \
  --allow tcp:80 \
  --source-ranges 0.0.0.0/0

gcloud compute firewall-rules create allow-https \
  --allow tcp:443 \
  --source-ranges 0.0.0.0/0
```

##  Docker Deployment

### Step 1: Create Dockerfile

```dockerfile
# Dockerfile
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    git \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .
COPY requirements-monitoring.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements-monitoring.txt

# Copy application code
COPY . .

# Create non-root user
RUN useradd -m -u 1000 healthcare && chown -R healthcare:healthcare /app
USER healthcare

# Expose ports
EXPOSE 8000 8501 8503 8504 8505 8506

# Start services
CMD ["python", "start_all_services.py"]
```

### Step 2: Create Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  healthcare-main:
    build: .
    ports:
      - "8501:8501"
    command: streamlit run dashboards/healthcare_streamlit_app.py --server.port 8501 --server.headless true
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:///data/healthcare_data.db

  healthcare-ml:
    build: .
    ports:
      - "8503:8503"
    command: streamlit run dashboards/healthcare_ml_dashboard.py --server.port 8503 --server.headless true
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:///data/healthcare_data.db

  healthcare-streaming:
    build: .
    ports:
      - "8504:8504"
    command: streamlit run dashboards/healthcare_streaming_dashboard.py --server.port 8504 --server.headless true
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:///data/healthcare_data.db

  healthcare-hipaa:
    build: .
    ports:
      - "8505:8505"
    command: streamlit run dashboards/healthcare_hipaa_dashboard.py --server.port 8505 --server.headless true
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:///data/healthcare_data.db

  healthcare-monitoring:
    build: .
    ports:
      - "8506:8506"
    command: streamlit run dashboards/healthcare_monitoring_dashboard.py --server.port 8506 --server.headless true
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:///data/healthcare_data.db

  healthcare-api:
    build: .
    ports:
      - "8000:8000"
    command: python src/api/healthcare_api.py
    volumes:
      - ./data:/app/data
    environment:
      - DATABASE_URL=sqlite:///data/healthcare_data.db

  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - healthcare-main
      - healthcare-ml
      - healthcare-streaming
      - healthcare-hipaa
      - healthcare-monitoring
      - healthcare-api
```

### Step 3: Deploy with Docker

```bash
# Build and start services
docker-compose up -d

# Check status
docker-compose ps

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

##  Kubernetes Deployment

### Step 1: Create Kubernetes Manifests

```yaml
# k8s/namespace.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: healthcare-analytics
```

```yaml
# k8s/configmap.yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: healthcare-config
  namespace: healthcare-analytics
data:
  DATABASE_URL: "sqlite:///data/healthcare_data.db"
  API_TOKEN: "your-api-token"
```

```yaml
# k8s/deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: healthcare-main
  namespace: healthcare-analytics
spec:
  replicas: 1
  selector:
    matchLabels:
      app: healthcare-main
  template:
    metadata:
      labels:
        app: healthcare-main
    spec:
      containers:
      - name: healthcare-main
        image: healthcare-analytics:latest
        ports:
        - containerPort: 8501
        env:
        - name: DATABASE_URL
          valueFrom:
            configMapKeyRef:
              name: healthcare-config
              key: DATABASE_URL
        command: ["streamlit", "run", "dashboards/healthcare_streamlit_app.py", "--server.port", "8501", "--server.headless", "true"]
```

```yaml
# k8s/service.yaml
apiVersion: v1
kind: Service
metadata:
  name: healthcare-main-service
  namespace: healthcare-analytics
spec:
  selector:
    app: healthcare-main
  ports:
  - port: 8501
    targetPort: 8501
  type: LoadBalancer
```

```yaml
# k8s/ingress.yaml
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: healthcare-ingress
  namespace: healthcare-analytics
  annotations:
    nginx.ingress.kubernetes.io/rewrite-target: /
spec:
  rules:
  - host: healthcare-analytics.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: healthcare-main-service
            port:
              number: 8501
```

### Step 2: Deploy to Kubernetes

```bash
# Create namespace
kubectl apply -f k8s/namespace.yaml

# Create configmap
kubectl apply -f k8s/configmap.yaml

# Deploy application
kubectl apply -f k8s/deployment.yaml

# Create services
kubectl apply -f k8s/service.yaml

# Create ingress
kubectl apply -f k8s/ingress.yaml

# Check status
kubectl get pods -n healthcare-analytics
kubectl get services -n healthcare-analytics
kubectl get ingress -n healthcare-analytics
```

##  Environment Configuration

### Environment Variables

```bash
# Database configuration
DATABASE_URL=sqlite:///healthcare_data.db
SNOWFLAKE_ACCOUNT=your-account
SNOWFLAKE_USER=your-user
SNOWFLAKE_PASSWORD=your-password
SNOWFLAKE_WAREHOUSE=your-warehouse
SNOWFLAKE_DATABASE=your-database

# API configuration
HEALTHCARE_API_TOKEN=your-api-token
SECRET_KEY=your-secret-key
CORS_ORIGINS=http://localhost:8501,http://localhost:8503

# Monitoring configuration
MONITORING_ENABLED=true
ALERT_EMAIL=admin@healthcare.com
SLACK_WEBHOOK_URL=your-slack-webhook
WEBHOOK_URL=your-webhook-url

# Security configuration
ENCRYPTION_KEY=your-encryption-key
JWT_SECRET=your-jwt-secret
SESSION_SECRET=your-session-secret
```

### Configuration Files

#### .env File
```bash
# .env
DATABASE_URL=sqlite:///healthcare_data.db
HEALTHCARE_API_TOKEN=healthcare-api-token
SECRET_KEY=your-secret-key
MONITORING_ENABLED=true
```

#### config.yaml
```yaml
# config.yaml
database:
  url: "sqlite:///healthcare_data.db"
  pool_size: 10
  max_overflow: 20

api:
  token: "healthcare-api-token"
  secret_key: "your-secret-key"
  cors_origins:
    - "http://localhost:8501"
    - "http://localhost:8503"

monitoring:
  enabled: true
  alert_email: "admin@healthcare.com"
  slack_webhook: "your-slack-webhook"
  webhook_url: "your-webhook-url"

security:
  encryption_key: "your-encryption-key"
  jwt_secret: "your-jwt-secret"
  session_secret: "your-session-secret"
```

##  Security Configuration

### SSL/TLS Configuration

#### Nginx SSL Configuration
```nginx
# /etc/nginx/sites-available/healthcare-analytics-ssl
server {
    listen 443 ssl http2;
    server_name your-domain.com;

    ssl_certificate /etc/ssl/certs/healthcare-analytics.crt;
    ssl_certificate_key /etc/ssl/private/healthcare-analytics.key;
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES256-GCM-SHA512:DHE-RSA-AES256-GCM-SHA512:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES256-GCM-SHA384;
    ssl_prefer_server_ciphers off;
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;

    # Security headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
    add_header X-Content-Type-Options nosniff;
    add_header X-Frame-Options DENY;
    add_header X-XSS-Protection "1; mode=block";

    # Dashboard configurations
    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### Firewall Configuration

#### UFW Configuration
```bash
# Enable UFW
sudo ufw enable

# Allow SSH
sudo ufw allow 22/tcp

# Allow HTTP
sudo ufw allow 80/tcp

# Allow HTTPS
sudo ufw allow 443/tcp

# Allow specific IPs for admin access
sudo ufw allow from 192.168.1.0/24 to any port 22
```

#### iptables Configuration
```bash
# Allow loopback
iptables -A INPUT -i lo -j ACCEPT

# Allow established connections
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow SSH
iptables -A INPUT -p tcp --dport 22 -j ACCEPT

# Allow HTTP
iptables -A INPUT -p tcp --dport 80 -j ACCEPT

# Allow HTTPS
iptables -A INPUT -p tcp --dport 443 -j ACCEPT

# Drop all other traffic
iptables -A INPUT -j DROP
```

### Access Control

#### User Management
```bash
# Create healthcare user
sudo useradd -m -s /bin/bash healthcare
sudo usermod -aG sudo healthcare

# Set up SSH keys
sudo mkdir -p /home/healthcare/.ssh
sudo cp /home/ubuntu/.ssh/authorized_keys /home/healthcare/.ssh/
sudo chown -R healthcare:healthcare /home/healthcare/.ssh
sudo chmod 700 /home/healthcare/.ssh
sudo chmod 600 /home/healthcare/.ssh/authorized_keys
```

#### File Permissions
```bash
# Set proper permissions
sudo chown -R healthcare:healthcare /opt/healthcare-analytics
sudo chmod -R 755 /opt/healthcare-analytics
sudo chmod 600 /opt/healthcare-analytics/.env
sudo chmod 600 /opt/healthcare-analytics/config.yaml
```

##  Monitoring Setup

### System Monitoring

#### Install Monitoring Tools
```bash
# Install monitoring tools
sudo apt install htop iotop nethogs -y

# Install log monitoring
sudo apt install logrotate -y
```

#### Configure Log Rotation
```bash
# /etc/logrotate.d/healthcare-analytics
/var/log/healthcare-analytics/*.log {
    daily
    missingok
    rotate 30
    compress
    delaycompress
    notifempty
    create 644 healthcare healthcare
    postrotate
        supervisorctl restart healthcare-main
        supervisorctl restart healthcare-ml
        supervisorctl restart healthcare-streaming
        supervisorctl restart healthcare-hipaa
        supervisorctl restart healthcare-monitoring
        supervisorctl restart healthcare-api
    endscript
}
```

### Application Monitoring

#### Health Checks
```bash
# Create health check script
cat > /opt/healthcare-analytics/health_check.sh << 'EOF'
#!/bin/bash

# Check if services are running
check_service() {
    local service=$1
    local port=$2
    
    if curl -f http://localhost:$port/health > /dev/null 2>&1; then
        echo " $service is healthy"
        return 0
    else
        echo " $service is unhealthy"
        return 1
    fi
}

# Check all services
check_service "Main Dashboard" 8501
check_service "ML Dashboard" 8503
check_service "Streaming Dashboard" 8504
check_service "HIPAA Dashboard" 8505
check_service "Monitoring Dashboard" 8506
check_service "API" 8000

# Check database
if [ -f "/opt/healthcare-analytics/healthcare_data.db" ]; then
    echo " Database exists"
else
    echo " Database missing"
fi
EOF

chmod +x /opt/healthcare-analytics/health_check.sh
```

#### Monitoring Script
```bash
# Create monitoring script
cat > /opt/healthcare-analytics/monitor.sh << 'EOF'
#!/bin/bash

# Monitor system resources
monitor_resources() {
    echo "=== System Resources ==="
    echo "CPU Usage: $(top -bn1 | grep "Cpu(s)" | awk '{print $2}' | cut -d'%' -f1)%"
    echo "Memory Usage: $(free | grep Mem | awk '{printf "%.2f%%", $3/$2 * 100.0}')"
    echo "Disk Usage: $(df -h / | awk 'NR==2{printf "%s", $5}')"
    echo "Load Average: $(uptime | awk -F'load average:' '{print $2}')"
}

# Monitor application status
monitor_applications() {
    echo "=== Application Status ==="
    supervisorctl status
}

# Monitor logs
monitor_logs() {
    echo "=== Recent Errors ==="
    tail -n 20 /var/log/healthcare-analytics/*.log | grep -i error
}

# Run monitoring
monitor_resources
monitor_applications
monitor_logs
EOF

chmod +x /opt/healthcare-analytics/monitor.sh
```

##  Backup and Recovery

### Database Backup

#### Automated Backup Script
```bash
# Create backup script
cat > /opt/healthcare-analytics/backup.sh << 'EOF'
#!/bin/bash

BACKUP_DIR="/opt/healthcare-analytics/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="healthcare_backup_$DATE.db"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup database
cp /opt/healthcare-analytics/healthcare_data.db $BACKUP_DIR/$BACKUP_FILE

# Compress backup
gzip $BACKUP_DIR/$BACKUP_FILE

# Remove old backups (keep last 30 days)
find $BACKUP_DIR -name "healthcare_backup_*.db.gz" -mtime +30 -delete

echo "Backup completed: $BACKUP_FILE.gz"
EOF

chmod +x /opt/healthcare-analytics/backup.sh
```

#### Cron Job for Backups
```bash
# Add to crontab
echo "0 2 * * * /opt/healthcare-analytics/backup.sh" | crontab -u healthcare -
```

### Application Backup

#### Full Application Backup
```bash
# Create application backup script
cat > /opt/healthcare-analytics/app_backup.sh << 'EOF'
#!/bin/bash

BACKUP_DIR="/opt/healthcare-analytics/backups"
DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_FILE="healthcare_app_backup_$DATE.tar.gz"

# Create backup directory
mkdir -p $BACKUP_DIR

# Backup application
tar -czf $BACKUP_DIR/$BACKUP_FILE \
    --exclude='venv' \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='.git' \
    /opt/healthcare-analytics

# Remove old backups (keep last 7 days)
find $BACKUP_DIR -name "healthcare_app_backup_*.tar.gz" -mtime +7 -delete

echo "Application backup completed: $BACKUP_FILE"
EOF

chmod +x /opt/healthcare-analytics/app_backup.sh
```

### Recovery Procedures

#### Database Recovery
```bash
# Stop services
sudo supervisorctl stop all

# Restore database
cp /opt/healthcare-analytics/backups/healthcare_backup_YYYYMMDD_HHMMSS.db.gz /tmp/
gunzip /tmp/healthcare_backup_YYYYMMDD_HHMMSS.db.gz
cp /tmp/healthcare_backup_YYYYMMDD_HHMMSS.db /opt/healthcare-analytics/healthcare_data.db

# Start services
sudo supervisorctl start all
```

#### Application Recovery
```bash
# Stop services
sudo supervisorctl stop all

# Restore application
tar -xzf /opt/healthcare-analytics/backups/healthcare_app_backup_YYYYMMDD_HHMMSS.tar.gz -C /

# Reinstall dependencies
cd /opt/healthcare-analytics
source venv/bin/activate
pip install -r requirements.txt

# Start services
sudo supervisorctl start all
```

##  Troubleshooting

### Common Issues

#### Service Not Starting
```bash
# Check service status
sudo supervisorctl status

# Check logs
sudo supervisorctl tail healthcare-main
sudo supervisorctl tail healthcare-ml

# Restart service
sudo supervisorctl restart healthcare-main
```

#### Database Issues
```bash
# Check database file
ls -la /opt/healthcare-analytics/healthcare_data.db

# Check database integrity
sqlite3 /opt/healthcare-analytics/healthcare_data.db "PRAGMA integrity_check;"

# Recreate database
cd /opt/healthcare-analytics
source venv/bin/activate
python populate_data.py
```

#### Port Conflicts
```bash
# Check port usage
netstat -tlnp | grep :8501
netstat -tlnp | grep :8503
netstat -tlnp | grep :8504
netstat -tlnp | grep :8505
netstat -tlnp | grep :8506
netstat -tlnp | grep :8000

# Kill processes on ports
sudo fuser -k 8501/tcp
sudo fuser -k 8503/tcp
sudo fuser -k 8504/tcp
sudo fuser -k 8505/tcp
sudo fuser -k 8506/tcp
sudo fuser -k 8000/tcp
```

#### Permission Issues
```bash
# Fix ownership
sudo chown -R healthcare:healthcare /opt/healthcare-analytics

# Fix permissions
sudo chmod -R 755 /opt/healthcare-analytics
sudo chmod 600 /opt/healthcare-analytics/.env
sudo chmod 600 /opt/healthcare-analytics/config.yaml
```

### Log Analysis

#### View Logs
```bash
# View all logs
sudo tail -f /var/log/healthcare-analytics/*.log

# View specific service logs
sudo tail -f /var/log/healthcare-analytics/main.log
sudo tail -f /var/log/healthcare-analytics/ml.log
sudo tail -f /var/log/healthcare-analytics/streaming.log
sudo tail -f /var/log/healthcare-analytics/hipaa.log
sudo tail -f /var/log/healthcare-analytics/monitoring.log
sudo tail -f /var/log/healthcare-analytics/api.log
```

#### Error Analysis
```bash
# Search for errors
grep -i error /var/log/healthcare-analytics/*.log

# Search for warnings
grep -i warning /var/log/healthcare-analytics/*.log

# Search for specific errors
grep -i "database" /var/log/healthcare-analytics/*.log
grep -i "connection" /var/log/healthcare-analytics/*.log
```

### Performance Issues

#### Resource Monitoring
```bash
# Monitor CPU usage
top -bn1 | grep "Cpu(s)"

# Monitor memory usage
free -h

# Monitor disk usage
df -h

# Monitor network usage
iftop
```

#### Application Performance
```bash
# Check response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8501

# Check API performance
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/health
```

---

**This deployment guide provides comprehensive instructions for deploying the Healthcare Patient Analytics Platform in various environments. For additional support or questions, please refer to the contact information above.**
