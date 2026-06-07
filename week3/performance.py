import time

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
    return [ord(p) ^ k for p, k in zip(plaintext, keystream)]

def benchmark(size_kb, key, iterations=5):
    data = 'A' * (size_kb * 1024)
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        rc4_encrypt(data, key)
        end = time.perf_counter()
        times.append(end - start)
    avg_time = sum(times) / len(times)
    throughput = size_kb / avg_time / 1024
    return avg_time, throughput

key = "BIT3208"

print("=== RC4 Encryption Performance ===")
print(f"\n{'Size (KB)':<12} {'Avg Time (ms)':<18} {'Throughput (MB/s)'}")
print("-" * 50)

for size in [1, 4, 16, 64]:
    avg_time, throughput = benchmark(size, key)
    print(f"{size:<12} {avg_time*1000:<18.2f} {throughput:.2f}")

print("\nNote: Pure Python — real RC4 in C is significantly faster.")
