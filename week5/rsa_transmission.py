from cryptography.hazmat.primitives.asymmetric import padding, rsa
from cryptography.hazmat.primitives import hashes, serialization

with open("private_key.pem", "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)
with open("public_key.pem", "rb") as f:
    public_key = serialization.load_pem_public_key(f.read())

message = b"BIT3208: End-to-end secure transmission test"

print("=== RSA Secure Message Transmission ===\n")
print(f"[SENDER]    Original message: {message.decode()}")

ciphertext = public_key.encrypt(
    message,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print(f"\n[SENDER]    Encrypted with public key")
print(f"[CHANNEL]   Transmitting {len(ciphertext)} bytes...")
print(f"[CHANNEL]   Ciphertext: {ciphertext.hex()[:48]}...")

signature = private_key.sign(
    message,
    padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH
    ),
    hashes.SHA256()
)
print(f"\n[SENDER]    Message signed with private key")
print(f"[SENDER]    Signature: {signature.hex()[:48]}...")

decrypted = private_key.decrypt(
    ciphertext,
    padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(),
        label=None
    )
)
print(f"\n[RECEIVER]  Decrypted: {decrypted.decode()}")

try:
    public_key.verify(
        signature,
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    print(f"[RECEIVER]  Signature verified: VALID")
    print(f"\nStatus: Secure transmission complete")
except Exception as e:
    print(f"[RECEIVER]  Signature INVALID: {e}")
