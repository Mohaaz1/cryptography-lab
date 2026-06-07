def caesar_encrypt(text, shift):
    result = ""
    for char in text:
        if char.isalpha():
            base = ord('A') if char.isupper() else ord('a')
            result += chr((ord(char) - base + shift) % 26 + base)
        else:
            result += char
    return result

def get_valid_shift():
    while True:
        try:
            shift = int(input("Enter shift value (1-25): "))
            if 1 <= shift <= 25:
                return shift
            print("[ERROR] Shift must be between 1 and 25")
        except ValueError:
            print("[ERROR] Please enter a valid integer")

def get_valid_text():
    while True:
        text = input("Enter message to encrypt: ").strip()
        if len(text) == 0:
            print("[ERROR] Message cannot be empty")
        elif not any(c.isalpha() for c in text):
            print("[ERROR] Message must contain at least one letter")
        else:
            return text

print("=== Caesar Cipher - User Input Validation ===")
text = get_valid_text()
shift = get_valid_shift()
encrypted = caesar_encrypt(text, shift)
print(f"[ENCRYPTED] {encrypted}")
