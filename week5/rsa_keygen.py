from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)
public_key = private_key.public_key()

priv_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm=serialization.NoEncryption()
)
pub_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

with open("private_key.pem", "wb") as f:
    f.write(priv_pem)
with open("public_key.pem", "wb") as f:
    f.write(pub_pem)

pub_numbers = public_key.public_key().public_numbers() if hasattr(public_key, 'public_key') else public_key.public_numbers()

print("=== RSA-2048 Key Pair Generation ===\n")
print(f"Key size:        2048 bits")
print(f"Public exponent: {pub_numbers.e}")
print(f"Modulus (n):     {str(pub_numbers.n)[:60]}...")
print(f"\n--- Public Key ---")
print(pub_pem.decode())
print("--- Private Key (first 3 lines) ---")
lines = priv_pem.decode().splitlines()
print('\n'.join(lines[:3]))
print("...")
print(f"\nKeys saved: public_key.pem, private_key.pem")
