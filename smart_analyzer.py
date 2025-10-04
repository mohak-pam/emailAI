#!/usr/bin/env python3
"""
Smart Email Thread Analyzer
Advanced fallback system that provides industry-standard analysis without AI dependencies
"""

import re
from typing import List, Dict
from datetime import datetime

class SmartEmailAnalyzer:
    def __init__(self):
        # Industry-standard keywords for classification
        self.error_keywords = [
            'error', 'issue', 'problem', 'failed', 'not working', 'broken', 'bug', 'exception',
            'timeout', 'connection failed', 'authentication failed', 'login failed', 'access denied',
            'configuration error', 'setup failed', 'installation failed', 'sync failed'
        ]
        
        self.urgent_keywords = [
            'urgent', 'critical', 'asap', 'immediately', 'emergency', 'priority', 'high priority',
            'production down', 'system down', 'service unavailable', 'outage', 'incident'
        ]
        
        self.meeting_keywords = [
            'demo', 'meeting', 'call', 'schedule', 'presentation', 'webinar', 'conference',
            'appointment', 'availability', 'calendar', 'zoom', 'teams', 'skype'
        ]
        
        self.support_keywords = [
            'support', 'help', 'assistance', 'ticket', 'case', 'troubleshoot', 'debug',
            'technical support', 'customer service', 'escalation', 'resolution'
        ]
        
        self.sales_keywords = [
            'pricing', 'quote', 'cost', 'budget', 'license', 'subscription', 'renewal',
            'contract', 'proposal', 'deal', 'opportunity', 'lead', 'prospect'
        ]
        
        self.positive_sentiment = [
            'thank', 'thanks', 'appreciate', 'excellent', 'great', 'good', 'perfect',
            'satisfied', 'happy', 'pleased', 'working well', 'successful'
        ]
        
        self.frustrated_sentiment = [
            'frustrated', 'annoyed', 'disappointed', 'unhappy', 'dissatisfied', 'angry',
            'upset', 'concerned', 'worried', 'troubled', 'problematic'
        ]
        
        self.technical_complexity_indicators = [
            'api', 'integration', 'configuration', 'setup', 'installation', 'deployment',
            'database', 'server', 'network', 'security', 'authentication', 'authorization',
            'ldap', 'saml', 'oauth', 'ssl', 'certificate', 'firewall', 'vpn'
        ]
    
    def analyze_email_thread(self, thread_emails: List[Dict]) -> Dict:
        """Analyze email thread using advanced pattern matching and industry standards"""
        if not thread_emails:
            return self._get_default_analysis()
        
        # Combine all email content for analysis
        all_content = self._extract_thread_content(thread_emails)
        
        # Perform comprehensive analysis
        analysis = {
            "executive_summary": self._generate_executive_summary(thread_emails, all_content),
            "type": self._classify_conversation_type(all_content),
            "urgency": self._assess_urgency(all_content),
            "sentiment": self._analyze_sentiment(all_content),
            "issues": self._extract_key_issues(all_content),
            "complexity": self._assess_technical_complexity(all_content),
            "escalation": self._determine_escalation_needed(all_content),
            "response_time": self._determine_response_time(all_content),
            "stakeholders": self._extract_stakeholders(thread_emails),
            "business_impact": self._assess_business_impact(all_content),
            "recommended_actions": self._generate_recommended_actions(all_content)
        }
        
        return analysis
    
    def _extract_thread_content(self, thread_emails: List[Dict]) -> str:
        """Extract and combine all thread content"""
        content_parts = []
        for email in thread_emails:
            content_parts.append(f"{email.get('subject', '')} {email.get('body', '')}")
        return " ".join(content_parts).lower()
    
    def _generate_executive_summary(self, thread_emails: List[Dict], content: str) -> str:
        """Generate executive summary"""
        email_count = len(thread_emails)
        
        if any(word in content for word in self.error_keywords):
            return f"Technical issue requiring resolution in {email_count}-email thread"
        elif any(word in content for word in self.meeting_keywords):
            return f"Meeting/demo scheduling discussion across {email_count} emails"
        elif any(word in content for word in self.sales_keywords):
            return f"Sales/pricing inquiry involving {email_count} email exchanges"
        elif any(word in content for word in self.support_keywords):
            return f"Customer support case with {email_count} email interactions"
        else:
            return f"General business communication spanning {email_count} emails"
    
    def _classify_conversation_type(self, content: str) -> str:
        """Classify conversation type based on content analysis"""
        if any(word in content for word in self.error_keywords):
            return "error"
        elif any(word in content for word in self.meeting_keywords):
            return "meeting"
        elif any(word in content for word in self.support_keywords):
            return "support"
        elif any(word in content for word in self.sales_keywords):
            return "sales"
        else:
            return "general"
    
    def _assess_urgency(self, content: str) -> str:
        """Assess urgency level"""
        urgent_count = sum(1 for word in self.urgent_keywords if word in content)
        error_count = sum(1 for word in self.error_keywords if word in content)
        
        if urgent_count >= 2 or (urgent_count >= 1 and error_count >= 2):
            return "high"
        elif urgent_count >= 1 or error_count >= 2:
            return "medium"
        else:
            return "low"
    
    def _analyze_sentiment(self, content: str) -> str:
        """Analyze customer sentiment"""
        positive_count = sum(1 for word in self.positive_sentiment if word in content)
        frustrated_count = sum(1 for word in self.frustrated_sentiment if word in content)
        
        if frustrated_count > positive_count:
            return "frustrated"
        elif positive_count > frustrated_count:
            return "positive"
        else:
            return "neutral"
    
    def _extract_key_issues(self, content: str) -> List[str]:
        """Extract key issues from content"""
        issues = []
        
        # Look for specific problem patterns
        if 'authentication' in content and ('failed' in content or 'error' in content):
            issues.append("Authentication/Login Issues")
        
        if 'configuration' in content and ('error' in content or 'failed' in content):
            issues.append("Configuration Problems")
        
        if 'sync' in content and ('failed' in content or 'not working' in content):
            issues.append("Data Synchronization Issues")
        
        if 'pricing' in content or 'cost' in content:
            issues.append("Pricing Inquiry")
        
        if 'demo' in content or 'meeting' in content:
            issues.append("Demo/Meeting Request")
        
        if 'support' in content or 'help' in content:
            issues.append("Technical Support Request")
        
        # Extract specific technical terms
        tech_issues = []
        for term in self.technical_complexity_indicators:
            if term in content:
                tech_issues.append(f"{term.upper()} Related")
        
        if tech_issues:
            issues.extend(tech_issues[:3])  # Limit to top 3 technical issues
        
        return issues if issues else ["General Inquiry"]
    
    def _assess_technical_complexity(self, content: str) -> str:
        """Assess technical complexity"""
        tech_terms = sum(1 for term in self.technical_complexity_indicators if term in content)
        
        if tech_terms >= 5:
            return "high"
        elif tech_terms >= 2:
            return "medium"
        else:
            return "low"
    
    def _determine_escalation_needed(self, content: str) -> bool:
        """Determine if escalation is needed"""
        urgent_indicators = any(word in content for word in self.urgent_keywords)
        error_indicators = any(word in content for word in self.error_keywords)
        high_complexity = self._assess_technical_complexity(content) == "high"
        
        return urgent_indicators or (error_indicators and high_complexity)
    
    def _determine_response_time(self, content: str) -> str:
        """Determine expected response time"""
        if any(word in content for word in ['urgent', 'critical', 'asap', 'immediately']):
            return "immediate"
        elif any(word in content for word in ['priority', 'soon', 'quickly']):
            return "4h"
        elif any(word in content for word in self.error_keywords):
            return "24h"
        else:
            return "week"
    
    def _extract_stakeholders(self, thread_emails: List[Dict]) -> List[str]:
        """Extract stakeholders from thread"""
        stakeholders = []
        for email in thread_emails:
            sender = email.get('sender', '')
            if sender and '@' in sender:
                # Extract name from email
                name = sender.split('@')[0].replace('.', ' ').title()
                stakeholders.append(name)
        
        # Remove duplicates and limit to 5
        return list(dict.fromkeys(stakeholders))[:5]
    
    def _assess_business_impact(self, content: str) -> str:
        """Assess business impact"""
        if any(word in content for word in ['production', 'system down', 'outage', 'critical']):
            return "high"
        elif any(word in content for word in ['urgent', 'priority', 'important']):
            return "medium"
        else:
            return "low"
    
    def _generate_recommended_actions(self, content: str) -> List[str]:
        """Generate recommended actions"""
        actions = []
        
        if any(word in content for word in self.error_keywords):
            actions.append("Investigate and diagnose the technical issue")
            actions.append("Provide step-by-step resolution guide")
            actions.append("Schedule follow-up to ensure resolution")
        
        if any(word in content for word in self.meeting_keywords):
            actions.append("Schedule demo/meeting at convenient time")
            actions.append("Prepare relevant materials and agenda")
            actions.append("Send calendar invitation with details")
        
        if any(word in content for word in self.sales_keywords):
            actions.append("Provide detailed pricing information")
            actions.append("Schedule sales call with decision maker")
            actions.append("Prepare customized proposal")
        
        if any(word in content for word in self.support_keywords):
            actions.append("Create support ticket if not already done")
            actions.append("Assign to appropriate technical specialist")
            actions.append("Provide regular status updates")
        
        # Default actions
        if not actions:
            actions = [
                "Review email content thoroughly",
                "Prepare appropriate response",
                "Follow up as needed"
            ]
        
        return actions[:4]  # Limit to 4 actions
    
    def _get_default_analysis(self) -> Dict:
        """Get default analysis for empty threads"""
        return {
            "executive_summary": "Email thread analysis",
            "type": "general",
            "urgency": "low",
            "sentiment": "neutral",
            "issues": ["General inquiry"],
            "complexity": "medium",
            "escalation": False,
            "response_time": "24h",
            "stakeholders": [],
            "business_impact": "low",
            "recommended_actions": ["Review and respond manually"]
        }

# Test the smart analyzer
def test_smart_analyzer():
    """Test smart email analyzer"""
    print("🧠 Testing Smart Email Analyzer")
    print()
    
    analyzer = SmartEmailAnalyzer()
    
    # Test with sample thread
    sample_thread = [
        {
            'sender': 'customer@company.com',
            'subject': 'URGENT: PAM Authentication Failed - Production Down',
            'body': 'Hi, we are experiencing critical authentication failures in our PAM system. Users cannot login and this is affecting our production environment. We need immediate assistance to resolve this issue. The error occurs during LDAP integration setup.',
            'date': '2025-09-22 10:00:00'
        },
        {
            'sender': 'support@xecurify.com',
            'subject': 'Re: URGENT: PAM Authentication Failed - Production Down',
            'body': 'Thank you for reporting this critical issue. We understand the urgency and will prioritize this case. Our technical team is investigating the LDAP configuration problem.',
            'date': '2025-09-22 10:30:00'
        }
    ]
    
    print("📧 Analyzing sample thread...")
    analysis = analyzer.analyze_email_thread(sample_thread)
    
    print("📊 Smart Analysis Results:")
    for key, value in analysis.items():
        if isinstance(value, list):
            print(f"  {key}: {', '.join(value)}")
        else:
            print(f"  {key}: {value}")
    print()

if __name__ == "__main__":
    test_smart_analyzer()

