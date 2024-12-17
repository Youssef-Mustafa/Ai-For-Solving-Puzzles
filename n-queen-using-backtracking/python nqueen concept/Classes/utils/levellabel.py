from tkinter import Label, Frame, CENTER
from Classes.utils.board import Board


class Level_Label(Board):
    def __init__(self):
        # To prevent the Board class being initiated multiple times
        # as it would create multiple Tk() window object
        if not hasattr(self, "window"):
            super().__init__()

        self.welcome_frame = Frame(self.window)
        self.welcome_frame.grid(row=1, column=0, sticky="nsew", pady=15, columnspan=2)

    def render_level_label(self):
        self.welcome_text = Label(
            self.welcome_frame,
            text=f"NQueens Level : {self.queens.get()}",
            font=("Arial", 14),
        )
        self.welcome_text.pack(anchor=CENTER)

    def reset_level_label(self):
        self.welcome_text.destroy()
        self.render_level_label()
