import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

try:
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('wordnet')

class EmailClassifier:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.query_patterns = self.initialize_query_patterns()
        self.response_templates = self.initialize_response_templates()
    
    def initialize_query_patterns(self):
        """Initialize patterns for different types of queries"""
        return {
            'mohak64bansal': [
                r'mohak64bansal\.com'
            ],
            'pricing': [
                r'\b(price|cost|pricing|quote|budget|expensive|cheap|afford)\b',
                r'\b(how much|what.*cost|pricing.*information)\b'
            ],
            'support': [
                r'\b(help|support|issue|problem|bug|error|trouble|stuck)\b',
                r'\b(how to|how do|can.*help|need.*help)\b'
            ],
            'product_info': [
                r'\b(feature|specification|specs|capability|functionality)\b',
                r'\b(what.*do|what.*can|how.*work|tell.*about)\b'
            ],
            'meeting': [
                r'\b(meeting|call|schedule|appointment|demo|presentation)\b',
                r'\b(when.*available|book.*time|set.*up.*meeting)\b'
            ],
            'general_inquiry': [
                r'\b(hello|hi|greetings|good morning|good afternoon)\b',
                r'\b(interested|curious|want.*know|more.*information)\b'
            ]
        }
    
    def initialize_response_templates(self):
        """Initialize response templates for different query types"""
        return {
            'mohak64bansal': """Hello,

I hope you are well, I am Mohak from the miniOrange team, and will be assisting you with your query.
It looks like you want to have a PAM solution for your organization, we do provide this solution.

Before we move forward, could you answer a few questions so that I can get a better understanding of your requirements. 
What are the different applications/devices (Windows, Linux machines, databases, Network devices etc. ) that you want to protect using PAM?
What is the estimated number of users that are going to use our solution?
What specific features or functionalities are you looking for in our product?
You can visit this page to learn more about the PAM capabilities of our product.

If you want, we can have a quick demo to showcase our product. If so, please share your availability and time zone so that I can schedule the call accordingly.
We can also have a demo right now.

Hope to hear from you soon.

Thanks & Regards,
Mohak""",
            'pricing': """Thank you for your interest in our pricing information.

I'd be happy to provide you with detailed pricing options. Our pricing varies based on your specific needs and requirements.

Could you please let me know:
- What type of service/product are you interested in?
- What's your expected timeline?
- Any specific features or requirements?

I'll get back to you with a customized quote within 24 hours.

Best regards,
[Your Name]""",
            
            'support': """Thank you for reaching out for support.

I understand you're experiencing an issue and I'm here to help resolve it quickly.

To better assist you, could you please provide:
- A detailed description of the problem
- Any error messages you're seeing
- Steps you've already tried
- Your system/browser information (if relevant)

I'll investigate this issue and get back to you with a solution as soon as possible.

Best regards,
[Your Name]""",
            
            'product_info': """Thank you for your interest in learning more about our product.

I'd be delighted to provide you with detailed information about our features and capabilities.

Based on your inquiry, here are some key highlights:
- [Feature 1]: [Brief description]
- [Feature 2]: [Brief description]
- [Feature 3]: [Brief description]

Would you like me to schedule a demo or provide more specific information about any particular feature?

Best regards,
[Your Name]""",
            
            'meeting': """Thank you for your interest in scheduling a meeting.

I'd be happy to set up a time to discuss your requirements in detail.

Please let me know your preferred:
- Date and time (with timezone)
- Meeting duration
- Preferred communication method (video call, phone, in-person)
- Any specific topics you'd like to cover

I'll check my availability and confirm the meeting details shortly.

Best regards,
[Your Name]""",
            
            'general_inquiry': """Thank you for reaching out!

I appreciate your interest and would be happy to help with any questions you may have.

Could you please provide a bit more detail about what you're looking for? This will help me give you the most relevant and helpful response.

I'll get back to you as soon as possible.

Best regards,
[Your Name]""",
            
            'default': """Thank you for your email.

I have received your message and will review it carefully. I'll get back to you with a detailed response as soon as possible.

If this is urgent, please don't hesitate to call me directly.

Best regards,
[Your Name]"""
        }
    
    def preprocess_text(self, text):
        """Preprocess text for classification"""
        if not text:
            return ""
        
        # Convert to lowercase
        text = text.lower()
        
        # Remove special characters and digits
        text = re.sub(r'[^a-zA-Z\s]', '', text)
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and lemmatize
        tokens = [self.lemmatizer.lemmatize(token) for token in tokens 
                 if token not in self.stop_words and len(token) > 2]
        
        return ' '.join(tokens)
    
    def classify_email(self, email_subject, email_body, sender_email=None):
        """Classify email based on subject, body content, and sender"""
        # Check sender first for special cases
        if sender_email and 'mohak64bansal@gmail.com' in sender_email.lower():
            # Check if the email contains "query for pam"
            combined_text = f"{email_subject} {email_body}".lower()
            if 'query for pam' in combined_text:
                return 'mohak64bansal'
            else:
                return 'default'  # Skip response for other emails from mohak64bansal@gmail.com
        
        # Combine subject and body
        full_text = f"{email_subject} {email_body}"
        
        # Preprocess text
        processed_text = self.preprocess_text(full_text)
        
        if not processed_text:
            return 'default'
        
        # Check against patterns
        scores = {}
        for category, patterns in self.query_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, processed_text, re.IGNORECASE))
                score += matches
            scores[category] = score
        
        # Find category with highest score
        if scores and max(scores.values()) > 0:
            return max(scores, key=scores.get)
        else:
            return 'default'
    
    def get_response_template(self, category):
        """Get response template for a given category"""
        return self.response_templates.get(category, self.response_templates['default'])
    
    def customize_response(self, template, sender_name=None, specific_details=None):
        """Customize response template with specific details"""
        response = template
        
        # Replace placeholder with sender name if available
        if sender_name:
            response = response.replace('[Your Name]', sender_name)
        
        # Add specific details if provided
        if specific_details:
            response += f"\n\nAdditional Information:\n{specific_details}"
        
        return response
