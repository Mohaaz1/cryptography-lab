def rc4_ksa(key):
    key_bytes = [ord(c) for c in key]
    S = list(range(256))
    j = 0
    for i in range(256):
        j = (j + S[i] + key_bytes[i % len(key_bytes)]) % 256
        S[i], S[j] = S[j], S[i]
    return S

def rc4_prga(S, length):
    i = j = 0
    keystream = []
    S = S.copy()
    for _ in range(length):
        i = (i + 1) % 256
        j = (j + S[i]) % 256
        S[i], S[j] = S[j], S[i]
        keystream.append(S[(S[i] + S[j]) % 256])
    return keystream

def rc4_encrypt(plaintext, key):
    S = rc4_ksa(key)
    keystream = rc4_prga(S, len(plaintext))
    ciphertext = [ord(p) ^ k for p, k in zip(plaintext, keystream)]
    return ciphertext, keystream

def rc4_decrypt(ciphertext, key):
    S = rc4_ksa(key)
    keystream = rc4_prga(S, len(ciphertext))
    return ''.join(chr(c ^ k) for c, k in zip(ciphertext, keystream))

key = "BIT3208"
message = "Stream Cipher Test"

ciphertext, keystream = rc4_encrypt(message, key)
decrypted = rc4_decrypt(ciphertext, key)

print("=== RC4 Stream Cipher ===")
print(f"Key:        {key}")
print(f"Message:    {message}")
print(f"Keystream:  {keystream[:len(message)]}")
print(f"Ciphertext: {ciphertext}")
print(f"Hex:        {' '.join(f'{b:02X}' for b in ciphertext)}")
print(f"Decrypted:  {decrypted}")
print(f"Match:      {'YES' if decrypted == message else 'NO'}")
