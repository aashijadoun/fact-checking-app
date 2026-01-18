# Quick Start Guide

Get your Fact-Checking Web App running in 5 minutes!

## 🚀 Fastest Path to Deployment

### 1. Get API Keys (2 minutes)

**OpenAI:**
1. Visit https://platform.openai.com/api-keys
2. Create account/login
3. Click "Create new secret key"
4. Copy the key (starts with `sk-`)

**Tavily:**
1. Visit https://tavily.com
2. Sign up (free)
3. Copy your API key from dashboard

### 2. Push to GitHub (1 minute)

```bash
cd /Users/aashijadoun/Cog_Culture
git init
git add .
git commit -m "Fact-Checking Web App"
git branch -M main

# Create repo on GitHub first, then:
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

**Important:** Make the GitHub repo **PUBLIC** (required for free Streamlit Cloud)

### 3. Deploy to Streamlit Cloud (2 minutes)

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repo, branch `main`, file `app.py`
5. Click "Advanced settings"
6. Add secrets:
   ```
   OPENAI_API_KEY=sk-your-key-here
   TAVILY_API_KEY=your-key-here
   ```
7. Click "Deploy"
8. Wait ~1 minute
9. **Done!** Your app is live at `https://YOUR-APP.streamlit.app`

## 🧪 Test Locally First (Optional)

```bash
# Install dependencies
pip install -r requirements.txt

# Set API keys
export OPENAI_API_KEY="sk-your-key"
export TAVILY_API_KEY="your-key"

# Run app
streamlit run app.py
```

Then open http://localhost:8501

## ✅ Verify It Works

1. Upload a PDF with some claims
2. Click "Start Fact-Checking"
3. Should see:
   - Claims extracted
   - Web search results
   - Verification status (Verified/Inaccurate/False)
   - Sources and explanations

## 🎯 Test with False Claims

Try a PDF containing:
- "The US population is 200 million" (should flag as inaccurate - actual is ~330M)
- "Bitcoin price is $10,000" (should flag as outdated)
- Any obviously false claim

The app should catch these and provide correct information!

---

**That's it!** Your fact-checking app is now live and ready to test. 🎉

