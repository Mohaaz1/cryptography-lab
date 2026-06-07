from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization

def generate_keypair(size=2048):
    priv = rsa.generate_private_key(public_exponent=65537, key_size=size)
    return priv, priv.public_key()

def rsa_encrypt(pub, msg):
    return pub.encrypt(msg, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(), label=None))

def rsa_decrypt(priv, ct):
    return priv.decrypt(ct, padding.OAEP(
        mgf=padding.MGF1(algorithm=hashes.SHA256()),
        algorithm=hashes.SHA256(), label=None))

def rsa_sign(priv, msg):
    return priv.sign(msg, padding.PSS(
        mgf=padding.MGF1(hashes.SHA256()),
        salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())

def rsa_verify(pub, sig, msg):
    try:
        pub.verify(sig, msg, padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH), hashes.SHA256())
        return True
    except:
        return False

priv, pub = generate_keypair()

tests = [
    ("Encrypt/Decrypt",     b"Hello RSA"),
    ("Encrypt/Decrypt",     b"BIT3208 Cryptography"),
    ("Encrypt/Decrypt",     b"Public Key Test Case"),
    ("Sign/Verify",         b"Signed Message BIT"),
    ("Tamper Detection",    b"Original Message"),
]

print("=== RSA Validation Test Suite ===\n")
print(f"{'#':<4} {'Test Type':<20} {'Message':<25} {'Result'}")
print("-" * 65)

for i, (test_type, message) in enumerate(tests, 1):
    if test_type == "Encrypt/Decrypt":
        ct = rsa_encrypt(pub, message)
        pt = rsa_decrypt(priv, ct)
        result = "PASS" if pt == message else "FAIL"
    elif test_type == "Sign/Verify":
        sig = rsa_sign(priv, message)
        result = "PASS" if rsa_verify(pub, sig, message) else "FAIL"
    elif test_type == "Tamper Detection":
        sig = rsa_sign(priv, message)
        tampered = b"Tampered Message"
        result = "PASS" if not rsa_verify(pub, sig, tampered) else "FAIL"
    print(f"{i:<4} {test_type:<20} {message.decode():<25} {result}")

print(f"\nAll tests completed.")
