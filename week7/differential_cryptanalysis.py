"""
BIT4138 - Ethical Hacking / Cryptography
Practical Task 1: Differential Cryptanalysis Simulation

This program demonstrates the core idea behind differential cryptanalysis:

    1. Two plaintexts are accepted from the user.
    2. Their XOR difference is computed (the "input difference").
    3. Both plaintexts are encrypted using the SAME key with a small
       4-round Substitution-Permutation Network (SPN), and the difference
       is traced after every round.
    4. The Difference Distribution Table (DDT) of the S-box is built and
       used to show how likely each output difference is for the chosen
       input difference -- this non-uniformity is exactly what an
       attacker exploits in real differential cryptanalysis.
    5. Observations are printed: Hamming weights, DDT probabilities and
       the diffusion (avalanche) behaviour of the cipher.

The 4-round, 16-bit toy SPN (4 x 4-bit S-boxes per round) follows the
well known teaching construction used in Heys, "A Tutorial on Linear and
Differential Cryptanalysis" -- it is small enough to analyse by hand but
behaves like a miniature block cipher (substitution + permutation +
key mixing), which makes it suitable for illustrating the attack.
"""

# ---------------------------------------------------------------------------
# Cipher definition
# ---------------------------------------------------------------------------

# 4-bit S-box (same values as DES S-box S1, row 0 -- a standard teaching S-box)
S_BOX = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8,
         0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]

# Bit permutation table (1-indexed): input bit position -> output bit position
P_BOX = {1: 1, 2: 5, 3: 9, 4: 13,
         5: 2, 6: 6, 7: 10, 8: 14,
         9: 3, 10: 7, 11: 11, 12: 15,
         13: 4, 14: 8, 15: 12, 16: 16}

MASTER_KEY = 0x3A94C2F1   # fixed 32-bit master key (kept constant for both plaintexts)
NUM_ROUNDS = 4


def substitute(block: int) -> int:
    """Apply the 4-bit S-box independently to each of the four nibbles of a 16-bit block."""
    result = 0
    for shift in (12, 8, 4, 0):
        nibble = (block >> shift) & 0xF
        result |= S_BOX[nibble] << shift
    return result


def permute(block: int) -> int:
    """Apply the fixed 16-bit bit-permutation defined by P_BOX."""
    bits = [(block >> (16 - i)) & 1 for i in range(1, 17)]   # bits[0] = bit 1 (MSB)
    out_bits = [0] * 16
    for in_pos, out_pos in P_BOX.items():
        out_bits[out_pos - 1] = bits[in_pos - 1]
    result = 0
    for b in out_bits:
        result = (result << 1) | b
    return result


def get_round_keys(master_key: int, num_keys: int = 5) -> list:
    """
    Derive num_keys 16-bit round keys from a 32-bit master key.
    Round key i uses bits (4i+1) .. (4i+16) of the master key (1-indexed),
    a sliding 16-bit window shifted by 4 bits each round.
    """
    bits = [(master_key >> (32 - i)) & 1 for i in range(1, 33)]
    round_keys = []
    for i in range(num_keys):
        window = bits[4 * i: 4 * i + 16]
        val = 0
        for b in window:
            val = (val << 1) | b
        round_keys.append(val)
    return round_keys


def encrypt(plaintext: int, round_keys: list):
    """
    Encrypt a 16-bit plaintext through 4 rounds of: key-mix -> substitute -> permute,
    with the final round omitting the permutation, followed by output key whitening.
    Returns (ciphertext, history) where history records the state after every stage.
    """
    state = plaintext
    history = [state]
    for r in range(NUM_ROUNDS - 1):
        state ^= round_keys[r]
        state = substitute(state)
        state = permute(state)
        history.append(state)
    # final round: key mix + substitution only (no permutation)
    state ^= round_keys[NUM_ROUNDS - 1]
    state = substitute(state)
    history.append(state)
    # output transformation (key whitening)
    state ^= round_keys[NUM_ROUNDS]
    history.append(state)
    return state, history


# ---------------------------------------------------------------------------
# Differential analysis helpers
# ---------------------------------------------------------------------------

def build_ddt():
    """Build the 16x16 Difference Distribution Table for S_BOX."""
    ddt = [[0] * 16 for _ in range(16)]
    for dx in range(16):
        for x in range(16):
            dy = S_BOX[x] ^ S_BOX[x ^ dx]
            ddt[dx][dy] += 1
    return ddt


def hex_input(prompt: str) -> int:
    """Prompt the user for a 16-bit hex value (0000-FFFF), validating input."""
    while True:
        raw = input(prompt).strip().lower().replace("0x", "")
        try:
            value = int(raw, 16)
        except ValueError:
            print("  Invalid input. Please enter a hexadecimal value, e.g. 1A2B")
            continue
        if 0 <= value <= 0xFFFF:
            return value
        print("  Value out of range. Enter a value between 0000 and FFFF.")


# ---------------------------------------------------------------------------
# Main program
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print(" DIFFERENTIAL CRYPTANALYSIS SIMULATION - 4-Round Toy SPN (16-bit)")
    print("=" * 70)
    print("Enter two 16-bit plaintexts in hexadecimal (0000 - FFFF).\n")

    p1 = hex_input("Plaintext 1 (hex): ")
    p2 = hex_input("Plaintext 2 (hex): ")

    round_keys = get_round_keys(MASTER_KEY)
    delta_p = p1 ^ p2

    print("\n--- Step 1: Input Difference ---")
    print(f"Plaintext 1            : {p1:04X}  ({p1:016b})")
    print(f"Plaintext 2             : {p2:04X}  ({p2:016b})")
    print(f"Input Difference (dP)   : {delta_p:04X}  ({delta_p:016b})")

    print("\n--- Step 2: Round-by-Round Difference Propagation ---")
    c1, h1 = encrypt(p1, round_keys)
    c2, h2 = encrypt(p2, round_keys)
    stage_labels = [
        "Plaintext",
        "After Round 1",
        "After Round 2",
        "After Round 3",
        "After Round 4 (sub.)",
        "Ciphertext (final)",
    ]
    print(f"{'Stage':<22}{'State 1':<10}{'State 2':<10}{'Difference':<10}{'Weight'}")
    for label, s1, s2 in zip(stage_labels, h1, h2):
        diff = s1 ^ s2
        weight = bin(diff).count("1")
        print(f"{label:<22}{s1:04X}{'':<6}{s2:04X}{'':<6}{diff:04X}{'':<6}{weight}")

    delta_c = c1 ^ c2
    print("\n--- Step 3: Output Difference ---")
    print(f"Ciphertext 1            : {c1:04X}")
    print(f"Ciphertext 2            : {c2:04X}")
    print(f"Output Difference (dC)  : {delta_c:04X}  ({delta_c:016b})")

    print("\n--- Step 4: S-box Difference Distribution Table (Round 1 input) ---")
    ddt = build_ddt()
    nibble_diffs = [(delta_p >> shift) & 0xF for shift in (12, 8, 4, 0)]
    print(f"{'S-box':<8}{'Input dX':<10}{'Possible output dY : count (out of 16)'}")
    for idx, dx in enumerate(nibble_diffs, start=1):
        pairs = [(dy, ddt[dx][dy]) for dy in range(16) if ddt[dx][dy] > 0]
        pairs_str = ", ".join(f"{dy:X}:{cnt}" for dy, cnt in pairs)
        print(f"S-box {idx:<3}{dx:X}{'':<8}{pairs_str}")

    print("\n--- Step 5: Observations ---")
    w_in = bin(delta_p).count("1")
    w_out = bin(delta_c).count("1")
    print(f"- Hamming weight of input difference (dP)  : {w_in} bit(s) out of 16")
    print(f"- Hamming weight of output difference (dC) : {w_out} bit(s) out of 16")

    if delta_p == 0:
        print("- The two plaintexts are identical (dP = 0000), so there is no")
        print("  difference to propagate. Enter two distinct plaintexts to see")
        print("  diffusion through the cipher.")
    else:
        active_boxes = [(idx, dx) for idx, dx in enumerate(nibble_diffs, start=1) if dx != 0]
        for idx, dx in active_boxes:
            best_dy, best_cnt = max(((dy, ddt[dx][dy]) for dy in range(16)), key=lambda t: t[1])
            print(f"- For S-box {idx} the input difference {dx:X} produces output difference")
            print(f"  {best_dy:X} with the highest probability, {best_cnt}/16, while some output")
            print(f"  differences for that input never occur (probability 0/16). This bias is")
            print(f"  exactly what a real differential attack exploits to recover key bits with")
            print(f"  fewer than brute-force-level plaintext/ciphertext pairs.")
        if w_out > w_in:
            print(f"- The output difference is denser ({w_out} bits) than the input difference")
            print(f"  ({w_in} bits), showing the avalanche effect produced by repeated")
            print(f"  substitution and permutation layers across {NUM_ROUNDS} rounds.")
        print(f"- Over the full {NUM_ROUNDS} rounds the single-bit/nibble bias visible at one")
        print(f"  S-box is diluted by diffusion, illustrating why real ciphers use enough")
        print(f"  rounds to make differential characteristics impractically low-probability.")

    print("\n" + "=" * 70)
    print(" End of simulation")
    print("=" * 70)


if __name__ == "__main__":
    main()
