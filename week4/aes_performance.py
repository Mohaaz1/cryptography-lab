import os
import time
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend

def aes_encrypt(data, key):
    iv = os.urandom(16)
    padder = padding.PKCS7(128).padder()
    padded = padder.update(data) + padder.finalize()
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    return encryptor.update(padded) + encryptor.finalize()

def benchmark(size_kb, key_bits, iterations=5):
    key  = os.urandom(key_bits // 8)
    data = os.urandom(size_kb * 1024)
    times = []
    for _ in range(iterations):
        start = time.perf_counter()
        aes_encrypt(data, key)
        times.append(time.perf_counter() - start)
    avg = sum(times) / len(times)
    throughput = (size_kb / 1024) / avg
    return avg, throughput

print("=== AES Encryption Performance Benchmark ===\n")
print(f"{'Key Size':<12} {'Data Size':<12} {'Avg Time (ms)':<18} {'Throughput (MB/s)'}")
print("-" * 62)

for key_bits in [128, 256]:
    for size_kb in [1, 64, 256]:
        avg, throughput = benchmark(size_kb, key_bits)
        print(f"AES-{key_bits:<8} {size_kb} KB{'':<8} {avg*1000:<18.3f} {throughput:.2f}")
    print()

print("Backend: OpenSSL via cryptography library")

