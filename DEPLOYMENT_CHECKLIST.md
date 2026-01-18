# Deployment Checklist

Follow these steps to deploy your Fact-Checking Web App to Streamlit Cloud.

## ✅ Step 1: Get API Keys

### OpenAI API Key
- [ ] Go to https://platform.openai.com/api-keys
- [ ] Sign up or log in
- [ ] Click "Create new secret key"
- [ ] Copy and save the key (starts with `sk-...`)
- [ ] **Important**: Save it securely - you won't see it again!

### Tavily API Key
- [ ] Go to https://tavily.com
- [ ] Sign up for a free account
- [ ] Navigate to your dashboard
- [ ] Copy your API key
- [ ] Save it for the next step

## ✅ Step 2: Prepare GitHub Repository

- [ ] Initialize git repository (if not already done):
  ```bash
  git init
  git add .
  git commit -m "Initial commit: Fact-Checking Web App"
  ```

- [ ] Create a new repository on GitHub:
  - Go to https://github.com/new
  - Choose a repository name (e.g., `fact-checking-app`)
  - Make it **Public** (required for free Streamlit Cloud)
  - Click "Create repository"

- [ ] Push your code to GitHub:
  ```bash
  git branch -M main
  git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
  git push -u origin main
  ```

## ✅ Step 3: Deploy to Streamlit Cloud

- [ ] Go to https://share.streamlit.io
- [ ] Sign in with your GitHub account
- [ ] Click **"New app"** button
- [ ] Fill in the deployment form:
  - **Repository**: Select your repository from the dropdown
  - **Branch**: `main`
  - **Main file path**: `app.py`
- [ ] Click **"Advanced settings"** (optional, but recommended)
- [ ] In the "Secrets" section, paste:
  ```
  OPENAI_API_KEY=sk-your-actual-openai-key-here
  TAVILY_API_KEY=your-actual-tavily-key-here
  ```
  (Replace with your actual keys!)
- [ ] Click **"Deploy"**
- [ ] Wait for deployment (usually 1-2 minutes)
- [ ] Your app URL will be: `https://YOUR-APP-NAME.streamlit.app`

## ✅ Step 4: Test Your Deployment

- [ ] Open your deployed app URL
- [ ] Verify the app loads correctly
- [ ] Check that you see "✅ API keys loaded from secrets" in the sidebar
- [ ] Upload a test PDF with some factual claims
- [ ] Click "Start Fact-Checking"
- [ ] Verify that:
  - Claims are extracted
  - Web search is working
  - Results are displayed correctly
  - False/outdated claims are flagged

## ✅ Step 5: Test with Intentional False Claims

Create or use a PDF with:
- [ ] Outdated statistics (e.g., "The US GDP in 2020 was $15 trillion" - should flag as outdated)
- [ ] False claims (e.g., "The Earth is flat" - should flag as False)
- [ ] Incorrect financial data (e.g., wrong stock prices)
- [ ] Verify the app catches these and provides correct information

## Troubleshooting

### App won't deploy
- Check that your repository is **public**
- Verify `app.py` is in the root directory
- Check the deployment logs for errors

### API errors
- Verify API keys are correct in Streamlit Cloud secrets
- Check that keys don't have extra spaces or quotes
- Ensure your OpenAI account has credits
- Check Tavily API usage limits

### App loads but fact-checking fails
- Check the browser console for errors
- Verify API keys are set correctly
- Try a simpler PDF first
- Check API usage/limits

## Success Criteria

Your deployment is successful when:
- ✅ App is accessible via public URL
- ✅ PDF upload works
- ✅ Claims are extracted from documents
- ✅ Web search returns results
- ✅ False/outdated claims are correctly flagged
- ✅ Results display with sources and explanations

## Next Steps

Once deployed:
1. Share your app URL for testing
2. Monitor API usage and costs
3. Consider adding rate limiting for production use
4. Add error handling improvements based on user feedback

---

**Need help?** Check the `DEPLOYMENT.md` file for detailed instructions.

