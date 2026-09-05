import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from qure.scanner.scanner import QRScanner

class TestQRScanner(unittest.TestCase):
    def test_scan_qr(self):
        scanner = QRScanner(key="NYuJyoVOa9qC2H7KGy7xavA-HGswtOsdL1OfjrpGxpk=")
        data = scanner.scan("qrcodes/BAHATI_Blaise_qr.png", decrypt=True)
        self.assertIsInstance(data, dict)
        self.assertIn("name", data)

if __name__ == "__main__":
    unittest.main()
