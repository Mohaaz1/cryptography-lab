from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization

with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

with open("ciphertext.bin", "rb") as f:
    ciphertext = f.read()

plaintext = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)

print("=== RSA Private Key Decryption ===\n")
print(f"Ciphertext (hex): {ciphertext.hex()[:64]}...")
print(f"CT length:        {len(ciphertext)} bytes")
print(f"\nDecrypted message: {plaintext.decode()}")
print(f"Msg length:        {len(plaintext)} bytes")
print(f"\nStatus: Decryption successful")
