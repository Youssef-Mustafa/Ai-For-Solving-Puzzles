from tkinter import Label
from Classes.utils.board import Board
from Classes.utils.gamesuccesshandler import GameSuccessHandler
from Classes.utils.gamelosehandler import GameLoseHandler


class Queens(Board):
    def __init__(self):
        if not hasattr(self, "window"):
            super().__init__()

        self.algos = []

        self.col = 0
        self.success_handler = GameSuccessHandler(self.window).handler
        self.lose_handler = GameLoseHandler(self.window).handler
        self.number_of_queens = self.queens.get()
        self.queen_icon_label = Label(
            self.queen_frame,
            image=self.queen_icon,
            width=100,
            height=40,
            compound="left",
            font=("Arial", 22, "bold"),
        )

    def render_queens(self):
        self.number_of_queens = self.queens.get()

        self.queen_icon_label.config(text=f"X{self.number_of_queens}")

        self.queen_icon_label.grid(row=0, column=7)

    def pop_queens(self):
        if self.number_of_queens == 0:
            return

        self.number_of_queens -= 1
        self.queen_icon_label.config(text=f"X{self.number_of_queens}")

        # if self.number_of_queens == 0:
        #     self.success_handler(self.queens.get())
        

    def append_queens(self):
        if self.number_of_queens > self.queens.get():
            return


        self.number_of_queens += 1
        self.queen_icon_label.config(text=f"X{self.number_of_queens}")
