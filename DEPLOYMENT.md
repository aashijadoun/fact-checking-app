# Deployment Guide

This guide provides step-by-step instructions for deploying the Fact-Checking Web App.

## Quick Deploy: Streamlit Cloud (Recommended)

Streamlit Cloud is the easiest way to deploy this app. It's free and takes just a few minutes.

### Step 1: Push to GitHub

1. Create a new repository on GitHub
2. Push your code:
   ```bash
   git init
   git add .
   git commit -m "Initial commit: Fact-Checking Web App"
   git branch -M main
   git remote add origin https://github.com/yourusername/your-repo-name.git
   git push -u origin main
   ```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"**
4. Fill in the form:
   - **Repository**: Select your repository
   - **Branch**: `main`
   - **Main file path**: `app.py`
5. Click **"Advanced settings"** and add secrets:
   ```
   OPENAI_API_KEY=your-openai-api-key
   TAVILY_API_KEY=your-tavily-api-key
   ```
6. Click **"Deploy"**

### Step 3: Access Your App

Your app will be available at: `https://your-app-name.streamlit.app`

## Alternative Deployment Options

### Render

1. Create a new **Web Service** on Render
2. Connect your GitHub repository
3. Settings:
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
4. Add environment variables:
   - `OPENAI_API_KEY`
   - `TAVILY_API_KEY`
5. Deploy

### Heroku

1. Create a `Procfile`:
   ```
   web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. Create `runtime.txt`:
   ```
   python-3.11.0
   ```

3. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set OPENAI_API_KEY=your-key
   heroku config:set TAVILY_API_KEY=your-key
   git push heroku main
   ```

### Vercel

1. Install Vercel CLI: `npm i -g vercel`
2. Create `vercel.json`:
   ```json
   {
     "builds": [
       {
         "src": "app.py",
         "use": "@vercel/python"
       }
     ],
     "routes": [
       {
         "src": "/(.*)",
         "dest": "app.py"
       }
     ]
   }
   ```
3. Deploy: `vercel --prod`

## Getting API Keys

### OpenAI API Key

1. Go to [platform.openai.com](https://platform.openai.com)
2. Sign up or log in
3. Navigate to **API Keys** section
4. Click **"Create new secret key"**
5. Copy and save the key (you won't see it again)

### Tavily API Key

1. Go to [tavily.com](https://tavily.com)
2. Sign up for a free account
3. Navigate to your dashboard
4. Copy your API key

## Testing Your Deployment

1. Upload a test PDF with some factual claims
2. Verify that claims are extracted
3. Check that web search is working
4. Confirm results are displayed correctly

## Troubleshooting

### App won't start
- Check that `requirements.txt` is correct
- Verify API keys are set correctly
- Check build logs for errors

### API errors
- Verify your API keys are valid
- Check your API usage limits
- Ensure keys are set as environment variables/secrets

### PDF extraction fails
- Ensure PDF contains extractable text (not just images)
- Try a different PDF to test

## Cost Considerations

- **OpenAI**: Pay-per-use, ~$0.15 per 1M input tokens (GPT-4o-mini)
- **Tavily**: Free tier available, then pay-per-search
- **Streamlit Cloud**: Free for public repos

For testing, expect ~$0.01-0.05 per document depending on claim count.

