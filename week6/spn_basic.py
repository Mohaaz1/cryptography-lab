# -----------------------------------------------------------------------
# Step 1: The S-Box (substitution table)
# This extends the 4-entry S-Box shown in class (0->14, 1->4, 2->13, 3->1)
# to cover all 16 possible 4-bit values (0-15), since real text characters
# need a full nibble's worth of substitution, not just 4 inputs.
# -----------------------------------------------------------------------
SBOX = {
    0: 14, 1: 4,  2: 13, 3: 1,
    4: 2,  5: 15, 6: 11, 7: 8,
    8: 3,  9: 10, 10: 6, 11: 12,
    12: 5, 13: 9, 14: 0, 15: 7
}

# -----------------------------------------------------------------------
# Step 2: The P-Box (permutation table)
# PBOX[i] tells us which input bit position moves into output position i.
# This rearranges bits without changing their values (diffusion).
# -----------------------------------------------------------------------
PBOX = [2, 7, 4, 1, 6, 0, 5, 3]


def substitute_byte(byte_value):
    """
    Step 3: Substitution.
    Splits one byte (0-255) into two 4-bit nibbles, runs each nibble
    through the S-Box, then recombines them into a substituted byte.
    """
    high_nibble = (byte_value >> 4) & 0xF
    low_nibble = byte_value & 0xF

    sub_high = SBOX[high_nibble]
    sub_low = SBOX[low_nibble]

    return (sub_high << 4) | sub_low


def permute_byte(byte_value):
    """
    Step 4: Permutation.
    Converts the byte to its 8-bit binary string, then rearranges those
    bits according to PBOX.
    """
    bits = format(byte_value, '08b')
    permuted_bits = ''.join(bits[position] for position in PBOX)
    return int(permuted_bits, 2)


def spn_encrypt(plaintext):
    """
    Step 5: Run every character of the plaintext through
    substitution, then permutation, producing the ciphertext bytes.
    """
    ciphertext_bytes = []
    for char in plaintext:
        original_byte = ord(char)
        substituted = substitute_byte(original_byte)
        permuted = permute_byte(substituted)
        ciphertext_bytes.append(permuted)
    return ciphertext_bytes


def main():
    plaintext = input("Enter plaintext: ")

    print("\n--- SPN Encryption Process ---")
    print("Plaintext:", plaintext)
    print("Plaintext byte values:", [ord(c) for c in plaintext])

    ciphertext = spn_encrypt(plaintext)

    print("\nCiphertext (decimal):", ciphertext)
    print("Ciphertext (hex):", [hex(b) for b in ciphertext])


if __name__ == "__main__":
    main()
