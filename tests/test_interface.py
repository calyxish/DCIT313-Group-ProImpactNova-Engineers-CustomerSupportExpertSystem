import unittest
import sys
import os

# Add project root to path so we can import the interface
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from interface.main import atom_to_label, normalize_text

class TestInterfaceLogic(unittest.TestCase):
    
    def test_atom_to_label(self):
        """Test that Prolog atoms are correctly converted to UI labels."""
        self.assertEqual(atom_to_label("login_issue"), "Login Issue")
        self.assertEqual(atom_to_label("no_internet_connection"), "No Internet Connection")
        
    def test_normalize_text(self):
        """Test that user input is properly cleaned for Prolog keyword matching."""
        # Tests replacing hyphens, stripping apostrophes, and lowercasing
        self.assertEqual(normalize_text("Can't login"), "cant_login")
        self.assertEqual(normalize_text("order-delayed"), "order_delayed")
        self.assertEqual(normalize_text("Billing/Invoice"), "billing_invoice")

if __name__ == '__main__':
    unittest.main()