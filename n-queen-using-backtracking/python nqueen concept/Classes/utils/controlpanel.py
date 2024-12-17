from tkinter import Frame
from Classes.utils.chessboard import NCanvas
from Classes.utils.nbutton import NButton
from matplotlib import pyplot as plt


# Controller of the game
class ControlPanel(NCanvas):
    def __init__(self):
        super().__init__()

    def create_control_panel(self):
        btn_frame = Frame(self.control_frame, width=self.board_size, padx=50)

        btn_frame.grid(row=0, column=0, sticky="nsew")

        self.backtrack_solve_button = NButton(
            btn_frame, "BackTracking", "#4CAF50", callback=self.backtrack
        )
        
        NButton(btn_frame, "Reset", "#FF5733", callback=self.reset_game)

    def backtrack(self):
        self.backtrack_solve_button.btn.config(background="#eeeeee")
        self.backtrack_solve_button.btn.config(state="disabled")

        self.backtrack_solve()
  
        
    def reset_game(self):
        self.reset_board()
        self.backtrack_solve_button.btn.config(background="#4CAF50")
        self.backtrack_solve_button.btn.config(state="normal")
        plt.close('all')
            
