import tkinter as tk
from tkinter import filedialog, messagebox
from collections import Counter
import matplotlib.pyplot as plt
import pandas as pd


# ==========================
# SIMPLE XOR BLOCK CIPHER
# ==========================
def encrypt(text, key):
    ciphertext = ""

    for i, char in enumerate(text):
        ciphertext += chr(
            ord(char) ^ ord(key[i % len(key)])
        )

    return ciphertext


# ==========================
# AVALANCHE EFFECT
# ==========================
def avalanche_effect(text, key):

    cipher1 = encrypt(text, key)

    modified_text = list(text)

    if len(modified_text) > 0:
        modified_text[0] = chr(
            ord(modified_text[0]) ^ 1
        )

    modified_text = "".join(modified_text)

    cipher2 = encrypt(modified_text, key)

    changed_bits = 0

    for a, b in zip(cipher1, cipher2):

        xor_result = ord(a) ^ ord(b)

        changed_bits += bin(
            xor_result
        ).count("1")

    total_bits = len(cipher1) * 8

    percentage = (
        changed_bits / total_bits
    ) * 100

    return changed_bits, percentage


# ==========================
# DIFFERENCE ANALYSIS
# ==========================
def difference_analysis(text, cipher):

    differences = []

    for p, c in zip(text, cipher):

        differences.append(
            abs(ord(p) - ord(c))
        )

    return differences


# ==========================
# FREQUENCY ANALYSIS
# ==========================
def frequency_distribution(cipher):

    return Counter(cipher)


# ==========================
# ANALYZE
# ==========================
def analyze():

    plaintext = plaintext_box.get(
        "1.0",
        tk.END
    ).strip()

    key = key_entry.get()

    if not plaintext or not key:

        messagebox.showerror(
            "Error",
            "Enter plaintext and key."
        )

        return

    cipher = encrypt(
        plaintext,
        key
    )

    ciphertext_box.delete(
        "1.0",
        tk.END
    )

    ciphertext_box.insert(
        tk.END,
        cipher
    )

    bits_changed, percentage = avalanche_effect(
        plaintext,
        key
    )

    differences = difference_analysis(
        plaintext,
        cipher
    )

    average_difference = (
        sum(differences) / len(differences)
    )

    report = f"""
BLOCK CIPHER SECURITY REPORT

Avalanche Effect
-------------------------
Bits Changed: {bits_changed}
Percentage Changed: {percentage:.2f}%

Difference Analysis
-------------------------
Average Difference: {average_difference:.2f}

Cipher Length: {len(cipher)}
Plaintext Length: {len(plaintext)}
"""

    report_box.delete(
        "1.0",
        tk.END
    )

    report_box.insert(
        tk.END,
        report
    )

    global frequency_data
    frequency_data = frequency_distribution(
        cipher
    )


# ==========================
# SHOW CHART
# ==========================
def show_chart():

    if not frequency_data:

        messagebox.showinfo(
            "Info",
            "Run analysis first."
        )

        return

    chars = list(
        frequency_data.keys()
    )

    counts = list(
        frequency_data.values()
    )

    plt.figure(
        figsize=(10, 5)
    )

    plt.bar(
        chars,
        counts
    )

    plt.title(
        "Ciphertext Frequency Distribution"
    )

    plt.xlabel(
        "Characters"
    )

    plt.ylabel(
        "Frequency"
    )

    plt.show()


# ==========================
# EXPORT RESULTS
# ==========================
def export_results():

    if not frequency_data:

        messagebox.showinfo(
            "Info",
            "Run analysis first."
        )

        return

    filename = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[
            ("CSV Files", "*.csv")
        ]
    )

    if not filename:
        return

    df = pd.DataFrame(
        frequency_data.items(),
        columns=[
            "Character",
            "Frequency"
        ]
    )

    df.to_csv(
        filename,
        index=False
    )

    messagebox.showinfo(
        "Success",
        "Results exported successfully."
    )


# ==========================
# GUI
# ==========================
root = tk.Tk()

root.title(
    "Block Cipher Security Analyzer"
)

root.geometry(
    "900x700"
)

frequency_data = {}

title = tk.Label(
    root,
    text="Block Cipher Security Analyzer",
    font=("Arial", 18, "bold")
)

title.pack(
    pady=10
)

tk.Label(
    root,
    text="Plaintext"
).pack()

plaintext_box = tk.Text(
    root,
    height=6,
    width=80
)

plaintext_box.pack()

tk.Label(
    root,
    text="Secret Key"
).pack()

key_entry = tk.Entry(
    root,
    width=40
)

key_entry.pack(
    pady=5
)

tk.Button(
    root,
    text="Analyze Security",
    command=analyze
).pack(
    pady=10
)

tk.Label(
    root,
    text="Ciphertext"
).pack()

ciphertext_box = tk.Text(
    root,
    height=5,
    width=80
)

ciphertext_box.pack()

tk.Label(
    root,
    text="Statistical Report"
).pack()

report_box = tk.Text(
    root,
    height=12,
    width=80
)

report_box.pack()

tk.Button(
    root,
    text="Show Frequency Chart",
    command=show_chart
).pack(
    pady=5
)

tk.Button(
    root,
    text="Export Results",
    command=export_results
).pack(
    pady=5
)

root.mainloop()
