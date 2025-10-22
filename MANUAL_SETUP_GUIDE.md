# Healthcare Patient Analytics - Manual Setup Guide

## Prerequisites

Before starting, ensure you have the following installed on your system:

### Required Software
- **Python 3.9+** - [Download from python.org](https://www.python.org/downloads/)
- **Git** - [Download from git-scm.com](https://git-scm.com/downloads)
- **VS Code or PyCharm** - Recommended IDE
- **Docker** (Optional) - For containerized deployment

### Required Accounts
- **GitHub Account** - For version control and deployment
- **Streamlit Cloud Account** - For dashboard deployment
- **Snowflake Account** (Optional) - For data warehouse

## Step-by-Step Manual Setup

### 1. Environment Setup

```bash
# Navigate to your project directory
cd /Users/joelomoroje/data_analytics/healthcare-patient-analytics

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Upgrade pip
pip install --upgrade pip
```

### 2. Install Dependencies

```bash
# Install all required packages
pip install -r requirements.txt

# Verify installation
pip list | grep streamlit
pip list | grep pandas
pip list | grep plotly
```

### 3. Test the Dashboard Locally

```bash
# Run the Streamlit dashboard
streamlit run dashboards/healthcare_streamlit_app.py

# The dashboard should open at http://localhost:8501
```

### 4. Set Up Git Repository

```bash
# Initialize git repository (if not already done)
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Healthcare Patient Analytics Platform"

# Add remote repository (replace with your GitHub repo)
git remote add origin https://github.com/yourusername/healthcare-patient-analytics.git

# Push to GitHub
git push -u origin main
```

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```bash
# Create .env file
touch .env
```

Add the following content to `.env`:

```env
# Database Configuration
DATABASE_URL=sqlite:///healthcare_data.db
SNOWFLAKE_ACCOUNT=your_account
SNOWFLAKE_USER=your_username
SNOWFLAKE_PASSWORD=your_password
SNOWFLAKE_WAREHOUSE=your_warehouse
SNOWFLAKE_DATABASE=healthcare_db
SNOWFLAKE_SCHEMA=public

# FHIR API Configuration
FHIR_BASE_URL=https://hapi.fhir.org/baseR4
FHIR_CLIENT_ID=your_client_id
FHIR_CLIENT_SECRET=your_client_secret

# Kafka Configuration
KAFKA_BOOTSTRAP_SERVERS=localhost:9092

# Security Configuration
SECRET_KEY=your_secret_key_here
ENCRYPTION_KEY=your_encryption_key_here

# Streamlit Configuration
STREAMLIT_SERVER_PORT=8501
STREAMLIT_SERVER_ADDRESS=localhost
```

### 6. Set Up Data Sources

#### Option A: Use Simulated Data (Recommended for Testing)
The project includes a medical device simulator that generates realistic healthcare data.

```bash
# Run the device simulator
python src/ingestion/medical_devices/device_simulator.py
```

#### Option B: Connect to Real FHIR Server
1. Sign up for a FHIR server account (e.g., HAPI FHIR)
2. Update the `.env` file with your credentials
3. Test the connection:

```bash
# Test FHIR connection
python -c "
from src.ingestion.fhir_integration.fhir_client import FHIRClient, FHIRConfig
config = FHIRConfig(
    base_url='https://hapi.fhir.org/baseR4',
    client_id='your_client_id',
    client_secret='your_client_secret',
    scope='fhir',
    token_url='https://hapi.fhir.org/baseR4/oauth/token'
)
client = FHIRClient(config)
print('FHIR connection test:', client.authenticate())
"
```

### 7. Set Up Database

#### Option A: SQLite (Default - No Setup Required)
The project uses SQLite by default, which requires no additional setup.

#### Option B: PostgreSQL
```bash
# Install PostgreSQL
# On macOS:
brew install postgresql
brew services start postgresql

# Create database
createdb healthcare_analytics

# Update .env file
DATABASE_URL=postgresql://username:password@localhost/healthcare_analytics
```

#### Option C: Snowflake (Production)
1. Sign up for Snowflake account
2. Create a new database and warehouse
3. Update `.env` file with Snowflake credentials
4. Test connection:

```bash
# Test Snowflake connection
python -c "
import snowflake.connector
conn = snowflake.connector.connect(
    user='your_username',
    password='your_password',
    account='your_account',
    warehouse='your_warehouse',
    database='your_database',
    schema='public'
)
print('Snowflake connection successful')
conn.close()
"
```

### 8. Set Up Apache Kafka (Optional)

For real-time data streaming:

```bash
# Install Kafka
# On macOS:
brew install kafka

# Start Zookeeper
zookeeper-server-start /usr/local/etc/kafka/zookeeper.properties

# Start Kafka
kafka-server-start /usr/local/etc/kafka/server.properties

# Create topics
kafka-topics --create --topic vital_signs --bootstrap-server localhost:9092
kafka-topics --create --topic lab_results --bootstrap-server localhost:9092
kafka-topics --create --topic medications --bootstrap-server localhost:9092
```

### 9. Deploy to Streamlit Cloud

1. **Push to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository: `healthcare-patient-analytics`
   - Main file path: `dashboards/healthcare_streamlit_app.py`
   - Click "Deploy"

3. **Configure Environment Variables:**
   - In Streamlit Cloud, go to your app settings
   - Add the environment variables from your `.env` file
   - Save and redeploy

### 10. Set Up Monitoring and Logging

```bash
# Create logs directory
mkdir logs

# Set up log rotation
# Add to crontab:
# 0 0 * * * /usr/bin/find /path/to/logs -name "*.log" -mtime +7 -delete
```

### 11. Security Configuration

#### HIPAA Compliance Setup
1. **Enable encryption:**
   ```bash
   # Generate encryption keys
   python -c "
   from cryptography.fernet import Fernet
   key = Fernet.generate_key()
   print('Encryption key:', key.decode())
   "
   ```

2. **Set up audit logging:**
   ```bash
   # Create audit log directory
   mkdir -p logs/audit
   chmod 700 logs/audit
   ```

3. **Configure access controls:**
   - Update `config/hipaa_compliance/config.yaml`
   - Set appropriate user roles and permissions
   - Enable PHI masking for non-production environments

### 12. Testing the Setup

```bash
# Run all tests
python -m pytest tests/ -v

# Test data validation
python src/ingestion/data_validator.py

# Test FHIR integration
python src/ingestion/fhir_integration/fhir_client.py

# Test medical device simulator
python src/ingestion/medical_devices/device_simulator.py
```

### 13. Performance Optimization

```bash
# Install performance monitoring tools
pip install memory-profiler psutil

# Run performance tests
python -m memory_profiler dashboards/healthcare_streamlit_app.py

# Optimize database queries
python -c "
import sqlite3
conn = sqlite3.connect('healthcare_data.db')
conn.execute('CREATE INDEX IF NOT EXISTS idx_patient_id ON patients(patient_id)')
conn.execute('CREATE INDEX IF NOT EXISTS idx_timestamp ON vital_signs(timestamp)')
conn.commit()
conn.close()
"
```

## Troubleshooting

### Common Issues

1. **Streamlit not starting:**
   ```bash
   # Check if port is in use
   lsof -i :8501
   # Kill process if needed
   kill -9 <PID>
   ```

2. **Import errors:**
   ```bash
   # Reinstall dependencies
   pip install -r requirements.txt --force-reinstall
   ```

3. **Database connection issues:**
   ```bash
   # Check database file permissions
   ls -la healthcare_data.db
   chmod 644 healthcare_data.db
   ```

4. **FHIR API errors:**
   - Verify API credentials in `.env` file
   - Check network connectivity
   - Verify FHIR server status

### Getting Help

- Check the logs in `logs/` directory
- Review error messages in the console
- Consult the study guide for detailed explanations
- Check GitHub issues for common problems

## Next Steps

After completing the manual setup:

1. **Test all functionality** - Run the dashboard and verify all features work
2. **Add real data** - Connect to actual healthcare data sources
3. **Implement ML models** - Add predictive analytics capabilities
4. **Scale the system** - Optimize for production use
5. **Deploy to production** - Set up monitoring and maintenance

## Support

For technical support:
- Review the study guide for detailed explanations
- Check the project documentation
- Create GitHub issues for bugs
- Consult the healthcare data standards documentation
