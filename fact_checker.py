import os
from typing import List, Dict, Optional
from openai import OpenAI
import requests
import json

class FactChecker:
    def __init__(self, openai_api_key: str, tavily_api_key: str):
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.tavily_api_key = tavily_api_key
        self.tavily_base_url = "https://api.tavily.com"
    
    def extract_claims(self, text: str) -> List[Dict]:
        """Extract specific claims from the text using OpenAI."""
        prompt = f"""
You are a fact-checking assistant.

Extract ALL sentences from the text below that:
- Make a factual assertion
- Contain numbers, dates, prices, years, or measurable facts

Do NOT judge accuracy.
Do NOT verify.
Do NOT filter aggressively.

Return STRICTLY valid JSON in this format:
[
  {{
    "claim_text": "...",
    "claim_type": "general",
    "key_entities": []
  }}
]

Text:
{text[:8000]}
"""

        
Focus on:
- Statistics and numbers (GDP, population, percentages, financial figures)
- Dates and historical events
- Technical specifications
- Scientific facts and research findings
- Financial data (stock prices, market caps, revenue)
- Demographic data
- Any factual assertions that can be verified

For each claim, provide:
1. The exact claim text
2. The type of claim (statistic, date, financial, technical, etc.)
3. The key entities or numbers mentioned

Return a JSON object with a "claims" array, where each claim has:
- "claim_text": the exact text of the claim
- "claim_type": the type (e.g., "statistic", "date", "financial", "technical")
- "key_entities": list of key entities/numbers mentioned

Text to analyze:
{text[:8000]}  # Limit to avoid token limits

Return valid JSON only, no markdown formatting."""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a precise fact-checking assistant. Always return valid JSON with a 'claims' array."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                response_format={"type": "json_object"}
            )
            
            raw = response.choices[0].message.content.strip()

try:
    result = json.loads(raw)
except Exception:
    result = []

# Case 1: Model returned a list (preferred)
if isinstance(result, list):
    claims = result

# Case 2: Model returned {"claims": [...]}
elif isinstance(result, dict):
    claims = result.get("claims", [])

else:
    claims = []

# 🔐 HARD FALLBACK — never silently return empty
if not claims:
    claims = [
        {
            "claim_text": line.strip(),
            "claim_type": "general",
            "key_entities": []
        }
        for line in text.split("\n")
        if any(char.isdigit() for char in line)
    ]

return claims[:20]
  
            
        except Exception as e:
            print(f"Error extracting claims: {e}")
            return []
    
    def search_web(self, query: str, max_results: int = 5) -> List[Dict]:
        """Search the web using Tavily API."""
        try:
            response = requests.post(
                f"{self.tavily_base_url}/search",
                json={
                    "api_key": self.tavily_api_key,
                    "query": query,
                    "search_depth": "advanced",
                    "include_answer": True,
                    "include_raw_content": False,
                    "max_results": max_results
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            sources = []
            for result in data.get('results', []):
                sources.append({
                    'title': result.get('title', ''),
                    'url': result.get('url', ''),
                    'content': result.get('content', '')
                })
            
            # Include answer if available
            if data.get('answer'):
                sources.insert(0, {
                    'title': 'Tavily Summary',
                    'url': '',
                    'content': data['answer']
                })
            
            return sources
            
        except Exception as e:
            print(f"Error searching web: {e}")
            return []
    
    def verify_claim(self, claim: Dict) -> Dict:
        """Verify a single claim against web search results."""
        claim_text = claim.get('claim_text', '')
        claim_type = claim.get('claim_type', 'general')
        
        # Create search query
        key_entities = claim.get('key_entities', [])
        if isinstance(key_entities, list):
            entities_str = " ".join(str(e) for e in key_entities)
        else:
            entities_str = str(key_entities)
        search_query = f"{claim_text} {entities_str}".strip()
        
        # Search the web
        sources = self.search_web(search_query, max_results=5)
        
        if not sources:
            return {
                **claim,
                'verification_status': 'False',
                'explanation': 'No evidence found in web search. The claim could not be verified.',
                'sources': []
            }
        
        # Use LLM to analyze search results
        sources_text = "\n\n".join([
            f"Source: {s['title']}\nURL: {s['url']}\nContent: {s['content'][:500]}"
            for s in sources[:3]
        ])
        
        verification_prompt = f"""You are a fact-checking expert. Analyze the following claim against the provided web search results.

Claim: {claim_text}
Claim Type: {claim_type}

Web Search Results:
{sources_text}

Determine if the claim is:
1. "Verified" - The claim matches the information found in reliable sources
2. "Inaccurate" - The claim is partially true but contains outdated or incorrect data (provide the correct value)
3. "False" - The claim contradicts reliable sources or no evidence supports it

Return a JSON object with:
- "verification_status": one of "Verified", "Inaccurate", or "False"
- "explanation": a brief explanation of your verdict
- "corrected_value": (only if status is "Inaccurate") the correct/updated value

Return valid JSON only."""

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a precise fact-checking expert. Always return valid JSON."},
                    {"role": "user", "content": verification_prompt}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            
            verification_result = json.loads(response.choices[0].message.content)
            
            return {
                **claim,
                'verification_status': verification_result.get('verification_status', 'False'),
                'explanation': verification_result.get('explanation', 'Could not verify claim.'),
                'corrected_value': verification_result.get('corrected_value', None),
                'sources': sources
            }
            
        except Exception as e:
            print(f"Error verifying claim: {e}")
            return {
                **claim,
                'verification_status': 'False',
                'explanation': f'Error during verification: {str(e)}',
                'sources': sources
            }
    
    def process_document(self, text: str) -> Dict:
        """Process a document: extract claims and verify them."""
        # Extract claims
        claims = self.extract_claims(text)
        
        if not claims:
            return {
                'claims': [],
                'summary': 'No claims were extracted from the document.'
            }
        
        # Verify each claim
        verified_claims = []
        for i, claim in enumerate(claims):
            print(f"Verifying claim {i+1}/{len(claims)}: {claim.get('claim_text', '')[:50]}...")
            verified_claim = self.verify_claim(claim)
            verified_claims.append(verified_claim)
        
        # Generate summary
        verified_count = sum(1 for c in verified_claims if c['verification_status'] == 'Verified')
        inaccurate_count = sum(1 for c in verified_claims if c['verification_status'] == 'Inaccurate')
        false_count = sum(1 for c in verified_claims if c['verification_status'] == 'False')
        
        summary = f"Analyzed {len(verified_claims)} claims: {verified_count} verified, {inaccurate_count} inaccurate, {false_count} false."
        
        return {
            'claims': verified_claims,
            'summary': summary,
            'statistics': {
                'total': len(verified_claims),
                'verified': verified_count,
                'inaccurate': inaccurate_count,
                'false': false_count
            }
        }

