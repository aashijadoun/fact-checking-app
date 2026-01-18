#!/bin/bash
# Automated deployment helper script

set -e

echo "🚀 Fact-Checking Web App - Deployment Helper"
echo "=============================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Step 1: Check git status
echo -e "${YELLOW}Step 1: Checking git repository...${NC}"
if [ -d ".git" ]; then
    echo -e "${GREEN}✅ Git repository initialized${NC}"
    BRANCH=$(git branch --show-current)
    echo "   Current branch: $BRANCH"
else
    echo -e "${RED}❌ Git repository not found${NC}"
    exit 1
fi

# Step 2: Check if remote exists
echo ""
echo -e "${YELLOW}Step 2: Checking GitHub remote...${NC}"
if git remote get-url origin &>/dev/null; then
    REMOTE_URL=$(git remote get-url origin)
    echo -e "${GREEN}✅ Remote configured: $REMOTE_URL${NC}"
    
    # Check if already pushed
    if git ls-remote --heads origin main &>/dev/null; then
        echo -e "${GREEN}✅ Code already pushed to GitHub${NC}"
        echo ""
        echo "Next: Deploy to Streamlit Cloud at https://share.streamlit.io"
        exit 0
    else
        echo "   Pushing to GitHub..."
        git push -u origin main
        echo -e "${GREEN}✅ Code pushed successfully!${NC}"
    fi
else
    echo -e "${YELLOW}⚠️  No GitHub remote configured${NC}"
    echo ""
    echo "To set up GitHub:"
    echo "1. Create a repository at https://github.com/new"
    echo "2. Make it PUBLIC (required for free Streamlit Cloud)"
    echo "3. Run: git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git"
    echo "4. Run: git push -u origin main"
    echo ""
    read -p "Do you want to open GitHub in your browser? (y/n): " OPEN_BROWSER
    if [ "$OPEN_BROWSER" = "y" ] || [ "$OPEN_BROWSER" = "Y" ]; then
        open "https://github.com/new" 2>/dev/null || xdg-open "https://github.com/new" 2>/dev/null || echo "Please open https://github.com/new manually"
    fi
    exit 0
fi

# Step 3: Deployment instructions
echo ""
echo -e "${YELLOW}Step 3: Deployment Instructions${NC}"
echo ""
echo "Your code is on GitHub! Now deploy to Streamlit Cloud:"
echo ""
echo "1. Go to: https://share.streamlit.io"
echo "2. Sign in with GitHub"
echo "3. Click 'New app'"
echo "4. Select your repository"
echo "5. Set Main file path: app.py"
echo "6. Add secrets:"
echo "   OPENAI_API_KEY=sk-your-key"
echo "   TAVILY_API_KEY=your-key"
echo "7. Click 'Deploy'"
echo ""
read -p "Do you want to open Streamlit Cloud in your browser? (y/n): " OPEN_STREAMLIT
if [ "$OPEN_STREAMLIT" = "y" ] || [ "$OPEN_STREAMLIT" = "Y" ]; then
    open "https://share.streamlit.io" 2>/dev/null || xdg-open "https://share.streamlit.io" 2>/dev/null || echo "Please open https://share.streamlit.io manually"
fi

echo ""
echo -e "${GREEN}✅ Setup complete!${NC}"

