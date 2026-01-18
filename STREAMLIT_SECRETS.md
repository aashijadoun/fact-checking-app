# Streamlit Cloud Secrets Configuration

## How to Add Secrets in Streamlit Cloud

### Step-by-Step Instructions:

1. **In the "Advanced settings" dialog**, scroll to the **"Secrets"** section
2. **Delete the example text** in the text area
3. **Paste this format** (replace with your actual keys):

```toml
OPENAI_API_KEY = "sk-your-actual-openai-key-here"
TAVILY_API_KEY = "your-actual-tavily-key-here"
```

### Important Notes:

- ✅ Use **TOML format** (key = "value")
- ✅ Keys must be in **UPPERCASE**
- ✅ Values must be in **quotes** ("...")
- ✅ No spaces around the `=` sign (or one space is fine)
- ✅ Each key on a new line

### Example (with placeholder keys):

```toml
OPENAI_API_KEY = "sk-proj-abc123xyz789..."
TAVILY_API_KEY = "tvly-abc123xyz789..."
```

### Common Issues:

**Issue 1: "Invalid TOML format"**
- Make sure values are in quotes
- Check for typos in key names
- Ensure no extra characters

**Issue 2: "Secrets not loading"**
- Wait 1-2 minutes after saving
- Refresh your app
- Check key names match exactly: `OPENAI_API_KEY` and `TAVILY_API_KEY`

**Issue 3: "Can't find secrets section"**
- Make sure you clicked "Advanced settings" (the ">" arrow)
- Scroll down in the dialog
- The secrets section is below Python version

### After Adding Secrets:

1. Click **"Save"** button (blue button at bottom)
2. Wait 1-2 minutes for changes to propagate
3. Your app will automatically redeploy
4. Check the sidebar - you should see "✅ API keys loaded from secrets"

### Testing:

Once deployed, upload a PDF and test. If you see errors about missing API keys, double-check:
- Keys are correctly formatted
- No extra spaces or characters
- Values are in quotes

