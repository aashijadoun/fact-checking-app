#!/bin/bash
# Push code using personal access token

echo "🚀 Pushing Fact-Checking App to GitHub"
echo "======================================"
echo ""

read -sp "Enter your GitHub Personal Access Token: " TOKEN
echo ""

if [ -z "$TOKEN" ]; then
    echo "❌ Token is required!"
    exit 1
fi

# Set remote with token
git remote set-url origin https://${TOKEN}@github.com/aashijadoun/fact-checking-app.git

echo "Pushing to GitHub..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "Your code is now live at:"
    echo "https://github.com/aashijadoun/fact-checking-app"
    echo ""
    # Remove token from URL for security
    git remote set-url origin https://github.com/aashijadoun/fact-checking-app.git
    echo "✅ Token removed from remote URL for security"
    echo ""
    echo "Next steps:"
    echo "1. Get API keys (OpenAI and Tavily)"
    echo "2. Deploy to Streamlit Cloud at https://share.streamlit.io"
    echo "3. Test your app!"
else
    echo ""
    echo "❌ Push failed. Please check:"
    echo "- Token is correct"
    echo "- Token has 'repo' scope"
    echo "- Repository exists on GitHub"
    # Remove token from URL
    git remote set-url origin https://github.com/aashijadoun/fact-checking-app.git
fi

