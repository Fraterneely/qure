import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
import json
from qure.generation.generator import CGenerator

class TestQRGenerator(unittest.TestCase):
    def test_generate_single_qr(self):
        data = {"name": "Test User", "id": "12345"}
        generator = CGenerator(data)
        qr_path = generator.generate()
        self.assertIsNotNone(qr_path)
    
    def test_generate_multiple_qrs(self):
        json_data = [
            {"name": "Alice", "id": "1001"},
            {"name": "Bob", "id": "1002"}
        ]
        with open("test_data.json", "w") as f:
            json.dump(json_data, f)
        
        generator = CGenerator("test_data.json", multiple=True)
        qr_paths = generator.generate()
        self.assertEqual(len(qr_paths), 2)

if __name__ == "__main__":
    unittest.main()
