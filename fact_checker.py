import os
from typing import List, Dict
from openai import OpenAI
import requests
import json


class FactChecker:
    def __init__(self, openai_api_key: str, tavily_api_key: str):
        self.openai_client = OpenAI(api_key=openai_api_key)
        self.tavily_api_key = tavily_api_key
        self.tavily_base_url = "https://api.tavily.com"

    # -------------------------
    # CLAIM EXTRACTION
    # -------------------------
    def extract_claims(self, text: str) -> List[Dict]:
        prompt = (
            "You are a fact-checking assistant.\n\n"
            "Extract ALL sentences from the text below that:\n"
            "- Make a factual assertion\n"
            "- Contain numbers, dates, prices, years, or measurable facts\n\n"
            "Do NOT judge accuracy.\n"
            "Do NOT verify.\n"
            "Return STRICTLY valid JSON as a LIST like this:\n"
            "[\n"
            "  {\n"
            "    \"claim_text\": \"...\",\n"
            "    \"claim_type\": \"general\",\n"
            "    \"key_entities\": []\n"
            "  }\n"
            "]\n\n"
            "Text:\n"
            f"{text[:8000]}"
        )

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Always return valid JSON."},
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

            if isinstance(result, list):
                claims = result
            elif isinstance(result, dict):
                claims = result.get("claims", [])
            else:
                claims = []

            # HARD FALLBACK (never return empty)
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

    # -------------------------
    # WEB SEARCH
    # -------------------------
    def search_web(self, query: str, max_results: int = 5) -> List[Dict]:
        try:
            response = requests.post(
                f"{self.tavily_base_url}/search",
                json={
                    "api_key": self.tavily_api_key,
                    "query": query,
                    "search_depth": "advanced",
                    "include_answer": True,
                    "max_results": max_results
                },
                timeout=10
            )
            response.raise_for_status()
            data = response.json()

            sources = []
            for result in data.get("results", []):
                sources.append({
                    "title": result.get("title", ""),
                    "url": result.get("url", ""),
                    "content": result.get("content", "")
                })

            if data.get("answer"):
                sources.insert(0, {
                    "title": "Tavily Summary",
                    "url": "",
                    "content": data["answer"]
                })

            return sources

        except Exception as e:
            print(f"Error searching web: {e}")
            return []

    # -------------------------
    # CLAIM VERIFICATION
    # -------------------------
    def verify_claim(self, claim: Dict) -> Dict:
        claim_text = claim.get("claim_text", "")
        search_query = claim_text

        sources = self.search_web(search_query)

        if not sources:
            return {
                **claim,
                "verification_status": "False",
                "explanation": "No evidence found.",
                "sources": []
            }

        sources_text = "\n\n".join(
            f"{s['title']} - {s['content'][:500]}"
            for s in sources[:3]
        )

        verification_prompt = (
            "Verify the following claim using the sources below.\n\n"
            f"Claim: {claim_text}\n\n"
            f"Sources:\n{sources_text}\n\n"
            "Return JSON with:\n"
            "- verification_status\n"
            "- explanation\n"
            "- corrected_value (if inaccurate)"
        )

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "Return valid JSON only."},
                    {"role": "user", "content": verification_prompt}
                ],
                temperature=0.2,
                response_format={"type": "json_object"}
            )

            result = json.loads(response.choices[0].message.content)

            return {
                **claim,
                "verification_status": result.get("verification_status", "False"),
                "explanation": result.get("explanation", ""),
                "corrected_value": result.get("corrected_value"),
                "sources": sources
            }

        except Exception as e:
            print(f"Error verifying claim: {e}")
            return {
                **claim,
                "verification_status": "False",
                "explanation": str(e),
                "sources": sources
            }

    # -------------------------
    # DOCUMENT PIPELINE
    # -------------------------
    def process_document(self, text: str) -> Dict:
        """Process a document: extract claims and verify them."""

        claims = self.extract_claims(text)

        if not claims:
            return {"claims": [], "summary": "No claims extracted."}

        verified = [self.verify_claim(c) for c in claims]

        summary = f"Analyzed {len(verified)} claims."

        return {
            "claims": verified,
            "summary": summary
        }

