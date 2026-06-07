from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)

message = b"Cryptography Week 1 - BIT Environment Test"

token = cipher.encrypt(message)
print(f"[KEY]       {key.decode()}")
print(f"[ORIGINAL]  {message.decode()}")
print(f"[ENCRYPTED] {token.decode()}")

decrypted = cipher.decrypt(token)
print(f"[DECRYPTED] {decrypted.decode()}")
