import streamlit as st
import pdfplumber
import os
from typing import List, Dict
import json
from fact_checker import FactChecker

st.set_page_config(
    page_title="Fact-Checking Web App",
    page_icon="✅",
    layout="wide"
)

st.title("🔍 Fact-Checking Web App")
st.markdown("Upload a PDF document to automatically verify claims against live web data.")

# Initialize session state
if 'results' not in st.session_state:
    st.session_state.results = None
if 'claims' not in st.session_state:
    st.session_state.claims = []

# Sidebar for API keys
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Try to get from Streamlit secrets first, then environment variables, then user input
    try:
        openai_key_from_secrets = st.secrets.get("OPENAI_API_KEY", None)
        tavily_key_from_secrets = st.secrets.get("TAVILY_API_KEY", None)
    except (AttributeError, FileNotFoundError):
        # Not using Streamlit secrets (local development)
        openai_key_from_secrets = None
        tavily_key_from_secrets = None
    
    openai_api_key = openai_key_from_secrets or os.getenv("OPENAI_API_KEY", "")
    tavily_api_key = tavily_key_from_secrets or os.getenv("TAVILY_API_KEY", "")
    
    # Show status if keys are loaded from secrets
    if openai_key_from_secrets or tavily_key_from_secrets:
        st.success("✅ API keys loaded from secrets")
        st.info("Keys are configured via Streamlit Cloud secrets. You can override them below if needed.")
    
    # Allow manual override
    openai_api_key_input = st.text_input(
        "OpenAI API Key",
        type="password",
        value=openai_api_key,
        help="Enter your OpenAI API key (or leave as-is if using secrets)"
    )
    tavily_api_key_input = st.text_input(
        "Tavily API Key",
        type="password",
        value=tavily_api_key,
        help="Enter your Tavily API key (or leave as-is if using secrets)"
    )
    
    # Use the input values (which will be the same if from secrets)
    openai_api_key = openai_api_key_input if openai_api_key_input else openai_api_key
    tavily_api_key = tavily_api_key_input if tavily_api_key_input else tavily_api_key
    
    if openai_api_key:
        os.environ["OPENAI_API_KEY"] = openai_api_key
    if tavily_api_key:
        os.environ["TAVILY_API_KEY"] = tavily_api_key

# Main content area
uploaded_file = st.file_uploader(
    "Upload PDF Document",
    type=["pdf"],
    help="Drag and drop a PDF file or click to browse"
)

if uploaded_file is not None:
    # Display file info
    st.success(f"✅ File uploaded: {uploaded_file.name}")
    
    # Extract text from PDF
    with st.spinner("📄 Extracting text from PDF..."):
        try:
            pdf_text = ""
            with pdfplumber.open(uploaded_file) as pdf:
                for page in pdf.pages:
                    pdf_text += page.extract_text() + "\n"
            
            if not pdf_text.strip():
                st.error("❌ Could not extract text from PDF. Please ensure the PDF contains readable text.")
            else:
                st.text_area("Extracted Text Preview", pdf_text[:500] + "...", height=100, disabled=True)
                
                # Fact checking button
                if st.button("🔍 Start Fact-Checking", type="primary"):
                    if not openai_api_key:
                        st.error("❌ Please enter your OpenAI API key in the sidebar.")
                    elif not tavily_api_key:
                        st.error("❌ Please enter your Tavily API key in the sidebar.")
                    else:
                        # Initialize fact checker
                        fact_checker = FactChecker(
                            openai_api_key=openai_api_key,
                            tavily_api_key=tavily_api_key
                        )
                        
                        # Process the document
                        progress_bar = st.progress(0)
                        status_text = st.empty()
                        
                        try:
                            # Extract claims first
                            status_text.text("📝 Extracting claims from document...")
                            claims = fact_checker.extract_claims(pdf_text)
                            
                            if not claims:
                                st.warning("⚠️ No claims were extracted from the document. The document may not contain verifiable factual claims.")
                                st.session_state.results = {'claims': [], 'summary': 'No claims found.'}
                            else:
                                status_text.text(f"🔍 Verifying {len(claims)} claims...")
                                
                                # Verify each claim with progress
                                verified_claims = []
                                for i, claim in enumerate(claims):
                                    progress = (i + 1) / len(claims)
                                    progress_bar.progress(progress)
                                    status_text.text(f"🔍 Verifying claim {i+1}/{len(claims)}: {claim.get('claim_text', '')[:50]}...")
                                    
                                    verified_claim = fact_checker.verify_claim(claim)
                                    verified_claims.append(verified_claim)
                                
                                # Generate summary
                                verified_count = sum(1 for c in verified_claims if c['verification_status'] == 'Verified')
                                inaccurate_count = sum(1 for c in verified_claims if c['verification_status'] == 'Inaccurate')
                                false_count = sum(1 for c in verified_claims if c['verification_status'] == 'False')
                                
                                summary = f"Analyzed {len(verified_claims)} claims: {verified_count} verified, {inaccurate_count} inaccurate, {false_count} false."
                                
                                results = {
                                    'claims': verified_claims,
                                    'summary': summary,
                                    'statistics': {
                                        'total': len(verified_claims),
                                        'verified': verified_count,
                                        'inaccurate': inaccurate_count,
                                        'false': false_count
                                    }
                                }
                                
                                st.session_state.results = results
                                st.session_state.claims = verified_claims
                                
                                progress_bar.progress(1.0)
                                status_text.text("✅ Fact-checking complete!")
                                
                        except Exception as e:
                            st.error(f"❌ Error during fact-checking: {str(e)}")
                            st.exception(e)
                                
        except Exception as e:
            st.error(f"❌ Error reading PDF: {str(e)}")
            st.exception(e)

# Display results
if st.session_state.results:
    st.divider()
    st.header("📊 Fact-Checking Results")
    
    results = st.session_state.results
    claims = results.get('claims', [])
    
    if claims:
        # Summary statistics
        col1, col2, col3, col4 = st.columns(4)
        verified_count = sum(1 for c in claims if c['verification_status'] == 'Verified')
        inaccurate_count = sum(1 for c in claims if c['verification_status'] == 'Inaccurate')
        false_count = sum(1 for c in claims if c['verification_status'] == 'False')
        
        with col1:
            st.metric("Total Claims", len(claims))
        with col2:
            st.metric("✅ Verified", verified_count, delta=None)
        with col3:
            st.metric("⚠️ Inaccurate", inaccurate_count, delta=None)
        with col4:
            st.metric("❌ False", false_count, delta=None)
        
        st.divider()
        
        # Display each claim
        for idx, claim in enumerate(claims, 1):
            status = claim['verification_status']
            
            # Color coding
            if status == 'Verified':
                status_emoji = "✅"
                status_color = "green"
            elif status == 'Inaccurate':
                status_emoji = "⚠️"
                status_color = "orange"
            else:
                status_emoji = "❌"
                status_color = "red"
            
            with st.expander(f"{status_emoji} Claim #{idx}: {claim['claim_text'][:100]}...", expanded=(status != 'Verified')):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown(f"**Claim:** {claim['claim_text']}")
                    st.markdown(f"**Type:** {claim['claim_type']}")
                    
                with col2:
                    st.markdown(f"**Status:** :{status_color}[{status}]")
                
                st.markdown(f"**Explanation:** {claim['explanation']}")
                
                if claim.get('sources'):
                    st.markdown("**Sources:**")
                    for source in claim['sources']:
                        st.markdown(f"- [{source['title']}]({source['url']})")
                
                if claim.get('corrected_value'):
                    st.info(f"**Corrected Value:** {claim['corrected_value']}")
        
        # Download results as JSON
        st.divider()
        json_results = json.dumps(results, indent=2)
        st.download_button(
            label="📥 Download Results as JSON",
            data=json_results,
            file_name="fact_check_results.json",
            mime="application/json"
        )
    else:
        st.warning("No claims were extracted from the document.")

