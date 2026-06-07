def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def caesar_decrypt(text, shift):
    return caesar_encrypt(text, -shift)

def vigenere_encrypt(text, key):
    result = ""
    key = key.upper()
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
            key_index += 1
        else:
            result += char
    return result

def vigenere_decrypt(text, key):
    result = ""
    key = key.upper()
    key_index = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - shift) % 26 + base)
            key_index += 1
        else:
            result += char
    return result

message = "BIT Cryptography Lab"
shift = 5
key = "SECRET"

print("=== Caesar Cipher ===")
enc = caesar_encrypt(message, shift)
dec = caesar_decrypt(enc, shift)
print(f"Original:  {message}")
print(f"Encrypted: {enc}")
print(f"Decrypted: {dec}")

print("\n=== Vigenere Cipher ===")
venc = vigenere_encrypt(message, key)
vdec = vigenere_decrypt(venc, key)
print(f"Original:  {message}")
print(f"Encrypted: {venc}")
print(f"Decrypted: {vdec}")
