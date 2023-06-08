import customtkinter as ctk
from customtkinter import CTkButton
from settings import *

class Button(CTkButton):
    def __init__(self, parent, text, row, col):
        super().__init__(
            master=parent,
            text=text,
            corner_radius=10,
            bg_color=BG_COLOR
            )
        self.grid(column=col, columnspan=1, row=row, sticky='nsew', padx=5, pady=5)