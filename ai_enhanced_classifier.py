#!/usr/bin/env python3
"""
AI-Enhanced Email Classifier with Thread Summarization
"""

import re
import json
import requests
from typing import List, Dict, Optional
from email_classifier import EmailClassifier

class AIEnhancedClassifier(EmailClassifier):
    def __init__(self, use_ai=True, ai_provider="gemini"):
        super().__init__()
        self.use_ai = use_ai
        self.ai_provider = ai_provider
        self.pam_patterns = self._load_pam_patterns()
        
    def _load_pam_patterns(self):
        """Load PAM-specific patterns for better classification"""
        return {
            'error_patterns': [
                r'error|issue|problem|failed|not working|troubleshoot',
                r'configuration|config|setup|install|deploy',
                r'access denied|permission|authentication|login',
                r'connection|timeout|network|server'
            ],
            'meeting_patterns': [
                r'demo|meeting|call|schedule|calendar',
                r'available|time|zoom|teams|webex',
                r'presentation|showcase|walkthrough'
            ],
            'configuration_patterns': [
                r'configure|setup|install|deploy|implementation',
                r'integration|api|saml|ldap|ad',
                r'documentation|guide|manual|steps'
            ]
        }
    
    def analyze_thread_with_ai(self, thread_emails: List[Dict]) -> Dict:
        """Enhanced thread analysis using AI"""
        if not self.use_ai or len(thread_emails) < 2:
            return self.analyze_thread_context(thread_emails)
        
        # Prepare thread data for AI analysis
        thread_text = self._prepare_thread_for_ai(thread_emails)
        
        # Get AI summary
        ai_summary = self._get_ai_summary(thread_text)
        
        # Combine with traditional analysis
        traditional_analysis = self.analyze_thread_context(thread_emails)
        
        # Merge results
        enhanced_analysis = {
            **traditional_analysis,
            'ai_summary': ai_summary,
            'conversation_type': self._classify_conversation_type(thread_text),
            'urgency_level': self._assess_urgency(thread_text),
            'next_steps': self._suggest_next_steps(thread_text, ai_summary)
        }
        
        return enhanced_analysis
    
    def _prepare_thread_for_ai(self, thread_emails: List[Dict]) -> str:
        """Prepare thread data for AI processing"""
        thread_data = []
        
        for email in thread_emails:
            email_data = {
                'sender': email.get('sender', ''),
                'subject': email.get('subject', ''),
                'body': email.get('body', ''),
                'date': email.get('date', '')
            }
            thread_data.append(email_data)
        
        return json.dumps(thread_data, indent=2)
    
    def _get_ai_summary(self, thread_text: str) -> str:
        """Get AI-powered thread summary"""
        if self.ai_provider == "gemini":
            return self._gemini_summary(thread_text)
        elif self.ai_provider == "huggingface":
            return self._huggingface_summary(thread_text)
        else:
            return "AI summary not available"
    
    def _gemini_summary(self, thread_text: str) -> str:
        """Generate summary using Gemini (cloud)"""
        try:
            from gemini_integration import GeminiPAMProcessor
            processor = GeminiPAMProcessor()
            # Convert thread_text back to minimal structure for processor
            try:
                thread_emails = json.loads(thread_text)
                if isinstance(thread_emails, list):
                    analysis = processor.summarize_pam_thread(thread_emails)
                else:
                    analysis = None
            except Exception:
                analysis = None
            return analysis or "AI summary not available"
        except Exception as e:
            return f"AI summary error: {str(e)}"
    
    def _huggingface_summary(self, thread_text: str) -> str:
        """Generate summary using Hugging Face transformers"""
        # Implementation would use Hugging Face API
        return "Hugging Face summary not implemented yet"
    
    def _classify_conversation_type(self, thread_text: str) -> str:
        """Classify the type of conversation"""
        text_lower = thread_text.lower()
        
        if any(pattern in text_lower for pattern in self.pam_patterns['error_patterns']):
            return "Error Resolution"
        elif any(pattern in text_lower for pattern in self.pam_patterns['meeting_patterns']):
            return "Meeting/Demo Scheduling"
        elif any(pattern in text_lower for pattern in self.pam_patterns['configuration_patterns']):
            return "Configuration/Setup"
        else:
            return "General Discussion"
    
    def _assess_urgency(self, thread_text: str) -> str:
        """Assess urgency level of the conversation"""
        text_lower = thread_text.lower()
        
        high_urgency_keywords = ['urgent', 'critical', 'asap', 'immediately', 'emergency']
        medium_urgency_keywords = ['soon', 'quickly', 'priority', 'important']
        
        if any(keyword in text_lower for keyword in high_urgency_keywords):
            return "High"
        elif any(keyword in text_lower for keyword in medium_urgency_keywords):
            return "Medium"
        else:
            return "Low"
    
    def _suggest_next_steps(self, thread_text: str, ai_summary: str) -> List[str]:
        """Suggest next steps based on conversation analysis"""
        text_lower = thread_text.lower()
        next_steps = []
        
        if 'demo' in text_lower or 'meeting' in text_lower:
            next_steps.append("Schedule demo call")
        
        if 'trial' in text_lower or 'test' in text_lower:
            next_steps.append("Provide trial access")
        
        if 'pricing' in text_lower or 'cost' in text_lower:
            next_steps.append("Prepare detailed pricing proposal")
        
        if 'error' in text_lower or 'issue' in text_lower:
            next_steps.append("Provide technical support")
        
        if 'configuration' in text_lower or 'setup' in text_lower:
            next_steps.append("Share configuration documentation")
        
        return next_steps if next_steps else ["Follow up with general information"]
    
    def generate_ai_enhanced_response(self, template: str, thread_info: Dict, current_email: Dict) -> str:
        """Generate AI-enhanced contextual response"""
        response = template
        
        if thread_info and thread_info.get('ai_summary'):
            response += f"\n\n--- AI-Enhanced Thread Analysis ---\n"
            
            # Add conversation type
            if 'conversation_type' in thread_info:
                response += f"Conversation Type: {thread_info['conversation_type']}\n"
            
            # Add urgency level
            if 'urgency_level' in thread_info:
                response += f"Urgency Level: {thread_info['urgency_level']}\n"
            
            # Add AI summary
            if isinstance(thread_info['ai_summary'], dict):
                response += f"AI Summary: {json.dumps(thread_info['ai_summary'], indent=2)}\n"
            else:
                response += f"AI Summary: {thread_info['ai_summary']}\n"
            
            # Add suggested next steps
            if 'next_steps' in thread_info:
                response += f"Suggested Next Steps: {', '.join(thread_info['next_steps'])}\n"
        
        return response

# Example usage and testing
def test_ai_enhanced_classifier():
    """Test the AI-enhanced classifier"""
    print("🤖 Testing AI-Enhanced Email Classifier")
    print()
    
    classifier = AIEnhancedClassifier(use_ai=True, ai_provider="gemini")
    
    # Test thread
    thread_emails = [
        {
            'id': '1',
            'sender': 'customer@company.com',
            'subject': 'PAM Configuration Issue',
            'body': 'Hi, we are having trouble configuring the PAM solution. Getting authentication errors.',
            'date': '2025-09-22 10:00:00'
        },
        {
            'id': '2', 
            'sender': 'mohak64bansal@gmail.com',
            'subject': 'Re: PAM Configuration Issue',
            'body': 'This is a query for PAM solution. Can you help us resolve the configuration issues?',
            'date': '2025-09-22 11:00:00'
        }
    ]
    
    # Analyze thread
    thread_info = classifier.analyze_thread_with_ai(thread_emails)
    
    print("📊 Enhanced Thread Analysis:")
    print(f"Conversation Type: {thread_info.get('conversation_type', 'N/A')}")
    print(f"Urgency Level: {thread_info.get('urgency_level', 'N/A')}")
    print(f"Next Steps: {thread_info.get('next_steps', [])}")
    print()
    
    # Generate response
    template = "Thank you for your inquiry. We'll help you resolve this issue."
    response = classifier.generate_ai_enhanced_response(template, thread_info, thread_emails[-1])
    
    print("📝 AI-Enhanced Response:")
    print(response)

if __name__ == "__main__":
    test_ai_enhanced_classifier()

