import tkinter as tk
from tkinter import ttk


class Step1(ttk.Frame):
    def __init__(self, parent, go_next):
        super().__init__(parent)
        tk.Label(self, text="Step 1: Connect Spotify + Deezer").pack(pady=20)
        ttk.Button(self, text="Next", command=go_next).pack()
        # Classic widgets
        tk.Label(self, text="Classic Tkinter Label").pack(pady=5)
        tk.Button(self, text="Classic Button").pack(pady=5)

        # Themed widgets
        ttk.Label(self, text="Themed ttk Label").pack(pady=5)
        ttk.Button(self, text="Themed Button").pack(pady=5)


class Step2(ttk.Frame):
    def __init__(self, parent, go_next, go_back):
        super().__init__(parent)
        ttk.Label(self, text="Step 2: Select Transfer Direction").pack(pady=20)
        ttk.Button(self, text="Back", command=go_back).pack(side="left", padx=10)
        ttk.Button(self, text="Next", command=go_next).pack(side="right", padx=10)


class Step3(ttk.Frame):
    def __init__(self, parent, go_back):
        super().__init__(parent)
        ttk.Label(self, text="Step 3: Select Playlists").pack(pady=20)
        ttk.Button(self, text="Back", command=go_back).pack()


class MusicShifter(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Music Shifter Wizard")
        self.geometry("400x300")

        # Container frame for swapping steps
        self.container = ttk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.show_step1()

    def clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_step1(self):
        self.clear_container()
        Step1(self.container, go_next=self.show_step2).pack(fill="both", expand=True)

    def show_step2(self):
        self.clear_container()
        Step2(self.container, go_next=self.show_step3, go_back=self.show_step1).pack(fill="both", expand=True)

    def show_step3(self):
        self.clear_container()
        Step3(self.container, go_back=self.show_step2).pack(fill="both", expand=True)


if __name__ == "__main__":
    MusicShifter().mainloop()
