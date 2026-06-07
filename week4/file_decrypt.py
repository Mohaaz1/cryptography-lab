from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def aes_decrypt_file(input_path, key):
    with open(input_path, 'rb') as f:
        data = f.read()
    iv = data[:16]
    ciphertext = data[16:]
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    padded = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    plaintext = unpadder.update(padded) + unpadder.finalize()
    return plaintext, iv

with open("encryption_key.bin", "rb") as f:
    key = f.read()

print("=== AES-256-CBC File Decryption ===")
print(f"Encrypted file: sample.enc")
print(f"Key (hex):      {key.hex()[:32]}...")
print()

plaintext, iv = aes_decrypt_file("sample.enc", key)

print(f"IV (hex):       {iv.hex()}")
print(f"Decrypted size: {len(plaintext)} bytes")
print(f"\n--- Decrypted Content ---")
print(plaintext.decode())
print("--- End of Content ---")
print(f"\nStatus: Decryption successful")
