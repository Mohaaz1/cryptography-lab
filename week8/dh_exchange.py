# ============================================================
#  Diffie-Hellman Key Exchange
#  BIT4138 - Advanced Cryptography
# ============================================================

def generate_public_key(g, private_key, p):
    """
    Compute public key using modular exponentiation.
    Formula: public_key = g^private_key mod p
    Python's built-in pow(base, exp, mod) is used for
    efficient modular exponentiation.
    """
    return pow(g, private_key, p)


def compute_shared_secret(other_public_key, private_key, p):
    """
    Compute shared secret using the other party's public key.
    Formula: shared_secret = other_public_key^private_key mod p
    Both Alice and Bob arrive at the same value due to the
    commutativity of modular exponentiation.
    """
    return pow(other_public_key, private_key, p)


def main():
    print("=" * 52)
    print("       DIFFIE-HELLMAN KEY EXCHANGE PROTOCOL")
    print("=" * 52)

    # Step 1: Accept Public Parameters
    print("\n[Step 1] Enter Public Parameters")
    print("-" * 36)
    p = int(input("  Public Prime  (p): "))
    g = int(input("  Generator     (g): "))

    # Step 2: Accept Private Keys
    print("\n[Step 2] Choose Private Keys (kept secret)")
    print("-" * 36)
    alice_private = int(input("  Alice Private Key: "))
    bob_private   = int(input("  Bob   Private Key: "))

    # Step 3: Generate Public Keys
    print("\n[Step 3] Computing Public Keys")
    print("-" * 36)
    alice_public = generate_public_key(g, alice_private, p)
    bob_public   = generate_public_key(g, bob_private, p)

    print(f"  Alice Public Key  = {g}^{alice_private} mod {p} = {alice_public}")
    print(f"  Bob   Public Key  = {g}^{bob_private}  mod {p} = {bob_public}")
    print("  [Public keys are exchanged over an insecure channel]")

    # Step 4: Compute Shared Secret
    print("\n[Step 4] Computing Shared Secret")
    print("-" * 36)
    alice_shared = compute_shared_secret(bob_public,   alice_private, p)
    bob_shared   = compute_shared_secret(alice_public, bob_private,   p)

    print(f"  Alice computes: {bob_public}^{alice_private} mod {p} = {alice_shared}")
    print(f"  Bob   computes: {alice_public}^{bob_private}  mod {p} = {bob_shared}")

    # Step 5: Verification
    print("\n[Step 5] Verification")
    print("-" * 36)
    if alice_shared == bob_shared:
        print(f"  [PASS] Shared secrets MATCH: {alice_shared}")
        print("  Both parties now hold the same secret key.")
    else:
        print("  [FAIL] Shared secrets DO NOT match.")
        print("  Check your inputs and try again.")

    # Summary
    print("\n" + "=" * 52)
    print("  SUMMARY")
    print("=" * 52)
    print(f"  Public Prime       (p): {p}")
    print(f"  Generator          (g): {g}")
    print(f"  Alice Private Key    : {alice_private}")
    print(f"  Bob   Private Key    : {bob_private}")
    print(f"  Alice Public Key     : {alice_public}")
    print(f"  Bob   Public Key     : {bob_public}")
    print(f"  Shared Secret Key    : {alice_shared}")
    print("=" * 52)


if __name__ == "__main__":
    main()
