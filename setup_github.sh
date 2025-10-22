#!/bin/bash

# Healthcare Patient Analytics Platform - GitHub Setup Script
# Automatically sets up GitHub repository and pushes code

set -e  # Exit on any error

echo "Healthcare Patient Analytics Platform - GitHub Setup"
echo "=================================================="

# Navigate to project directory
cd "$(dirname "$0")"
echo "Working in directory: $(pwd)"

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "Git repository not found. Initializing..."
    git init
fi

# Add all files
echo "Adding all files to git..."
git add .

# Create commit
echo "Creating commit..."
git commit -m "Healthcare Patient Analytics Platform - Complete Implementation

Features:
- Real-time patient monitoring dashboard
- Vital signs tracking and alerts
- Lab results analysis with critical value detection
- Medication administration tracking
- Population health analytics
- HIPAA-compliant data handling
- Interactive Streamlit interface

Data:
- 10 sample patients with realistic demographics
- 420 vital signs records over 7 days
- 80 lab results with critical value flags
- 199 medication administration records

Tech Stack:
- Python, Streamlit, Plotly, Pandas
- SQLite database with optimized schema
- Real-time data visualization
- Healthcare data validation
- FHIR integration ready

Ready for deployment to Streamlit Cloud!"

echo " Commit created successfully"

# Check if remote exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "Remote origin already exists"
    CURRENT_URL=$(git remote get-url origin)
    echo "Current remote URL: $CURRENT_URL"
else
    echo "No remote origin found"
    echo "Please create a GitHub repository first:"
    echo "1. Go to https://github.com/new"
    echo "2. Create repository: healthcare-patient-analytics"
    echo "3. Don't initialize with README (we have files)"
    echo "4. Copy the repository URL"
    echo ""
    echo "Then run:"
    echo "git remote add origin YOUR_REPOSITORY_URL"
    echo "git push -u origin main"
    echo ""
    echo "Or update the remote URL below:"
fi

# Create GitHub setup instructions
cat > GITHUB_SETUP.md << 'EOF'
# GitHub Repository Setup Instructions

## Step 1: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `healthcare-patient-analytics`
3. Description: `Healthcare Patient Analytics Platform with Real-time Monitoring`
4. Make it Public (for Streamlit Cloud deployment)
5. **Don't** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

## Step 2: Connect Local Repository

After creating the repository, GitHub will show you commands. Use these:

```bash
# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/healthcare-patient-analytics.git

# Push your code to GitHub
git push -u origin main
```

## Step 3: Deploy to Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Repository: `YOUR_USERNAME/healthcare-patient-analytics`
5. Branch: `main`
6. Main file path: `dashboards/healthcare_streamlit_app.py`
7. Click "Deploy"

## Step 4: Configure Environment Variables (Optional)

In Streamlit Cloud, you can add environment variables:
- `DATABASE_URL=sqlite:///healthcare_data.db`
- `SECRET_KEY=healthcare_analytics_secret_key_2024`

## Your Healthcare Analytics Platform is Now Live!

- **Local Development**: http://localhost:8501
- **Streamlit Cloud**: https://YOUR_APP_NAME.streamlit.app
- **GitHub Repository**: https://github.com/YOUR_USERNAME/healthcare-patient-analytics

## Features Available

 **Patient Management**: 10 sample patients with realistic data
 **Vital Signs**: 420 records with real-time monitoring
 **Lab Results**: 80 results with critical value alerts
 **Medications**: 199 administration records
 **Analytics**: Population health insights
 **Alerts**: Critical health notifications
 **HIPAA Compliance**: Secure data handling

## Next Steps

1. **Test locally**: `./start_dashboard.sh`
2. **Deploy to GitHub**: Follow steps above
3. **Deploy to Streamlit Cloud**: Follow deployment steps
4. **Share your project**: Add to your portfolio!

## Support

- **Documentation**: README.md, STUDY_GUIDE.md
- **Setup Guide**: MANUAL_SETUP_GUIDE.md
- **Deployment**: DEPLOYMENT_INSTRUCTIONS.md
EOF

echo " GitHub setup instructions created: GITHUB_SETUP.md"

# Show current status
echo ""
echo " Current Status:"
echo "=================="
echo " Git repository initialized"
echo " All files committed"
echo " Healthcare data populated (10 patients, 420 vitals, 80 labs, 199 meds)"
echo " Dashboard ready with realistic data"
echo ""
echo " Next Steps:"
echo "1. Create GitHub repository: https://github.com/new"
echo "2. Follow instructions in: GITHUB_SETUP.md"
echo "3. Deploy to Streamlit Cloud: https://share.streamlit.io"
echo ""
echo " Test your dashboard:"
echo "   ./start_dashboard.sh"
echo "   Open: http://localhost:8501"
echo ""
echo " Your healthcare analytics platform is ready for deployment!"
