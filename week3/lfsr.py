def lfsr(seed, taps, length):
    register = list(seed)
    output = []

    print(f"Initial register: {register}")
    print(f"Taps: {taps}")
    print(f"\n{'Step':<6} {'Register':<20} {'Output Bit'}")
    print("-" * 40)

    for step in range(length):
        output_bit = register[-1]
        output.append(output_bit)

        feedback = 0
        for tap in taps:
            feedback ^= register[tap]

        register = [feedback] + register[:-1]
        print(f"{step+1:<6} {str(register):<20} {output_bit}")

    return output

seed = [1, 0, 1, 1]
taps = [0, 3]
sequence = lfsr(seed, taps, 16)
print(f"\nFull sequence: {''.join(map(str, sequence))}")
