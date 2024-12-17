from tkinter import *
from Classes.utils.levelconfiguration import LevelConfiguration


class App(LevelConfiguration):

    def __init__(self):

        super().__init__()

    def start(self):

        self.create_level_button()
        self.render_level_label()
        self.create_canvas()
        self.draw_board()
        self.render_queens()
        self.create_control_panel()
        self.window.protocol("WM_DELETE_WINDOW", self.destroy_all)
        self.window.mainloop()


App().start()
