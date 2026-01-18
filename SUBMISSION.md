# Fact-Checking Web App - Submission

## Overview

This is a fully functional fact-checking web application that automatically extracts claims from PDF documents and verifies them against live web data. The app identifies specific claims (statistics, dates, financial figures, technical specs) and flags them as Verified, Inaccurate, or False.

## Deployed App Link

**Note**: To deploy the app, follow the instructions in `DEPLOYMENT.md`. Once deployed on Streamlit Cloud, your app will be available at:

```
https://your-app-name.streamlit.app
```

### Quick Deploy Steps:

1. Push this code to a GitHub repository
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo
4. Add secrets:
   - `OPENAI_API_KEY`
   - `TAVILY_API_KEY`
5. Deploy!

## GitHub Repository

The repository contains:

- **`app.py`**: Main Streamlit application with drag-and-drop PDF upload interface
- **`fact_checker.py`**: Core fact-checking logic using OpenAI and Tavily APIs
- **`requirements.txt`**: All Python dependencies
- **`README.md`**: Comprehensive documentation
- **`DEPLOYMENT.md`**: Step-by-step deployment guide
- **`.streamlit/config.toml`**: Streamlit configuration
- **`.gitignore`**: Git ignore file

## How It Works

1. **PDF Upload**: User uploads a PDF through the Streamlit interface
2. **Text Extraction**: Extracts text from all PDF pages using pdfplumber
3. **Claim Extraction**: Uses OpenAI GPT-4o-mini to identify specific, verifiable claims
4. **Web Search**: For each claim, searches the web using Tavily API
5. **Verification**: Analyzes search results and categorizes each claim as:
   - ✅ **Verified**: Matches reliable sources
   - ⚠️ **Inaccurate**: Contains outdated/incorrect data (with corrected values)
   - ❌ **False**: No evidence or contradicts sources
6. **Results Display**: Shows detailed report with explanations, sources, and statistics

## Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **AI/LLM**: OpenAI GPT-4o-mini
- **Web Search**: Tavily API
- **PDF Processing**: pdfplumber

## Key Features

✅ Drag-and-drop PDF upload  
✅ Automatic claim extraction  
✅ Real-time web verification  
✅ Detailed reporting with source citations  
✅ Progress indicators  
✅ JSON export of results  
✅ Clean, intuitive UI  

## Testing

The app is designed to catch:
- Intentional lies and false claims
- Outdated statistics (e.g., old GDP figures, wrong stock prices)
- Widely circulated myths
- Incorrect financial data

When tested with documents containing false information, the app will flag them and provide correct, real-time data from reliable sources.

## API Keys Required

- **OpenAI API Key**: [Get one here](https://platform.openai.com/api-keys)
- **Tavily API Key**: [Get one here](https://tavily.com/)

## Local Testing

```bash
pip install -r requirements.txt
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

**Ready for deployment and testing!** 🚀

