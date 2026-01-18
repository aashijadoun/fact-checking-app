# Fact-Checking Web App

A deployed web application that automatically extracts claims from PDF documents and verifies them against live web data using AI and web search APIs.

## Features

- **PDF Upload**: Drag-and-drop interface for uploading PDF documents
- **Claim Extraction**: Automatically identifies specific claims (statistics, dates, financial figures, technical specs) from documents
- **Live Verification**: Cross-references claims against real-time web data using Tavily Search API
- **Detailed Reporting**: Flags each claim as:
  - ✅ **Verified**: Matches reliable sources
  - ⚠️ **Inaccurate**: Contains outdated or incorrect data (with corrected values)
  - ❌ **False**: No evidence found or contradicts reliable sources
- **Source Citations**: Provides links to sources used for verification

## Tech Stack

- **Frontend**: Streamlit (simple, intuitive UI)
- **Backend**: Python
- **AI/LLM**: OpenAI GPT-4o-mini (for claim extraction and verification analysis)
- **Web Search**: Tavily API (for real-time web data retrieval)
- **PDF Processing**: pdfplumber

## Setup Instructions

### Local Development

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd Cog_Culture
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up API keys**:
   - Get an OpenAI API key from [OpenAI Platform](https://platform.openai.com/api-keys)
   - Get a Tavily API key from [Tavily](https://tavily.com/)
   
   You can either:
   - Set environment variables:
     ```bash
     export OPENAI_API_KEY="your-openai-key"
     export TAVILY_API_KEY="your-tavily-key"
     ```
   - Or enter them in the app's sidebar when running

4. **Run the app**:
   ```bash
   streamlit run app.py
   ```

5. **Access the app**: Open your browser to `http://localhost:8501`

## Deployment

### Streamlit Cloud (Recommended)

1. **Push to GitHub**: Ensure your code is in a GitHub repository

2. **Deploy on Streamlit Cloud**:
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with your GitHub account
   - Click "New app"
   - Select your repository and branch
   - Set the main file path to `app.py`
   - Add secrets in the "Secrets" section:
     ```
     OPENAI_API_KEY=your-openai-key
     TAVILY_API_KEY=your-tavily-key
     ```
   - Click "Deploy"

3. **Access your deployed app**: You'll get a URL like `https://your-app.streamlit.app`

### Alternative Deployment Options

- **Render**: Create a `render.yaml` or use the web service option
- **Heroku**: Use a `Procfile` with `web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
- **Vercel**: Use the Streamlit adapter or deploy as a Python app

## How It Works

1. **PDF Upload**: User uploads a PDF document through the Streamlit interface
2. **Text Extraction**: The app extracts text from all pages of the PDF using pdfplumber
3. **Claim Identification**: OpenAI GPT-4o-mini analyzes the text and extracts specific, verifiable claims (statistics, dates, figures, etc.)
4. **Web Search**: For each claim, Tavily API searches the web for relevant, current information
5. **Verification**: GPT-4o-mini analyzes the search results and determines if the claim is:
   - Verified (matches sources)
   - Inaccurate (outdated/incorrect data)
   - False (no evidence or contradicts sources)
6. **Results Display**: The app presents a detailed report with status, explanations, sources, and corrected values

## Example Usage

1. Upload a PDF document containing claims (e.g., a research paper, article, or report)
2. Click "Start Fact-Checking"
3. Review the results:
   - See summary statistics (total claims, verified, inaccurate, false)
   - Expand each claim to see detailed verification results
   - Check sources and corrected values
4. Download results as JSON for further analysis

## API Keys Required

- **OpenAI API Key**: For claim extraction and verification analysis
- **Tavily API Key**: For web search functionality

Both can be obtained from their respective platforms and entered in the app's sidebar or set as environment variables.

## Limitations

- PDF must contain extractable text (not scanned images)
- Processing time depends on the number of claims (approximately 5-10 seconds per claim)
- API rate limits may apply based on your OpenAI and Tavily plans
- Maximum of 20 claims extracted per document to avoid rate limits

## File Structure

```
Cog_Culture/
├── app.py              # Main Streamlit application
├── fact_checker.py     # Core fact-checking logic
├── requirements.txt    # Python dependencies
└── README.md          # This file
```

## License

This project is provided as-is for demonstration purposes.

