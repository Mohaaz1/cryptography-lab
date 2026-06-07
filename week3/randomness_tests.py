import math

def lfsr(seed, taps, length):
    register = list(seed)
    output = []
    for _ in range(length):
        output_bit = register[-1]
        output.append(output_bit)
        feedback = 0
        for tap in taps:
            feedback ^= register[tap]
        register = [feedback] + register[:-1]
    return output

def frequency_test(seq):
    n = len(seq)
    ones = sum(seq)
    zeros = n - ones
    s_obs = abs(ones - zeros) / math.sqrt(n)
    p_value = math.erfc(s_obs / math.sqrt(2))
    return ones, zeros, s_obs, p_value

def runs_test(seq):
    n = len(seq)
    runs = 1
    for i in range(1, n):
        if seq[i] != seq[i-1]:
            runs += 1
    pi = sum(seq) / n
    expected = 2 * n * pi * (1 - pi)
    return runs, expected

sequence = lfsr([1, 0, 1, 1], [0, 3], 128)

print("=== Statistical Randomness Tests ===\n")

ones, zeros, s_obs, p_value = frequency_test(sequence)
print("--- Frequency (Monobit) Test ---")
print(f"Length:  {len(sequence)} bits")
print(f"Ones:    {ones} ({ones/len(sequence)*100:.1f}%)")
print(f"Zeros:   {zeros} ({zeros/len(sequence)*100:.1f}%)")
print(f"S_obs:   {s_obs:.4f}")
print(f"P-value: {p_value:.4f}")
print(f"Result:  {'PASS (random)' if p_value > 0.01 else 'FAIL (not random)'}")

print("\n--- Runs Test ---")
runs, expected = runs_test(sequence)
print(f"Observed runs: {runs}")
print(f"Expected runs: {expected:.2f}")
print(f"Difference:    {abs(runs - expected):.2f}")
print(f"Result:        {'PASS' if abs(runs - expected) < 20 else 'FAIL'}")
