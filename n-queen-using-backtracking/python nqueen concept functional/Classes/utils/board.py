from tkinter import Tk,IntVar,PhotoImage,Frame
from matplotlib import pyplot as plt



class Board(object):
    def __init__(self):
        self.board_size = 600
        self.window = Tk()
        self.window.resizable(False, False)
        self.window.title("NQueens_AI")
        self.queens = IntVar()
        self.queens.set(4)

        self.queen_icon = PhotoImage(file="Images/queen_icon.png")
        self.queen_img = PhotoImage(file="Images/queen.png")
        self.setting_img = PhotoImage(file="Images/setting.png").zoom(2,2)

        self.body_frame = Frame(self.window)
        self.body_frame.grid(row=2, column=0, padx=20, pady=5)

        self.play_frame = Frame(self.body_frame)
        self.play_frame.grid(row=0, column=0,columnspan=10)

        self.control_frame = Frame(
            self.body_frame,
            width=self.board_size,
            padx=10,
            pady=60,
        )

        self.control_frame.grid(row=0, column=11, sticky="nsew")

        self.queen_frame = Frame(
            self.play_frame,
            width=self.board_size,
            pady=5,
        )
        self.queen_frame.grid(row=0, column=0, rowspan=1, columnspan=10)
        
    def destroy_all(self):
        plt.close('all')
        self.window.destroy()
