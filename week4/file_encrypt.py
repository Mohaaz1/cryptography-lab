from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend
import os

def aes_encrypt_file(input_path, output_path, key):
    iv = os.urandom(16)
    with open(input_path, 'rb') as f:
        plaintext = f.read()
    padder = padding.PKCS7(128).padder()
    padded = padder.update(plaintext) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(padded) + encryptor.finalize()
    with open(output_path, 'wb') as f:
        f.write(iv + ciphertext)
    return iv, len(plaintext), len(ciphertext)

sample = """BIT3208 - Cryptography Lab
Week 4: Block Cipher Design & AES
This is a confidential document encrypted using AES-256-CBC.
Unauthorized parties cannot read this content without the key.
"""

with open("sample.txt", "w") as f:
    f.write(sample)

key = os.urandom(32)

print("=== AES-256-CBC File Encryption ===")
print(f"Input file:  sample.txt")
print(f"Output file: sample.enc")
print(f"Algorithm:   AES-256-CBC")
print(f"Key (hex):   {key.hex()}")
print()

iv, plain_size, cipher_size = aes_encrypt_file("sample.txt", "sample.enc", key)

print(f"Original size:  {plain_size} bytes")
print(f"Encrypted size: {cipher_size + 16} bytes (includes IV)")
print(f"IV (hex):       {iv.hex()}")
print(f"Status:         File encrypted successfully")

with open("encryption_key.bin", "wb") as f:
    f.write(key)
print(f"Key saved to:   encryption_key.bin")
