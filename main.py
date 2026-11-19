import tkinter as tk
from tkinter import ttk, messagebox
import random
import string
import pyperclip

# --- colors ---
BG = "#1e1e2e"
SURFACE = "#2a2a3e"
ACCENT = "#7c3aed"
ACCENT_HOVER = "#6d28d9"
TEXT = "#e2e8f0"
MUTED = "#94a3b8"
SUCCESS = "#22c55e"
WARNING = "#f59e0b"
DANGER = "#ef4444"

def get_strength(password):
    score = 0
    if len(password) >= 8: score += 1
    if len(password) >= 14: score += 1
    if any(c.islower() for c in password): score += 1
    if any(c.isupper() for c in password): score += 1
    if any(c.isdigit() for c in password): score += 1
    if any(c in string.punctuation for c in password): score += 1

    if score <= 2:
        return "Weak", DANGER
    elif score <= 4:
        return "Medium", WARNING
    else:
        return "Strong", SUCCESS


def generate_password(length, use_upper, use_lower, use_digits, use_symbols):
    chars = ""
    if use_upper: chars += string.ascii_uppercase
    if use_lower: chars += string.ascii_lowercase
    if use_digits: chars += string.digits
    if use_symbols: chars += string.punctuation

    if not chars:
        return None

    # guarantee at least one char from each selected set
    guaranteed = []
    if use_upper: guaranteed.append(random.choice(string.ascii_uppercase))
    if use_lower: guaranteed.append(random.choice(string.ascii_lowercase))
    if use_digits: guaranteed.append(random.choice(string.digits))
    if use_symbols: guaranteed.append(random.choice(string.punctuation))

    rest = [random.choice(chars) for _ in range(length - len(guaranteed))]
    all_chars = guaranteed + rest
    random.shuffle(all_chars)
    return "".join(all_chars)


class PasswordGenerator:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Password Generator")
        self.root.geometry("520x560")
        self.root.resizable(False, False)
        self.root.configure(bg=BG)

        self.length_var = tk.IntVar(value=16)
        self.use_upper = tk.BooleanVar(value=True)
        self.use_lower = tk.BooleanVar(value=True)
        self.use_digits = tk.BooleanVar(value=True)
        self.use_symbols = tk.BooleanVar(value=True)
        self.history = []

        self.build_ui()
        self.generate()

    def build_ui(self):
        # title
        tk.Label(self.root, text="Password Generator", font=("Segoe UI", 20, "bold"),
                 bg=BG, fg=TEXT).pack(pady=(25, 5))
        tk.Label(self.root, text="generate strong passwords instantly",
                 font=("Segoe UI", 10), bg=BG, fg=MUTED).pack(pady=(0, 20))

        # password display
        display_frame = tk.Frame(self.root, bg=SURFACE, bd=0)
        display_frame.pack(padx=30, fill="x")

        self.password_var = tk.StringVar()
        self.password_entry = tk.Entry(
            display_frame, textvariable=self.password_var,
            font=("Courier New", 13), bg=SURFACE, fg=TEXT,
            bd=0, relief="flat", width=28, show=""
        )
        self.password_entry.pack(side="left", padx=15, pady=15)

        copy_btn = tk.Button(display_frame, text="Copy", font=("Segoe UI", 10, "bold"),
                             bg=ACCENT, fg="white", bd=0, padx=14, pady=6,
                             cursor="hand2", command=self.copy_password,
                             activebackground=ACCENT_HOVER, activeforeground="white")
        copy_btn.pack(side="right", padx=10, pady=10)

        # strength bar
        strength_frame = tk.Frame(self.root, bg=BG)
        strength_frame.pack(padx=30, fill="x", pady=(8, 0))

        self.strength_label = tk.Label(strength_frame, text="Strength: —",
                                       font=("Segoe UI", 10), bg=BG, fg=MUTED)
        self.strength_label.pack(side="left")

        self.strength_bar = tk.Canvas(strength_frame, width=120, height=8, bg=SURFACE,
                                      bd=0, highlightthickness=0)
        self.strength_bar.pack(side="right", pady=6)

        # length slider
        length_frame = tk.Frame(self.root, bg=BG)
        length_frame.pack(padx=30, fill="x", pady=(20, 5))

        tk.Label(length_frame, text="Length", font=("Segoe UI", 11),
                 bg=BG, fg=TEXT).pack(side="left")

        self.length_display = tk.Label(length_frame, text="16",
                                       font=("Segoe UI", 11, "bold"), bg=BG, fg=ACCENT)
        self.length_display.pack(side="right")

        self.slider = tk.Scale(self.root, from_=6, to=64, orient="horizontal",
                               variable=self.length_var, bg=BG, fg=TEXT,
                               troughcolor=SURFACE, highlightthickness=0,
                               activebackground=ACCENT, bd=0, showvalue=False,
                               command=self.on_slider)
        self.slider.pack(padx=30, fill="x")

        # checkboxes
        opts_frame = tk.Frame(self.root, bg=BG)
        opts_frame.pack(padx=30, fill="x", pady=(15, 5))

        tk.Label(opts_frame, text="Include", font=("Segoe UI", 11),
                 bg=BG, fg=TEXT).pack(anchor="w", pady=(0, 8))

        checks = [
            ("Uppercase (A-Z)", self.use_upper),
            ("Lowercase (a-z)", self.use_lower),
            ("Numbers (0-9)", self.use_digits),
            ("Symbols (!@#...)", self.use_symbols),
        ]

        grid = tk.Frame(opts_frame, bg=BG)
        grid.pack(fill="x")
        for i, (label, var) in enumerate(checks):
            cb = tk.Checkbutton(grid, text=label, variable=var,
                                font=("Segoe UI", 10), bg=BG, fg=TEXT,
                                selectcolor=SURFACE, activebackground=BG,
                                activeforeground=TEXT, bd=0,
                                command=self.generate)
            cb.grid(row=i // 2, column=i % 2, sticky="w", padx=5, pady=3)

        # buttons
        btn_frame = tk.Frame(self.root, bg=BG)
        btn_frame.pack(padx=30, pady=20, fill="x")

        gen_btn = tk.Button(btn_frame, text="Generate New Password",
                            font=("Segoe UI", 12, "bold"), bg=ACCENT, fg="white",
                            bd=0, pady=10, cursor="hand2", command=self.generate,
                            activebackground=ACCENT_HOVER, activeforeground="white")
        gen_btn.pack(fill="x", pady=(0, 10))

        hist_btn = tk.Button(btn_frame, text="Show History",
                             font=("Segoe UI", 10), bg=SURFACE, fg=TEXT,
                             bd=0, pady=7, cursor="hand2", command=self.show_history,
                             activebackground="#3a3a5e", activeforeground=TEXT)
        hist_btn.pack(fill="x")

        # copied label (hidden by default)
        self.copied_label = tk.Label(self.root, text="Copied to clipboard!",
                                     font=("Segoe UI", 10), bg=BG, fg=SUCCESS)
        self.copied_label.pack()
        self.copied_label.pack_forget()

    def on_slider(self, val):
        self.length_display.config(text=str(val))
        self.generate()

    def generate(self):
        pw = generate_password(
            self.length_var.get(),
            self.use_upper.get(),
            self.use_lower.get(),
            self.use_digits.get(),
            self.use_symbols.get()
        )
        if pw is None:
            messagebox.showwarning("oops", "Pick at least one character type.")
            return

        self.password_var.set(pw)
        self.history.append(pw)
        if len(self.history) > 20:
            self.history.pop(0)
        self.update_strength(pw)

    def update_strength(self, password):
        label, color = get_strength(password)
        self.strength_label.config(text=f"Strength: {label}", fg=color)

        self.strength_bar.delete("all")
        levels = {"Weak": 1, "Medium": 2, "Strong": 3}
        filled = levels[label]
        for i in range(3):
            x0 = i * 42
            fill = color if i < filled else SURFACE
            self.strength_bar.create_rectangle(x0, 0, x0 + 36, 8, fill=fill, outline="")

    def copy_password(self):
        pw = self.password_var.get()
        if pw:
            try:
                pyperclip.copy(pw)
            except Exception:
                self.root.clipboard_clear()
                self.root.clipboard_append(pw)
            self.copied_label.pack()
            self.root.after(2000, self.copied_label.pack_forget)

    def show_history(self):
        if not self.history:
            messagebox.showinfo("History", "No passwords generated yet.")
            return

        win = tk.Toplevel(self.root)
        win.title("Password History")
        win.geometry("420x380")
        win.configure(bg=BG)
        win.resizable(False, False)

        tk.Label(win, text="Recent Passwords", font=("Segoe UI", 14, "bold"),
                 bg=BG, fg=TEXT).pack(pady=15)

        frame = tk.Frame(win, bg=BG)
        frame.pack(fill="both", expand=True, padx=20)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        listbox = tk.Listbox(frame, font=("Courier New", 10), bg=SURFACE, fg=TEXT,
                             bd=0, selectbackground=ACCENT, activestyle="none",
                             yscrollcommand=scrollbar.set)
        listbox.pack(fill="both", expand=True)
        scrollbar.config(command=listbox.yview)

        for pw in reversed(self.history):
            listbox.insert("end", f"  {pw}")

        def copy_selected():
            sel = listbox.curselection()
            if sel:
                pw = listbox.get(sel[0]).strip()
                try:
                    pyperclip.copy(pw)
                except Exception:
                    win.clipboard_clear()
                    win.clipboard_append(pw)

        tk.Button(win, text="Copy Selected", font=("Segoe UI", 10),
                  bg=ACCENT, fg="white", bd=0, pady=7, cursor="hand2",
                  command=copy_selected,
                  activebackground=ACCENT_HOVER, activeforeground="white").pack(
                      fill="x", padx=20, pady=15)

    def run(self):
        self.root.mainloop()


app = PasswordGenerator()
app.run()
