from tkinter import Canvas, CENTER
from Classes.utils.queens import Queens
from Classes.algos.backtracking import BackTracking
import random

from threading import Thread, Event



# Main class for chess board playground
class NCanvas(Queens):
    def __init__(self):
        super().__init__()
        self.__size = self.board_size
        self.__parent = self.play_frame
        self.board = []

    def create_canvas(self):
        self.board = []
        canvas = Canvas(
            self.__parent, width=self.__size, height=self.__size, bg="white"
        )
        canvas.grid(row=1, column=0)
        self.canvas = canvas
        for i in range(0, self.queens.get()):
            row = []
            for k in range(0, self.queens.get()):
                row.append(0)
            self.board.append(row)

    def draw_board(self):
        queens = self.queens.get()
        box_size = self.__size / queens
        for row in range(0, queens):
            for col in range(0, queens):
                x1, y1 = row * box_size, col * box_size
                x2, y2 = x1 + box_size, y1 + box_size
                color = "white"
                if (row + col) % 2 != 0:
                    color = "#3b3a37"

                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, tags=f"{row},{col}", outline="gray"
                )

    def reset_board(self):
        self.create_canvas()
        self.draw_board()
        self.render_queens()

    # def add_queen(self, row, col):
    #     queens = self.queens.get()
    #     box_size = self.__size / queens

    #     x = row * (box_size) + (int(box_size / 2))
    #     y = col * (box_size) + (int(box_size / 2))

    #     queenid = self.canvas.create_image(
    #         x, y, image=self.queen_img, anchor=CENTER, tags=(row, col)
    #     )
    #     self.canvas.tag_bind(queenid, "<Button-3>", lambda: None)

    #     # self.pop_queens()
    
    def add_queen(self, row, col):
        queens = self.queens.get()
        box_size = self.__size / queens

        x = row * (box_size) + (int(box_size / 2))
        y = col * (box_size) + (int(box_size / 2))

        # Tag with a string, for example "row_col" where row and col are integers
        queenid = self.canvas.create_image(
            y, x, image=self.queen_img, anchor=CENTER, tags=f"{row}_{col}"
        )
        self.canvas.tag_bind(queenid, "<Button-3>", lambda: None)
        
    def remove_queen(self, row, col):
        queenid = self.canvas.find_withtag(f"{row}_{col}")
        
        if queenid:
            self.canvas.delete(queenid)
        

    def random_col(self):
        return random.choice(range(self.queens.get()))
    
    # BackTracking
    def backtrack_solve(self):
        event = Event()
        
        bt = BackTracking(self.queens.get(), self, 0)
        
        run = Thread(target=bt.run, args=(event,))
        run.daemon = True
        run.start()
        
        follow = Thread(target=self.follow_bt, args=(bt, event))
        follow.daemon = True
        follow.start()


            
    def follow_bt(self, bt, event):
        event.wait()
        if bt.found_sol :
            # print("a7aaa")
            data_dict = {'Algorithm':f'{bt.algorithm}','NumberOfQueens':f'{self.queens.get()}'}
            self.success_handler(data_dict)
        else:
            print("wtffffffffffffffffffffffff")

            
