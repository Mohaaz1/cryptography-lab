def vigenere_encrypt(text, key):
    result = ""
    key = key.upper()
    key_index = 0
    print(f"\n{'Char':<8} {'Key':<8} {'Shift':<8} {'Output'}")
    print("-" * 35)
    for char in text:
        if char.isalpha():
            shift = ord(key[key_index % len(key)]) - ord('A')
            base = ord('A') if char.isupper() else ord('a')
            enc_char = chr((ord(char) - base + shift) % 26 + base)
            print(f"{char:<8} {key[key_index % len(key)]:<8} {shift:<8} {enc_char}")
            result += enc_char
            key_index += 1
        else:
            result += char
    return result

message = "HELLO BIT"
key = "CRYPTO"

print(f"[MESSAGE]   {message}")
print(f"[KEY]       {key}")
encrypted = vigenere_encrypt(message, key)
print(f"\n[ENCRYPTED] {encrypted}")
