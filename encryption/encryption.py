from cryptography.fernet import Fernet

def generate_key() -> bytes:
    return Fernet.generate_key()

KEY = b'NYuJyoVOa9qC2H7KGy7xavA-HGswtOsdL1OfjrpGxpk='
cipher = Fernet(KEY)

def encrypt_data(data: str) -> str:

    """
    Encrypts the given string using Fernet encryption.
    :param data: The string to encrypt
    :return: The encrypted string, encoded in base64 format
    """

    encrypted_data = cipher.encrypt(data.encode())
    return encrypted_data.decode()

def decrypt_data(encrypted_data: str) -> str:

    """
    Decrypts the encrypted string back to its original form using Fernet decryption.
    :param encrypted_data: The encrypted string to decrypt (base64 encoded)
    :return: The decrypted string
    """

    decrypted_data = cipher.decrypt(encrypted_data.encode())
    return decrypted_data.decode()

# Example usage:
if __name__ == "__main__":
    original_data = "This is some secret data"
    print(f"Original Data: {original_data}")
    
    encrypted = encrypt_data(original_data)
    print(f"Encrypted Data: {encrypted}")
    
    decrypted = decrypt_data(encrypted)
    print(f"Decrypted Data: {decrypted}")
