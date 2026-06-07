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
    ki = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[ki % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
            ki += 1
        else:
            result += char
    return result

def vigenere_decrypt(text, key):
    result = ""
    key = key.upper()
    ki = 0
    for char in text:
        if char.isalpha():
            shift = ord(key[ki % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base - shift) % 26 + base)
            ki += 1
        else:
            result += char
    return result

tests = [
    ("Caesar",   lambda m, k: caesar_encrypt(m, int(k)),   lambda c, k: caesar_decrypt(c, int(k)),   "Hello World",   "3"),
    ("Caesar",   lambda m, k: caesar_encrypt(m, int(k)),   lambda c, k: caesar_decrypt(c, int(k)),   "BIT3208",       "13"),
    ("Vigenere", vigenere_encrypt,                          vigenere_decrypt,                          "Cryptography",  "KEY"),
    ("Vigenere", vigenere_encrypt,                          vigenere_decrypt,                          "SecurityTest",  "BIT"),
]

print(f"{'#':<3} {'Cipher':<10} {'Message':<15} {'Key':<6} {'Encrypted':<20} {'Decrypted':<15} {'Result'}")
print("-" * 80)

for i, (cipher, enc_fn, dec_fn, message, key) in enumerate(tests, 1):
    encrypted = enc_fn(message, key)
    decrypted = dec_fn(encrypted, key)
    result = "PASS" if decrypted == message else "FAIL"
    print(f"{i:<3} {cipher:<10} {message:<15} {key:<6} {encrypted:<20} {decrypted:<15} {result}")
