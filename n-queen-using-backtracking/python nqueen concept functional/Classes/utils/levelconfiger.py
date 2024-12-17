from tkinter import IntVar, Toplevel, Label, Entry, TclError
from tkinter.messagebox import showwarning
from Classes.utils.controlpanel import ControlPanel
from Classes.utils.levellabel import Level_Label
from Classes.utils.nbutton import NButton


# class for configuring Level and Time
class LevelConfiger(ControlPanel, Level_Label):
    def __init__(self):
        ControlPanel.__init__(self)
        Level_Label.__init__(self)
        self.__level = IntVar()
        self.__level.set(self.queens.get())

    def create_level_config_box(self):
        self.__level.set(self.queens.get())
        level_window = Toplevel(self.window)
        self.__level_window = level_window
        level_window.geometry("400x300")
        level_window.resizable(False, False)
        level_window.title("Level Setting")

        label = Label(level_window, text="Level :", font=("Arial", 14))
        label.pack(pady=10)

        level_box = Entry(
            level_window, textvariable=self.__level, width=15, font=("Arial", 14)
        )
        level_box.pack(padx=10, pady=10)

        NButton(level_window, "Set", "#4287f5", self.change_level)

    def change_level(self):
        # Exception handling when user's input is not valid
        try:
            level = self.__level.get()
            if level < 4:
                showwarning(
                    "Invalid Level",
                    "The level is limted greater than or equal 4!",
                    parent=self.__level_window,
                )
            else:
                self.queens.set(level)
                self.reset_board()
                self.reset_level_label()
                self.__level_window.destroy()
                self.backtrack_solve_button.btn.config(background="#4CAF50")
                self.backtrack_solve_button.btn.config(state="normal")
        except TclError:
            showwarning("Invalid input", "The level input must be integer")

