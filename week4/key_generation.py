import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes

print("=== AES Key Generation ===\n")

for bits in [128, 192, 256]:
    key = os.urandom(bits // 8)
    print(f"AES-{bits}:")
    print(f"  Hex:    {key.hex()}")
    print(f"  Length: {len(key)} bytes ({len(key)*8} bits)")
    print()

print("=== Password-Based Key Derivation (PBKDF2) ===")
password = b"BIT3208SecurePassword"
salt = os.urandom(16)
kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000)
derived_key = kdf.derive(password)

print(f"Password:    {password.decode()}")
print(f"Salt (hex):  {salt.hex()}")
print(f"Iterations:  100,000")
print(f"Derived Key: {derived_key.hex()}")
print(f"Key Length:  {len(derived_key)*8} bits")
