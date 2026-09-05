import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from qure.utils.image_utils import resize_image, is_image_file

class TestImageUtils(unittest.TestCase):
    def test_resize_image(self):
        resized_path = resize_image("qrcodes/BAHATI_Blaise_qr.png", (200, 200))
        self.assertTrue(resized_path.endswith("_resized.png"))
    
    def test_is_image_file(self):
        self.assertTrue(is_image_file("sample.png"))
        self.assertFalse(is_image_file("sample.txt"))

if __name__ == "__main__":
    unittest.main()
