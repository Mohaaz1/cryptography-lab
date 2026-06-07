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

message = "Cryptography BIT3208"
shift = 7

encrypted = caesar_encrypt(message, shift)
decrypted = caesar_decrypt(encrypted, shift)

print(f"[ORIGINAL]  {message}")
print(f"[SHIFT]     {shift}")
print(f"[ENCRYPTED] {encrypted}")
print(f"[DECRYPTED] {decrypted}")
