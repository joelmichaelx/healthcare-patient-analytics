#!/usr/bin/env python3
"""
Automated GitHub Repository Creation and Deployment
This script helps automate the GitHub repository creation process
"""

import webbrowser
import time
import subprocess
import sys
import os

def open_github_new_repo():
    """Open GitHub new repository page"""
    print(" Opening GitHub new repository page...")
    webbrowser.open("https://github.com/new")
    print(" GitHub new repository page opened in your browser")
    print("\n Follow these steps in the opened browser:")
    print("1. Repository name: healthcare-patient-analytics")
    print("2. Description: Healthcare Patient Analytics Platform with Real-time Monitoring")
    print("3. Make it Public")
    print("4. DO NOT initialize with README, .gitignore, or license")
    print("5. Click 'Create repository'")
    print("\n⏳ Waiting for you to create the repository...")
    input("Press Enter when you've created the repository...")

def get_repo_url():
    """Get repository URL from user"""
    print("\n Please provide your GitHub repository URL:")
    print("Format: https://github.com/YOUR_USERNAME/healthcare-patient-analytics.git")
    repo_url = input("Repository URL: ").strip()
    
    if not repo_url.startswith("https://github.com/"):
        print(" Invalid URL format. Please use: https://github.com/USERNAME/REPO.git")
        return get_repo_url()
    
    return repo_url

def setup_remote_and_push(repo_url):
    """Set up remote and push to GitHub"""
    print(f"\n Setting up remote repository: {repo_url}")
    
    # Remove existing remote if it exists
    try:
        subprocess.run(["git", "remote", "remove", "origin"], check=False)
    except:
        pass
    
    # Add new remote
    subprocess.run(["git", "remote", "add", "origin", repo_url], check=True)
    print(" Remote origin added")
    
    # Push to GitHub
    print(" Pushing code to GitHub...")
    subprocess.run(["git", "push", "-u", "origin", "main"], check=True)
    print(" Code pushed to GitHub successfully!")
    
    return repo_url

def open_streamlit_cloud():
    """Open Streamlit Cloud deployment page"""
    print("\n Opening Streamlit Cloud for deployment...")
    webbrowser.open("https://share.streamlit.io")
    print(" Streamlit Cloud opened in your browser")
    print("\n Follow these steps in Streamlit Cloud:")
    print("1. Sign in with GitHub")
    print("2. Click 'New app'")
    print("3. Repository: Select your healthcare-patient-analytics repository")
    print("4. Branch: main")
    print("5. Main file path: dashboards/healthcare_streamlit_app.py")
    print("6. Click 'Deploy'")
    print("\n Your healthcare analytics platform will be live on Streamlit Cloud!")

def main():
    """Main automation function"""
    print(" Healthcare Patient Analytics Platform - GitHub Automation")
    print("=" * 60)
    
    # Step 1: Open GitHub new repo page
    open_github_new_repo()
    
    # Step 2: Get repository URL
    repo_url = get_repo_url()
    
    # Step 3: Set up remote and push
    setup_remote_and_push(repo_url)
    
    # Step 4: Open Streamlit Cloud
    open_streamlit_cloud()
    
    print("\n GitHub Deployment Complete!")
    print("=" * 30)
    print(" Repository created and configured")
    print(" Code pushed to GitHub")
    print(" Ready for Streamlit Cloud deployment")
    print(f" Repository URL: {repo_url}")
    print("\n Test your local dashboard:")
    print("   ./start_dashboard.sh")
    print("   Open: http://localhost:8501")

if __name__ == "__main__":
    main()
