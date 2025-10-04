#!/usr/bin/env python3
"""
Gemini Integration for PAM Email Automation
"""

import json
from typing import List, Dict, Optional
import requests
import logging

try:
    import google.generativeai as genai
except Exception:  # Library may not be installed yet
    genai = None  # type: ignore

from config import Config
from smart_analyzer import SmartEmailAnalyzer


class GeminiPAMProcessor:
    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.logger = logging.getLogger(__name__)
        self.api_key = api_key or Config.GEMINI_API_KEY
        self.model_name = model or Config.GEMINI_MODEL
        self._model = None

        if self.api_key and genai is not None:
            try:
                genai.configure(api_key=self.api_key)
                self._model = genai.GenerativeModel(
                    self.model_name,
                    generation_config={
                        "temperature": Config.GEMINI_TEMPERATURE,
                        "top_p": Config.GEMINI_TOP_P,
                        "max_output_tokens": Config.GEMINI_MAX_OUTPUT_TOKENS,
                    }
                )
                self.logger.info(f"Gemini SDK configured with model: {self.model_name}")
            except Exception:
                self.logger.warning("Gemini SDK configuration failed; will use REST fallback if possible")
                self._model = None

        self._fallback = SmartEmailAnalyzer()

    def is_configured(self) -> bool:
        return self._model is not None

    def summarize_pam_thread(self, thread_emails: List[Dict]) -> Dict:
        if not thread_emails:
            return self._fallback._get_default_analysis()

        if not self.is_configured():
            # Try REST fallback if SDK isn't available/working
            prompt = self._build_prompt(thread_emails)
            self.logger.info(f"Gemini REST call: model={self.model_name}, prompt_chars={len(prompt)}")
            rest = self._rest_generate(prompt)
            if rest:
                return rest
            return self._fallback.analyze_email_thread(thread_emails)

        prompt = self._build_prompt(thread_emails)
        self.logger.info(f"Gemini SDK call: model={self.model_name}, prompt_chars={len(prompt)}")

        try:
            response = self._model.generate_content(prompt)  # type: ignore[attr-defined]
            text = getattr(response, 'text', '') or ''
            parsed = self._parse_ai_json(text)
            if not parsed:
                return self._fallback.analyze_email_thread(thread_emails)
            return parsed
        except Exception as e:
            self.logger.error(f"Gemini SDK error: {e}. Falling back to REST.")
            # Try REST fallback once
            rest = self._rest_generate(prompt)
            if rest:
                return rest
            return self._fallback.analyze_email_thread(thread_emails)

    def generate_support_reply(self, latest_email: Dict, thread_emails: List[Dict]) -> Optional[str]:
        """Generate a customer-support-ready reply draft using Gemini. Returns None on failure."""
        if not thread_emails:
            thread_emails = [latest_email]
        prompt = self._build_reply_prompt(latest_email, thread_emails)

        # Prefer SDK if available, otherwise REST
        if self.is_configured():
            self.logger.info(f"Gemini SDK reply call: model={self.model_name}, prompt_chars={len(prompt)}")
            try:
                response = self._model.generate_content(prompt)  # type: ignore[attr-defined]
                text = getattr(response, 'text', '') or ''
                return self._extract_reply_text(text)
            except Exception as e:
                self.logger.error(f"Gemini SDK reply error: {e}. Falling back to REST.")

        self.logger.info(f"Gemini REST reply call: model={self.model_name}, prompt_chars={len(prompt)}")
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
            payload = {
                "contents": [
                    {"parts": [{"text": prompt}]}
                ],
                "generationConfig": {
                    "temperature": Config.GEMINI_TEMPERATURE,
                    "topP": Config.GEMINI_TOP_P,
                    "maxOutputTokens": Config.GEMINI_MAX_OUTPUT_TOKENS
                }
            }
            resp = requests.post(url, json=payload, timeout=30)
            if resp.status_code != 200:
                try:
                    err = resp.json()
                except Exception:
                    err = {"text": resp.text}
                self.logger.error(f"Gemini REST reply error: status={resp.status_code} body={err}")
                return None
            data = resp.json()
            text = ""
            for cand in (data.get("candidates") or []):
                parts = cand.get("content", {}).get("parts", [])
                for part in parts:
                    if "text" in part:
                        text += part["text"]
            return self._extract_reply_text(text)
        except Exception as e:
            self.logger.error(f"Gemini REST reply exception: {e}")
            return None

    def _build_reply_prompt(self, latest_email: Dict, thread_emails: List[Dict]) -> str:
        thread_text = self._prepare_thread(thread_emails)
        latest_text = f"Subject: {latest_email.get('subject','')}\nFrom: {latest_email.get('sender','')}\nBody: {latest_email.get('body','')}"
        return f"""
You are a senior customer support specialist. Read the entire email thread and compose a concise, professional, helpful reply.

Requirements:
- Be empathetic and professional.
- Address the user's specific concern.
- If follow-up info is needed, ask 2-4 precise questions.
- Offer next steps and realistic timelines when applicable.
- Keep it under 180 words.
- Do not include any JSON or meta commentary.
- Do NOT include any sign-off, name, job title, or company signature. The system will append those.
Output only the email body text to send (without signature).

Latest Email:
{latest_text}

Thread Context:
{thread_text}
"""

    def _extract_reply_text(self, text: str) -> Optional[str]:
        if not text:
            return None
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`").strip()
            if cleaned.lower().startswith("text"):
                cleaned = cleaned[4:].strip()
        # Basic sanity: require at least a sentence and some alphabetic chars
        if len(cleaned) < 40 or not any(c.isalpha() for c in cleaned):
            return None
        return cleaned

    def _rest_generate(self, prompt: str) -> Optional[Dict]:
        if not self.api_key:
            return None
        try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model_name}:generateContent?key={self.api_key}"
            payload = {
                "contents": [
                    {"parts": [{"text": prompt}]}
                ],
                "generationConfig": {
                    "temperature": Config.GEMINI_TEMPERATURE,
                    "topP": Config.GEMINI_TOP_P,
                    "maxOutputTokens": Config.GEMINI_MAX_OUTPUT_TOKENS
                }
            }
            resp = requests.post(url, json=payload, timeout=30)
            if resp.status_code != 200:
                try:
                    err = resp.json()
                except Exception:
                    err = {"text": resp.text}
                self.logger.error(f"Gemini REST error: status={resp.status_code} body={err}")
                return None
            data = resp.json()
            # Extract text from candidates
            text = ""
            for cand in (data.get("candidates") or []):
                parts = cand.get("content", {}).get("parts", [])
                for part in parts:
                    if "text" in part:
                        text += part["text"]
            parsed = self._parse_ai_json(text)
            return parsed
        except Exception as e:
            self.logger.error(f"Gemini REST exception: {e}")
            return None

    def _build_prompt(self, thread_emails: List[Dict]) -> str:
        thread_text = self._prepare_thread(thread_emails)
        return f"""
You are an assistant analyzing a professional email thread about Privileged Access Management (PAM).
Return ONLY valid JSON (no prose) with this exact schema and keys:
{{
  "executive_summary": string,
  "type": "error"|"meeting"|"support"|"sales"|"general",
  "urgency": "low"|"medium"|"high",
  "sentiment": "positive"|"neutral"|"frustrated",
  "issues": [string],
  "complexity": "low"|"medium"|"high",
  "escalation": true|false,
  "response_time": "immediate"|"4h"|"24h"|"week",
  "stakeholders": [string],
  "business_impact": "low"|"medium"|"high",
  "recommended_actions": [string]
}}

Email Thread:
{thread_text}
"""

    def _prepare_thread(self, thread_emails: List[Dict]) -> str:
        # Limit number of emails and total characters to control cost
        limited = thread_emails[-Config.MAX_THREAD_EMAILS:] if len(thread_emails) > Config.MAX_THREAD_EMAILS else thread_emails
        parts = []
        for i, email in enumerate(limited, 1):
            parts.append(
                f"Email {i}:\nFrom: {email.get('sender','Unknown')}\nSubject: {email.get('subject','No Subject')}\nBody: {email.get('body','')}\nDate: {email.get('date','Unknown')}\n"
            )
        return "\n\n".join(parts)[: Config.MAX_THREAD_CHARS]

    def _parse_ai_json(self, text: str) -> Optional[Dict]:
        if not text:
            return None
        # Strip code fences if present
        cleaned = text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.strip("`")
            # Remove possible language hints like json
            if cleaned.lower().startswith("json"):
                cleaned = cleaned[4:]
        cleaned = cleaned.strip()

        try:
            data = json.loads(cleaned)
            return self._normalize_schema(data)
        except Exception:
            # Try to find first/last braces as a fallback
            try:
                start = cleaned.find('{')
                end = cleaned.rfind('}')
                if start != -1 and end != -1 and end > start:
                    data = json.loads(cleaned[start:end + 1])
                    return self._normalize_schema(data)
            except Exception:
                return None
        return None

    def _normalize_schema(self, data: Dict) -> Dict:
        # Ensure all expected keys exist with sensible defaults
        return {
            "executive_summary": data.get("executive_summary") or data.get("summary") or "Email thread analysis",
            "type": data.get("type") or data.get("conversation_type") or "general",
            "urgency": data.get("urgency") or data.get("urgency_level") or "low",
            "sentiment": data.get("sentiment") or data.get("customer_sentiment") or "neutral",
            "issues": data.get("issues") or data.get("key_issues") or ["General inquiry"],
            "complexity": data.get("complexity") or data.get("technical_complexity") or "medium",
            "escalation": bool(data.get("escalation") if data.get("escalation") is not None else data.get("escalation_needed", False)),
            "response_time": data.get("response_time") or (data.get("key_metrics", {}).get("response_time_expected") if isinstance(data.get("key_metrics"), dict) else None) or "24h",
            "stakeholders": data.get("stakeholders") or data.get("stakeholders_involved") or [],
            "business_impact": data.get("business_impact") or "low",
            "recommended_actions": data.get("recommended_actions") or ["Review and respond manually"]
        }


# Simple smoke test
def test_gemini_integration():
    print("🤖 Testing Gemini PAM Integration")
    processor = GeminiPAMProcessor()
    result = processor.summarize_pam_thread([
        {"sender": "user@example.com", "subject": "PAM configuration help", "body": "Need assistance setting up LDAP.", "date": "2025-10-04"}
    ])
    print("Result keys:", list(result.keys()))

if __name__ == "__main__":
    test_gemini_integration()


