# GitHub Repository Setup - Step by Step

## Current Status
✅ You're on the GitHub login page

## Step-by-Step Instructions

### 1. Sign In to GitHub
- Enter your **username or email** in the first field
- Enter your **password** in the second field
- Click **"Sign in"** button

### 2. Create New Repository
After signing in, you'll be redirected to the "Create a new repository" page.

Fill in the form:

**Repository name:**
```
fact-checking-app
```

**Description (optional):**
```
Fact-Checking Web App - Automatically verifies claims from PDFs against live web data
```

**Visibility:**
- ✅ Select **"Public"** (required for free Streamlit Cloud)
- ❌ Do NOT select "Private"

**Initialize repository:**
- ❌ **DO NOT** check "Add a README file" (we already have one)
- ❌ **DO NOT** check "Add .gitignore" (we already have one)
- ❌ **DO NOT** select a license (optional, we can add later if needed)

**Click:** "Create repository" button (green button at the bottom)

### 3. After Creating Repository

GitHub will show you a page with setup instructions. **IGNORE those** - we already have everything set up!

Instead, run these commands in your terminal:

```bash
cd /Users/aashijadoun/Cog_Culture
git remote add origin https://github.com/YOUR_USERNAME/fact-checking-app.git
git push -u origin main
```

**Important:** Replace `YOUR_USERNAME` with your actual GitHub username!

### 4. Verify Push

After running the commands, refresh your GitHub repository page. You should see all your files:
- app.py
- fact_checker.py
- requirements.txt
- README.md
- And all other files

## Troubleshooting

**If you get "repository already exists" error:**
- The remote might already be set. Run: `git remote remove origin` then try again.

**If you get authentication errors:**
- You may need to set up SSH keys or use a personal access token
- Or use: `git remote add origin https://YOUR_USERNAME@github.com/YOUR_USERNAME/fact-checking-app.git`

**If push is rejected:**
- Make sure the repository is empty on GitHub (no README was added)
- Or run: `git pull origin main --allow-unrelated-histories` first

## Next Steps After GitHub Setup

Once your code is on GitHub:
1. Get API keys (OpenAI and Tavily)
2. Deploy to Streamlit Cloud
3. Test your app!

See `DEPLOY_NOW.md` for complete instructions.

