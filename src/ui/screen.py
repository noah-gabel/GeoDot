"""Base class for different screens."""

import customtkinter as ctk

class Screen(ctk.CTkFrame):
    """A frame that fills the whole window and can be shown or hidden.

    Screens are created once and toggled with ``show`` and ``hide``, so their widgets and loaded map tiles are kept between switches.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def show(self):
        self.pack(fill="both", expand=True)

    def hide(self):
        self.pack_forget()