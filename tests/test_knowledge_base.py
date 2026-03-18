import unittest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from interface.main import load_engine, solve_by_issue, solve_by_text

class TestKnowledgeBase(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Load the Prolog engine once for all the rule validation tests."""
        cls.engine = load_engine()

    def test_known_issue_resolution(self):
        """Test that a specific issue atom returns the correct solution string."""
        message = solve_by_issue(self.engine, "login_issue")
        self.assertIn("Reset your password", message)

    def test_keyword_diagnosis(self):
        """Test that free text containing keywords triggers the right rule."""
        # 'password' is a keyword for login_issue
        message_login = solve_by_text(self.engine, "I forgot my password")
        self.assertIn("Reset your password", message_login)
        
        # 'late' is a keyword for order_delayed
        message_delayed = solve_by_text(self.engine, "Why is my shipment late")
        self.assertIn("Your order is in transit", message_delayed)

    def test_unknown_issue_escalation(self):
        """Test that text without known keywords hits the fallback escalation rule."""
        message = solve_by_text(self.engine, "I just want to say hello")
        self.assertIn("escalate to a human support agent", message)

if __name__ == '__main__':
    unittest.main()