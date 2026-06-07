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

seed = [1, 0, 1, 1]
taps = [0, 3]
sequence = lfsr(seed, taps, 64)

print("=== Pseudorandom Bit Sequence (LFSR) ===")
print(f"Seed:   {seed}")
print(f"Taps:   {taps}")
print(f"Length: {len(sequence)} bits\n")

for i in range(0, len(sequence), 8):
    group = sequence[i:i+8]
    bits = ''.join(map(str, group))
    byte_val = int(bits, 2)
    print(f"  Bits {i+1:>2}-{i+8:<2}: {bits}  (0x{byte_val:02X} = {byte_val})")

print(f"\nFull: {''.join(map(str, sequence))}")
print(f"Ones: {sequence.count(1)}  Zeros: {sequence.count(0)}")
print(f"Balance: {sequence.count(1)/len(sequence)*100:.1f}% ones")
