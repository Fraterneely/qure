from .encryption import encrypt_data, decrypt_data, generate_key

# Expose the encryption functions to the library's public API
__all__ = ["encrypt_data", "decrypt_data", "generate_key"]
