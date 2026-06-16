import time

# =====================================
# SPN CIPHER
# =====================================

SBOX = {
    0: 14, 1: 4, 2: 13, 3: 1,
    4: 2, 5: 15, 6: 11, 7: 8,
    8: 3, 9: 10, 10: 6, 11: 12,
    12: 5, 13: 9, 14: 0, 15: 7
}

def spn_encrypt(text):

    data = [ord(c) % 16 for c in text]

    for _ in range(4):

        # Key Mixing
        data = [x ^ 5 for x in data]

        # Substitution
        data = [SBOX[x] for x in data]

        # Permutation
        data = data[::-1]

    return data


# =====================================
# FEISTEL CIPHER
# =====================================

def round_function(x):
    return (x + 5) % 16


def feistel_encrypt(text):

    data = [ord(c) % 16 for c in text]

    if len(data) % 2 != 0:
        data.append(0)

    left = data[:len(data)//2]
    right = data[len(data)//2:]

    for _ in range(4):

        new_left = right

        new_right = []

        for i in range(len(left)):
            new_right.append(
                left[i] ^ round_function(right[i])
            )

        left = new_left
        right = new_right

    return left + right


# =====================================
# MAIN PROGRAM
# =====================================

plaintext = input("Enter plaintext: ")

# SPN Test
start = time.perf_counter()
spn_result = spn_encrypt(plaintext)
spn_time = time.perf_counter() - start

# Feistel Test
start = time.perf_counter()
feistel_result = feistel_encrypt(plaintext)
feistel_time = time.perf_counter() - start

# =====================================
# REPORT
# =====================================

print("\n" + "="*50)
print("SPN vs FEISTEL COMPARISON")
print("="*50)

print("\nOriginal Text:")
print(plaintext)

print("\nSPN Ciphertext:")
print(spn_result)

print("\nFeistel Ciphertext:")
print(feistel_result)

print("\nEncryption Speed")

print(f"SPN Time     : {spn_time:.8f} seconds")
print(f"Feistel Time : {feistel_time:.8f} seconds")

print("\nSecurity Comparison")

print("SPN:")
print("  ✓ Strong confusion")
print("  ✓ Strong diffusion")
print("  ✓ Basis of AES")

print("\nFeistel:")
print("  ✓ Easier decryption")
print("  ✓ Flexible round function")
print("  ✓ Used in DES and Blowfish")

print("\nEase of Implementation")

print("SPN      : Moderate")
print("Feistel  : Easy")

print("\nModern Usage")

print("SPN      : AES")
print("Feistel  : DES, Blowfish")

print("\nFinal Verdict")

if spn_time < feistel_time:
    print("SPN was faster on this input.")
else:
    print("Feistel was faster on this input.")

print("\nAES uses an SPN structure, which is why")
print("SPN is considered the dominant modern design.")
