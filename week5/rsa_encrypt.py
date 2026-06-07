from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

with open("public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

message = b"Secure Message - BIT3208 Cryptography Lab"

ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

with open("ciphertext.bin", "wb") as f:
    f.write(ciphertext)

print("=== RSA Public Key Encryption (OAEP) ===\n")
print(f"Algorithm:   RSA-2048 with OAEP padding")
print(f"Hash:        SHA-256")
print(f"Message:     {message.decode()}")
print(f"Msg length:  {len(message)} bytes")
print(f"\nCiphertext (hex):")
print(ciphertext.hex())
print(f"\nCT length:   {len(ciphertext)} bytes")
print(f"Saved to:    ciphertext.bin")
