import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import unittest
from qure.encryption.encryption import encrypt_data, decrypt_data

class TestEncryption(unittest.TestCase):
    def test_encrypt_decrypt_data(self):
        data = "Test data for encryption"
        encrypted_data = encrypt_data(data)
        self.assertNotEqual(data, encrypted_data)
        
        decrypted_data = decrypt_data(encrypted_data)
        self.assertEqual(data, decrypted_data)

if __name__ == "__main__":
    unittest.main()
