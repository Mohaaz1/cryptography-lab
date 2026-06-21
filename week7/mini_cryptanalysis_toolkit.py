"""
BIT4138 - Advanced Cryptography / Ethical Hacking
Advanced Programming Task: Mini Cryptanalysis Toolkit

A small, self-contained toolkit that brings together three classical
cryptanalysis primitives used throughout this course:

    1. Differential analysis  - XOR differences between input pairs, plus
                                 a Difference Distribution Table (DDT) lookup
                                 for the S-box used in the Week 7 SPN work.
    2. Frequency analysis     - letter-frequency / chi-squared analysis of
                                 ciphertext, used to break classical
                                 mono-alphabetic substitution (Caesar) ciphers.
    3. Statistical bias       - a Linear Approximation Table (LAT) for the
                                 S-box, the building block behind Matsui's
                                 linear cryptanalysis of DES.

Running this file directly executes run_demo(), which performs all three
analyses on built-in sample data and prints a formatted report
automatically; no user input is required.
"""

import string

# ---------------------------------------------------------------------------
# Shared cipher component
# ---------------------------------------------------------------------------

# Same 4-bit S-box used in the Practical Task 1 SPN (DES S1-row style box),
# reused here so the differential and bias analyses examine the same
# component studied earlier in the week.
S_BOX = [0xE, 0x4, 0xD, 0x1, 0x2, 0xF, 0xB, 0x8,
         0x3, 0xA, 0x6, 0xC, 0x5, 0x9, 0x0, 0x7]

# Standard English letter frequency (%), the classic reference distribution
# used when attacking substitution ciphers by frequency analysis.
ENGLISH_FREQ = {
    'A': 8.17, 'B': 1.49, 'C': 2.78, 'D': 4.25, 'E': 12.70, 'F': 2.23,
    'G': 2.02, 'H': 6.09, 'I': 6.97, 'J': 0.15, 'K': 0.77, 'L': 4.03,
    'M': 2.41, 'N': 6.75, 'O': 7.51, 'P': 1.93, 'Q': 0.10, 'R': 5.99,
    'S': 6.33, 'T': 9.06, 'U': 2.76, 'V': 0.98, 'W': 2.36, 'X': 0.15,
    'Y': 1.97, 'Z': 0.07,
}


# ===========================================================================
# 1. DIFFERENTIAL ANALYSIS
# ===========================================================================

def xor_difference(a: bytes, b: bytes):
    """Compute the byte-wise XOR difference between two equal-length byte strings."""
    if len(a) != len(b):
        raise ValueError("Inputs must be the same length to compute a difference.")
    diff = bytes(x ^ y for x, y in zip(a, b))
    weight = sum(bin(byte).count("1") for byte in diff)
    return diff, weight


def build_ddt(sbox=S_BOX):
    """Build the Difference Distribution Table (DDT) for a 4-bit S-box."""
    n = len(sbox)
    ddt = [[0] * n for _ in range(n)]
    for dx in range(n):
        for x in range(n):
            dy = sbox[x] ^ sbox[x ^ dx]
            ddt[dx][dy] += 1
    return ddt


def differential_report(pairs, sbox=S_BOX):
    """
    Run differential analysis over a list of (input1, input2) byte-string
    pairs: compute the XOR difference and Hamming weight, then look up the
    most likely S-box output difference for every active 4-bit nibble.
    """
    ddt = build_ddt(sbox)
    results = []
    for a, b in pairs:
        diff, weight = xor_difference(a, b)
        nibble_lookups = []
        for byte in diff:
            for nibble in (byte >> 4, byte & 0xF):
                if nibble != 0:
                    best_dy, best_cnt = max(
                        ((dy, ddt[nibble][dy]) for dy in range(16)), key=lambda t: t[1]
                    )
                    nibble_lookups.append((nibble, best_dy, best_cnt))
        results.append({"a": a, "b": b, "diff": diff, "weight": weight, "lookups": nibble_lookups})
    return results, ddt


# ===========================================================================
# 2. FREQUENCY ANALYSIS
# ===========================================================================

def letter_frequencies(text: str):
    """Return percentage frequency of each letter A-Z in the given text, plus total letter count."""
    letters = [c.upper() for c in text if c.isalpha()]
    total = len(letters)
    freq = {ch: 0 for ch in string.ascii_uppercase}
    for ch in letters:
        freq[ch] += 1
    if total:
        freq = {ch: (count / total) * 100 for ch, count in freq.items()}
    return freq, total


def chi_squared_score(observed_pct, total_letters, expected_pct=ENGLISH_FREQ):
    """
    Chi-squared goodness-of-fit statistic comparing an observed letter
    frequency distribution (percentages) to the standard English reference
    distribution. Lower values indicate a closer match to English.
    """
    score = 0.0
    for ch in string.ascii_uppercase:
        observed_count = observed_pct[ch] / 100 * total_letters
        expected_count = expected_pct[ch] / 100 * total_letters
        if expected_count > 0:
            score += ((observed_count - expected_count) ** 2) / expected_count
    return score


def caesar_decrypt(text: str, shift: int) -> str:
    """Decrypt text assuming a Caesar (mono-alphabetic shift) cipher with the given shift."""
    result = []
    for ch in text:
        if ch.isalpha():
            base = ord("A") if ch.isupper() else ord("a")
            result.append(chr((ord(ch) - base - shift) % 26 + base))
        else:
            result.append(ch)
    return "".join(result)


def frequency_analysis_report(ciphertext: str):
    """
    Perform classic frequency analysis on a ciphertext assumed to be a
    Caesar cipher: compute its letter-frequency distribution, then test all
    26 shifts and rank them by chi-squared distance to standard English to
    recover the most likely shift and plaintext.
    """
    freq, total = letter_frequencies(ciphertext)
    candidates = []
    for shift in range(26):
        decrypted = caesar_decrypt(ciphertext, shift)
        dec_freq, dec_total = letter_frequencies(decrypted)
        score = chi_squared_score(dec_freq, dec_total)
        candidates.append((shift, score, decrypted))
    candidates.sort(key=lambda t: t[1])
    return freq, total, candidates


# ===========================================================================
# 3. STATISTICAL BIAS (LINEAR APPROXIMATION)
# ===========================================================================

def parity(x: int) -> int:
    """Return the XOR (parity) of all set bits in x."""
    p = 0
    while x:
        p ^= x & 1
        x >>= 1
    return p


def build_lat(sbox=S_BOX):
    """
    Build the Linear Approximation Table (LAT) for a 4-bit S-box.
    lat[a][b] = (number of x where parity(a & x) == parity(b & S(x))) - n/2
    A value of 0 means the approximation a.x = b.S(x) is unbiased (holds for
    exactly half of all inputs); larger |value| means stronger bias, which
    is exactly what linear cryptanalysis (Matsui's attack on DES) exploits.
    """
    n = len(sbox)
    lat = [[0] * n for _ in range(n)]
    for a in range(n):
        for b in range(n):
            count = sum(1 for x in range(n) if parity(a & x) == parity(b & sbox[x]))
            lat[a][b] = count - n // 2
    return lat


def bias_report(sbox=S_BOX):
    """Build the LAT and identify the strongest non-trivial linear approximation."""
    lat = build_lat(sbox)
    n = len(sbox)
    best = None
    for a in range(1, n):
        for b in range(1, n):
            bias = abs(lat[a][b]) / (2 * n)
            if best is None or bias > best[2]:
                best = (a, b, bias, lat[a][b])
    return lat, best


# ===========================================================================
# 4. AUTOMATIC DEMONSTRATION / REPORT
# ===========================================================================

def section(title):
    print("\n" + "=" * 72)
    print(f" {title}")
    print("=" * 72)


def run_demo():
    print("#" * 72)
    print("# MINI CRYPTANALYSIS TOOLKIT - AUTOMATIC DEMONSTRATION")
    print("#" * 72)

    # ---- 1. Differential analysis -----------------------------------
    section("1. DIFFERENTIAL ANALYSIS")
    sample_pairs = [
        (b"\x1A\x2B", b"\x1A\x2F"),   # single-nibble difference
        (b"\x00\x00", b"\x80\x00"),   # single-bit difference
        (b"HELLO", b"HEMLO"),         # one-character text difference
    ]
    results, _ = differential_report(sample_pairs)
    for r in results:
        print(f"\nInput 1 = {r['a']!r}")
        print(f"Input 2 = {r['b']!r}")
        print(f"XOR Difference = {r['diff'].hex().upper()}  (Hamming weight = {r['weight']})")
        if r["lookups"]:
            print("S-box DDT lookup for each active nibble difference:")
            for nib, dy, cnt in r["lookups"]:
                print(f"  input diff {nib:X} -> most likely output diff {dy:X}  (probability {cnt}/16)")
        else:
            print("No active nibbles (inputs identical).")

    # ---- 2. Frequency analysis ---------------------------------------
    section("2. FREQUENCY ANALYSIS")
    sample_ciphertext = "WKLV LV D VLPSOH WHVW PHVVDJH IRU IUHTXHQFB DQDOBVLV"
    freq, total, candidates = frequency_analysis_report(sample_ciphertext)
    print(f"Ciphertext: {sample_ciphertext}")
    print(f"Total letters analysed: {total}")
    print("\nObserved letter frequency (top 5 most common letters):")
    for ch, pct in sorted(freq.items(), key=lambda t: t[1], reverse=True)[:5]:
        print(f"  {ch}: {pct:5.2f}%")
    print("\nTop 3 candidate shifts ranked by chi-squared distance to English")
    print("(lowest score = closest match = most likely correct shift):")
    for shift, score, decrypted in candidates[:3]:
        print(f"  Shift {shift:2d}   chi^2 = {score:7.2f}   -> {decrypted}")

    # ---- 3. Statistical bias ------------------------------------------
    section("3. STATISTICAL BIAS (LINEAR APPROXIMATION TABLE)")
    lat, best = bias_report()
    a, b, bias, raw = best
    print(f"S-box analysed: {[hex(v) for v in S_BOX]}")
    print("Strongest non-trivial linear approximation found:")
    print(f"  input mask = {a:X}, output mask = {b:X}")
    print(f"  holds for {raw + 8}/16 inputs  ->  bias = {bias:.4f}  (0.0000 = unbiased)")
    print("\nFull LAT (rows = input mask a, columns = output mask b);")
    print("values are signed deviation from the unbiased count of 8:")
    print("    " + "".join(f"{col:5X}" for col in range(16)))
    for a_idx, row in enumerate(lat):
        print(f"{a_idx:X} | " + "".join(f"{v:5d}" for v in row))

    # ---- 5. Observations ------------------------------------------------
    section("OBSERVATIONS")
    print("- Differential analysis shows that the S-box does not spread input")
    print("  differences uniformly: some output differences are far more likely")
    print("  than others, which is exactly what differential cryptanalysis exploits.")
    print(f"- Frequency analysis correctly ranked shift {candidates[0][0]} as the most")
    print("  English-like decryption using only the statistical shape of the letter")
    print("  distribution, with no knowledge of the key - the classical attack on")
    print("  mono-alphabetic substitution ciphers.")
    print(f"- The strongest linear approximation (mask {a:X} -> {b:X}) is biased away")
    print("  from the ideal 8/16, giving an attacker a statistical edge over random")
    print("  guessing - the foundation of Matsui's linear cryptanalysis of DES.")

    section("END OF AUTOMATIC REPORT")


if __name__ == "__main__":
    run_demo()
