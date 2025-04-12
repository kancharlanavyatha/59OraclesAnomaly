from config import settings
import re

class IssueClassifier:
    def __init__(self):
        self.keywords = {
            "Technical Support": ["error", "bug", "not working", "broken", "failed", "issue", "problem"],
            "Billing": ["payment", "invoice", "charge", "bill", "subscription", "price", "cost", "refund"],
            "Account Management": ["login", "password", "account", "profile", "settings", "access"],
            "General Inquiry": []  # Default category
        }
        
    def classify_issue(self, text: str) -> str:
        """
        Classify the customer issue into one of the service groups using keyword matching
        """
        text = text.lower()
        
        # Count matches for each category
        matches = {
            category: sum(1 for keyword in keywords if keyword in text)
            for category, keywords in self.keywords.items()
        }
        
        # Return the category with most matches, or General Inquiry if no matches
        max_matches = max(matches.values())
        if max_matches == 0:
            return "General Inquiry"
            
        return max(matches.items(), key=lambda x: x[1])[0] 