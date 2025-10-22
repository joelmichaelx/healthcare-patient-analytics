#!/bin/bash

# Healthcare Patient Analytics Platform - GitHub Connection Script
# This script will guide you through connecting to GitHub

set -e  # Exit on any error

echo " Healthcare Patient Analytics Platform - GitHub Connection"
echo "============================================================"

# Navigate to project directory
cd "$(dirname "$0")"
echo "Working in directory: $(pwd)"

# Check current git status
echo " Current Git Status:"
echo "====================="
git status --short
echo ""

# Show current remote (if any)
echo " Current Remote Configuration:"
echo "================================"
if git remote get-url origin >/dev/null 2>&1; then
    echo "Current remote: $(git remote get-url origin)"
else
    echo "No remote configured"
fi
echo ""

# Step 1: Create GitHub Repository
echo " Step 1: Create GitHub Repository"
echo "===================================="
echo "1. Go to: https://github.com/new"
echo "2. Repository name: healthcare-patient-analytics"
echo "3. Description: Healthcare Patient Analytics Platform with Real-time Monitoring"
echo "4. Make it: Public"
echo "5. Initialize: NO (don't check any boxes)"
echo "6. Click: Create repository"
echo ""

# Open GitHub in browser
echo " Opening GitHub new repository page..."
if command -v open >/dev/null 2>&1; then
    open "https://github.com/new"
elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "https://github.com/new"
else
    echo "Please open: https://github.com/new"
fi

echo ""
echo "⏳ Please create the repository in your browser, then come back here..."
read -p "Press Enter when you've created the repository..."

# Step 2: Get repository URL
echo ""
echo " Step 2: Configure Repository URL"
echo "==================================="
echo "After creating the repository, GitHub will show you a URL like:"
echo "https://github.com/YOUR_USERNAME/healthcare-patient-analytics.git"
echo ""

# Get repository URL from user
while true; do
    read -p "Enter your GitHub repository URL: " REPO_URL
    
    if [[ $REPO_URL =~ ^https://github\.com/[^/]+/healthcare-patient-analytics\.git$ ]]; then
        echo " Valid repository URL: $REPO_URL"
        break
    else
        echo " Invalid URL format. Please use: https://github.com/USERNAME/healthcare-patient-analytics.git"
    fi
done

# Step 3: Configure remote and push
echo ""
echo " Step 3: Configure Remote and Push"
echo "===================================="

# Remove existing remote if it exists
if git remote get-url origin >/dev/null 2>&1; then
    echo "Removing existing remote..."
    git remote remove origin
fi

# Add new remote
echo "Adding remote repository: $REPO_URL"
git remote add origin "$REPO_URL"
echo " Remote added successfully"

# Push to GitHub
echo ""
echo " Pushing code to GitHub..."
echo "This may take a moment..."

if git push -u origin main; then
    echo " Code pushed to GitHub successfully!"
else
    echo " Push failed. This might be because:"
    echo "   - Repository doesn't exist yet"
    echo "   - Authentication issues"
    echo "   - Network problems"
    echo ""
    echo "Please check:"
    echo "1. Repository exists at: $REPO_URL"
    echo "2. You're logged into GitHub"
    echo "3. You have push access to the repository"
    echo ""
    echo "You can try pushing manually:"
    echo "   git push -u origin main"
    exit 1
fi

# Step 4: Success and next steps
echo ""
echo " GitHub Connection Complete!"
echo "=============================="
echo " Repository: $REPO_URL"
echo " Code pushed successfully"
echo " Ready for Streamlit Cloud deployment"
echo ""

# Show repository info
echo " Repository Information:"
echo "========================="
echo "Repository URL: $REPO_URL"
echo "Branch: main"
echo "Files: $(git ls-files | wc -l) files"
echo "Commits: $(git rev-list --count HEAD) commits"
echo ""

# Show next steps
echo " Next Steps:"
echo "============="
echo "1. Deploy to Streamlit Cloud:"
echo "   - Go to: https://share.streamlit.io"
echo "   - Sign in with GitHub"
echo "   - Select: healthcare-patient-analytics"
echo "   - Main file: dashboards/healthcare_streamlit_app.py"
echo "   - Deploy!"
echo ""
echo "2. Test your local dashboard:"
echo "   ./start_dashboard.sh"
echo "   Open: http://localhost:8501"
echo ""
echo "3. Share your project:"
echo "   - Add to your portfolio"
echo "   - Share the Streamlit Cloud URL"
echo "   - Showcase your healthcare data engineering skills"
echo ""

# Create deployment summary
cat > GITHUB_CONNECTION_SUMMARY.md << EOF
# GitHub Connection Summary

##  Successfully Connected to GitHub

**Repository**: $REPO_URL
**Status**: Code pushed successfully
**Branch**: main
**Files**: $(git ls-files | wc -l) files committed

##  Project Contents

### Healthcare Data:
- **10 Patients** with realistic medical conditions
- **420 Vital Signs** records over 7 days
- **80 Lab Results** with critical value detection
- **199 Medications** administration records

### Technical Features:
- **Interactive Dashboard** with 6 main sections
- **Real-time Monitoring** with live data updates
- **HIPAA Compliance** with secure data handling
- **Professional UI** with healthcare-appropriate design

### Files Included:
- `dashboards/healthcare_streamlit_app.py` - Main dashboard
- `populate_data.py` - Data generation script
- `requirements.txt` - Dependencies
- `README.md` - Project documentation
- `STUDY_GUIDE.md` - Learning resource
- Database with realistic healthcare data

##  Ready for Deployment

Your healthcare analytics platform is now:
-  **GitHub Repository**: Created and configured
-  **Code Pushed**: All files uploaded
-  **Documentation**: Complete guides included
-  **Data Populated**: Realistic healthcare data
-  **Dashboard Ready**: Fully functional

##  Test Locally

\`\`\`bash
./start_dashboard.sh
# Open: http://localhost:8501
\`\`\`

##  Deploy to Streamlit Cloud

1. Go to: https://share.streamlit.io
2. Sign in with GitHub
3. Select: healthcare-patient-analytics
4. Main file: dashboards/healthcare_streamlit_app.py
5. Deploy!

##  Portfolio Value

This project demonstrates:
- **Healthcare Data Engineering**
- **Real-time Analytics**
- **HIPAA Compliance**
- **Interactive Dashboards**
- **Production Deployment**

**Your healthcare analytics platform is ready for the world!**
EOF

echo " Created: GITHUB_CONNECTION_SUMMARY.md"
echo ""
echo " Your Healthcare Analytics Platform is now on GitHub!"
echo "Repository: $REPO_URL"
echo ""
echo "Ready to deploy to Streamlit Cloud and share with the world! "
