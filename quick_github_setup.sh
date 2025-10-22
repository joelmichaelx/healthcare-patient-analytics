#!/bin/bash

echo " Healthcare Patient Analytics - Quick GitHub Setup"
echo "=================================================="

# Open GitHub new repository page
echo " Opening GitHub new repository page..."
open "https://github.com/new" 2>/dev/null || xdg-open "https://github.com/new" 2>/dev/null || echo "Please open: https://github.com/new"

echo ""
echo " Create repository with these settings:"
echo "   Repository name: healthcare-patient-analytics"
echo "   Description: Healthcare Patient Analytics Platform with Real-time Monitoring"
echo "   Make it: Public"
echo "   Initialize: NO (don't check any boxes)"
echo "   Click: Create repository"
echo ""

# Wait for user to create repository
read -p "Press Enter when you've created the repository..."

# Get repository URL
echo ""
echo " Enter your GitHub repository URL:"
echo "Format: https://github.com/YOUR_USERNAME/healthcare-patient-analytics.git"
read -p "Repository URL: " REPO_URL

# Set up remote and push
echo ""
echo " Setting up remote repository..."
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"

echo " Pushing code to GitHub..."
git push -u origin main

echo ""
echo " GitHub setup complete!"
echo "Repository: $REPO_URL"
echo ""
echo " Next: Deploy to Streamlit Cloud"
echo "1. Go to: https://share.streamlit.io"
echo "2. Sign in with GitHub"
echo "3. Select your repository"
echo "4. Main file: dashboards/healthcare_streamlit_app.py"
echo "5. Deploy!"
