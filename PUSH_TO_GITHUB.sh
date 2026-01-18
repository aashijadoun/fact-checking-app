#!/bin/bash
# Script to push code to GitHub
# Run this after creating a repository on GitHub

echo "🚀 Pushing Fact-Checking Web App to GitHub..."
echo ""
echo "Before running this script:"
echo "1. Go to https://github.com/new"
echo "2. Create a new repository (make it PUBLIC for free Streamlit Cloud)"
echo "3. Copy the repository URL"
echo ""
read -p "Enter your GitHub repository URL (e.g., https://github.com/username/repo-name.git): " REPO_URL

if [ -z "$REPO_URL" ]; then
    echo "❌ No repository URL provided. Exiting."
    exit 1
fi

echo ""
echo "Adding remote and pushing..."
git remote add origin "$REPO_URL" 2>/dev/null || git remote set-url origin "$REPO_URL"
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "Next steps:"
    echo "1. Go to https://share.streamlit.io"
    echo "2. Sign in with GitHub"
    echo "3. Click 'New app'"
    echo "4. Select your repository"
    echo "5. Add API keys as secrets"
    echo "6. Deploy!"
else
    echo ""
    echo "❌ Error pushing to GitHub. Please check:"
    echo "   - Repository URL is correct"
    echo "   - Repository exists on GitHub"
    echo "   - You have push access"
fi

