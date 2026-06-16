import tkinter as tk
from tkinter import messagebox
import string

# =====================================
# S-BOX CREATION
# =====================================

alphabet = string.printable

sbox = {}
inverse_sbox = {}

for i, ch in enumerate(alphabet):
    substitute = alphabet[(i + 7) % len(alphabet)]
    sbox[ch] = substitute
    inverse_sbox[substitute] = ch


# =====================================
# KEY MIXING
# =====================================

def key_mix(text, key):
    result = ""

    for i in range(len(text)):
        result += chr(ord(text[i]) ^ ord(key[i % len(key)]))

    return result


# =====================================
# SUBSTITUTION
# =====================================

def substitute(text):
    return ''.join(sbox.get(c, c) for c in text)


def inverse_substitute(text):
    return ''.join(inverse_sbox.get(c, c) for c in text)


# =====================================
# PERMUTATION
# =====================================

def permute(text):

    chars = list(text)

    for i in range(0, len(chars) - 1, 2):
        chars[i], chars[i + 1] = chars[i + 1], chars[i]

    return ''.join(chars)


def inverse_permute(text):

    chars = list(text)

    for i in range(0, len(chars) - 1, 2):
        chars[i], chars[i + 1] = chars[i + 1], chars[i]

    return ''.join(chars)


# =====================================
# ENCRYPTION
# =====================================

def encrypt(plaintext, key, rounds):

    state = plaintext

    for _ in range(rounds):
        state = key_mix(state, key)
        state = substitute(state)
        state = permute(state)

    return state


# =====================================
# DECRYPTION
# =====================================

def decrypt(ciphertext, key, rounds):

    state = ciphertext

    for _ in range(rounds):
        state = inverse_permute(state)
        state = inverse_substitute(state)
        state = key_mix(state, key)

    return state


# =====================================
# GUI FUNCTIONS
# =====================================

def encrypt_text():

    text = input_text.get("1.0", tk.END).rstrip()

    key = key_entry.get()

    if not text or not key:
        messagebox.showerror(
            "Error",
            "Please enter text and key."
        )
        return

    rounds = int(rounds_entry.get())

    cipher = encrypt(text, key, rounds)

    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, repr(cipher))


def decrypt_text():

    cipher = input_text.get("1.0", tk.END).rstrip()

    key = key_entry.get()

    if not cipher or not key:
        messagebox.showerror(
            "Error",
            "Please enter ciphertext and key."
        )
        return

    rounds = int(rounds_entry.get())

    try:
        cipher = eval(cipher)

        plain = decrypt(cipher, key, rounds)

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, plain)

    except:
        messagebox.showerror(
            "Error",
            "Invalid ciphertext format."
        )


# =====================================
# GUI WINDOW
# =====================================

root = tk.Tk()
root.title("Mini AES Encryption Simulator")
root.geometry("700x600")

title = tk.Label(
    root,
    text="Mini AES-Inspired Encryption Simulator",
    font=("Arial", 16, "bold")
)
title.pack(pady=10)

tk.Label(root, text="Input Text").pack()

input_text = tk.Text(root, height=8, width=70)
input_text.pack()

tk.Label(root, text="Secret Key").pack(pady=5)

key_entry = tk.Entry(root, width=40)
key_entry.pack()

tk.Label(root, text="Number of Rounds").pack(pady=5)

rounds_entry = tk.Entry(root, width=10)
rounds_entry.insert(0, "3")
rounds_entry.pack()

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

encrypt_btn = tk.Button(
    button_frame,
    text="Encrypt",
    width=15,
    command=encrypt_text
)
encrypt_btn.grid(row=0, column=0, padx=10)

decrypt_btn = tk.Button(
    button_frame,
    text="Decrypt",
    width=15,
    command=decrypt_text
)
decrypt_btn.grid(row=0, column=1, padx=10)

tk.Label(root, text="Output").pack()

output_text = tk.Text(root, height=10, width=70)
output_text.pack()

root.mainloop()
