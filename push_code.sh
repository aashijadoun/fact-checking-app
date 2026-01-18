#!/bin/bash
# Helper script to push code to GitHub

echo "🚀 Pushing Fact-Checking App to GitHub"
echo "======================================"
echo ""

# Check if remote is set
if ! git remote get-url origin &>/dev/null; then
    echo "❌ No remote configured!"
    echo "Setting remote to: https://github.com/aashijadoun/fact-checking-app.git"
    git remote add origin https://github.com/aashijadoun/fact-checking-app.git
fi

echo "Repository: https://github.com/aashijadoun/fact-checking-app"
echo ""

# Try to push
echo "Attempting to push..."
git push -u origin main

if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "Your code is now live at:"
    echo "https://github.com/aashijadoun/fact-checking-app"
    echo ""
    echo "Next steps:"
    echo "1. Get API keys (OpenAI and Tavily)"
    echo "2. Deploy to Streamlit Cloud at https://share.streamlit.io"
    echo "3. Test your app!"
else
    echo ""
    echo "❌ Push failed - Authentication required"
    echo ""
    echo "You need a Personal Access Token:"
    echo "1. Go to: https://github.com/settings/tokens"
    echo "2. Click 'Generate new token (classic)'"
    echo "3. Name it: 'Fact-Checking App'"
    echo "4. Check 'repo' scope"
    echo "5. Generate and copy the token"
    echo ""
    echo "Then run this command again and use the token as password:"
    echo "  ./push_code.sh"
    echo ""
    echo "Or use the token directly in the URL:"
    echo "  git remote set-url origin https://YOUR_TOKEN@github.com/aashijadoun/fact-checking-app.git"
    echo "  git push -u origin main"
fi

