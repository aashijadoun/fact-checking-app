#!/bin/bash
# Run this AFTER creating the GitHub repository

echo "🚀 Pushing Fact-Checking App to GitHub"
echo "======================================"
echo ""

# Get GitHub username
read -p "Enter your GitHub username: " GITHUB_USERNAME

if [ -z "$GITHUB_USERNAME" ]; then
    echo "❌ Username is required!"
    exit 1
fi

REPO_URL="https://github.com/${GITHUB_USERNAME}/fact-checking-app.git"

echo "Repository URL: $REPO_URL"
echo ""

# Check if remote already exists
if git remote get-url origin &>/dev/null; then
    echo "⚠️  Remote 'origin' already exists"
    read -p "Remove existing remote and continue? (y/n): " REMOVE
    if [ "$REMOVE" = "y" ] || [ "$REMOVE" = "Y" ]; then
        git remote remove origin
        echo "✅ Removed existing remote"
    else
        echo "❌ Cancelled"
        exit 1
    fi
fi

# Add remote
echo "Adding remote..."
git remote add origin "$REPO_URL"

# Push
echo "Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "Your repository is now at:"
    echo "https://github.com/${GITHUB_USERNAME}/fact-checking-app"
    echo ""
    echo "Next steps:"
    echo "1. Get API keys (OpenAI and Tavily)"
    echo "2. Deploy to Streamlit Cloud"
    echo "3. Test your app!"
else
    echo ""
    echo "❌ Error pushing to GitHub"
    echo "Please check:"
    echo "- Repository exists on GitHub"
    echo "- Repository is empty (no README added)"
    echo "- You have push access"
fi
