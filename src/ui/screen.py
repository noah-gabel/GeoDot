import customtkinter as ctk

class Screen(ctk.CTkFrame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def show(self):
        self.pack(fill="both", expand=True)

    def hide(self):
        self.pack_forget()