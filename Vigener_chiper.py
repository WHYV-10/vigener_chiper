import tkinter as tk
from tkinter import messagebox

# ====== TEMA: BIRU NAVY ======
WARNA, GELAP, MUDA, BG, BORDER = "#1E3A8A", "#172554", "#BFDBFE", "#E8EEF9", "#B6C6EA"
FONT = "Segoe UI"


def vigenere(text, key, decrypt=False):
    kunci = [ord(k.lower()) - 97 for k in key if k.isalpha()]
    hasil = ""
    i = 0
    for ch in text:
        if ch.isalpha():
            geser = kunci[i % len(kunci)]
            if decrypt:
                geser = -geser
            base = ord("A") if ch.isupper() else ord("a")
            hasil += chr((ord(ch) - base + geser) % 26 + base)
            i += 1
        else:
            hasil += ch
    return hasil


def aliran_kunci(teks, key):
    k = [c.upper() for c in key if c.isalpha()]
    out, i = "", 0
    for ch in teks:
        if ch.isalpha():
            out += k[i % len(k)]
            i += 1
        else:
            out += " "
    return out


def tombol(parent, teks, cmd, bg, fg, hover):
    b = tk.Label(parent, text=teks, bg=bg, fg=fg, font=(FONT, 10, "bold"),
                 padx=20, pady=8, cursor="hand2")
    b.bind("<Button-1>", lambda e: cmd())
    b.bind("<Enter>", lambda e: b.config(bg=hover))
    b.bind("<Leave>", lambda e: b.config(bg=bg))
    return b


def kotak_teks(parent, tinggi):
    return tk.Text(parent, height=tinggi, width=54, font=("Consolas", 11), wrap="word",
                   relief="flat", bg="#F5F8FF", padx=8, pady=8,
                   highlightthickness=2, highlightbackground=BORDER, highlightcolor=WARNA)


def label(parent, teks):
    return tk.Label(parent, text=teks, bg="white", fg=WARNA, font=(FONT, 10, "bold"))


def proses(decrypt):
    key = entry_key.get()
    if not any(k.isalpha() for k in key):
        messagebox.showerror("Error", "Kunci harus berisi huruf!")
        return
    teks = input_text.get("1.0", tk.END).strip()
    if not teks:
        messagebox.showwarning("Peringatan", "Teks masih kosong!")
        return
    hasil = vigenere(teks, key, decrypt)
    output_text.delete("1.0", tk.END)
    output_text.insert(tk.END, hasil)

    # Panel visual khas Vigenere: teks asli sejajar dengan aliran kunci
    asli = (hasil if decrypt else teks).replace("\n", " ")[:45]
    stream.config(text="Teks : " + asli + "\nKunci: " + aliran_kunci(asli, key))
    status.config(text="Dekripsi berhasil" if decrypt else "Enkripsi berhasil")


def salin():
    hasil = output_text.get("1.0", tk.END).strip()
    if hasil:
        root.clipboard_clear()
        root.clipboard_append(hasil)
        status.config(text="Hasil disalin ke clipboard")


root = tk.Tk()
root.title("Vigenere Cipher")
root.configure(bg=BG)
root.resizable(False, False)

# Header
header = tk.Frame(root, bg=WARNA)
header.pack(fill="x")
tk.Label(header, text="VIGENERE CIPHER", font=(FONT, 22, "bold"), bg=WARNA, fg="white").pack(pady=(18, 0))
tk.Label(header, text="Cipher polialfabetik  |  kunci berupa kata yang diulang",
         font=(FONT, 10), bg=WARNA, fg=MUDA).pack(pady=(2, 18))
tk.Frame(root, bg="#3B82F6", height=4).pack(fill="x")

# Kartu utama
card = tk.Frame(root, bg="white", padx=22, pady=16)
card.pack(padx=18, pady=18)

label(card, "Teks").pack(anchor="w")
input_text = kotak_teks(card, 5)
input_text.pack(pady=(4, 10))

label(card, "Kunci (kata)").pack(anchor="w")
entry_key = tk.Entry(card, font=(FONT, 12), width=24, relief="flat", bg="#F5F8FF",
                     highlightthickness=2, highlightbackground=BORDER, highlightcolor=WARNA)
entry_key.insert(0, "KUNCI")
entry_key.pack(anchor="w", pady=(4, 10), ipady=4)

frame = tk.Frame(card, bg="white")
frame.pack(pady=(0, 10))
tombol(frame, "Enkripsi", lambda: proses(False), WARNA, "white", GELAP).pack(side="left", padx=5)
tombol(frame, "Dekripsi", lambda: proses(True), "#DBEAFE", WARNA, MUDA).pack(side="left", padx=5)

stream = tk.Label(card, text="Aliran kunci akan tampil di sini setelah proses",
                  bg="#DBEAFE", fg=WARNA, font=("Consolas", 9), justify="left",
                  anchor="w", padx=8, pady=6)
stream.pack(fill="x", pady=(0, 10))

label(card, "Hasil").pack(anchor="w")
output_text = kotak_teks(card, 5)
output_text.pack(pady=(4, 8))

bawah = tk.Frame(card, bg="white")
bawah.pack(fill="x")
status = tk.Label(bawah, text="", bg="white", fg="#64748B", font=(FONT, 9))
status.pack(side="left")
tombol(bawah, "Salin Hasil", salin, "white", WARNA, "#DBEAFE").pack(side="right")

root.mainloop()