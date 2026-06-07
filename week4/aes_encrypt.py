from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

def aes_encrypt(plaintext, key, iv):
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext.encode()) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(padded) + encryptor.finalize()

key = os.urandom(32)
iv  = os.urandom(16)
message = "AES Encryption - BIT3208 Cryptography Lab"

ciphertext = aes_encrypt(message, key, iv)

print("=== AES-256-CBC Encryption ===")
print(f"Message:    {message}")
print(f"Key (hex):  {key.hex()}")
print(f"IV  (hex):  {iv.hex()}")
print(f"Key size:   {len(key)*8} bits")
print(f"Ciphertext: {ciphertext.hex()}")
print(f"CT length:  {len(ciphertext)} bytes")
