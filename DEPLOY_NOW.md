# 🚀 Deploy Now - Step by Step

I've opened the necessary pages in your browser. Follow these steps:

## ✅ Step 1: Create GitHub Repository (Browser is open)

1. **Sign in to GitHub** (if not already signed in)
2. Fill in the form:
   - **Repository name**: `fact-checking-app`
   - **Description**: "Fact-Checking Web App - Automatically verifies claims from PDFs"
   - **Visibility**: Select **Public** (required for free Streamlit Cloud)
   - **DO NOT** check "Add a README file" (we already have one)
   - **DO NOT** check "Add .gitignore" (we already have one)
   - **DO NOT** select a license (optional)
3. Click **"Create repository"**

## ✅ Step 2: Push Code to GitHub

After creating the repository, GitHub will show you commands. Run these in your terminal:

```bash
cd /Users/aashijadoun/Cog_Culture

# Replace YOUR_USERNAME and YOUR_REPO_NAME with your actual values
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git push -u origin main
```

Or use the automated script:
```bash
./automated_deploy.sh
```

## ✅ Step 3: Get API Keys

### OpenAI API Key
1. Go to: https://platform.openai.com/api-keys
2. Sign up or log in
3. Click **"Create new secret key"**
4. Copy the key (starts with `sk-...`)
5. **Save it somewhere safe!**

### Tavily API Key  
1. Go to: https://tavily.com
2. Sign up for a free account
3. Navigate to your dashboard
4. Copy your API key
5. **Save it somewhere safe!**

## ✅ Step 4: Deploy to Streamlit Cloud

1. Go to: https://share.streamlit.io
2. Sign in with your **GitHub account**
3. Click **"New app"** button
4. Fill in:
   - **Repository**: Select your repository from dropdown
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Advanced settings"** (or the ">" arrow)
6. In the **"Secrets"** section, paste exactly:
   ```
   OPENAI_API_KEY=sk-your-actual-openai-key-here
   TAVILY_API_KEY=your-actual-tavily-key-here
   ```
   (Replace with your actual keys - no quotes needed!)
7. Click **"Deploy"**
8. Wait 1-2 minutes
9. Your app will be live! 🎉

## ✅ Step 5: Test Your App

1. Open your app URL (e.g., `https://fact-checking-app.streamlit.app`)
2. Check the sidebar - you should see "✅ API keys loaded from secrets"
3. Upload a test PDF
4. Click "Start Fact-Checking"
5. Verify it works!

## 🎯 Quick Commands Reference

```bash
# Check git status
git status

# Push to GitHub (after setting remote)
git push -u origin main

# Run automated deployment helper
./automated_deploy.sh
```

---

**Need help?** All your code is ready at: `/Users/aashijadoun/Cog_Culture`

