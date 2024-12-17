

from tkinter import Toplevel,Label

class GameLoseHandler():

    def __init__(self, window):
        self.parent_window = window

    def center_game_over_window(self, top_window) :

        root_x = self.parent_window.winfo_rootx()
        root_y = self.parent_window.winfo_rooty()
        root_width = self.parent_window.winfo_width()
        root_height = self.parent_window.winfo_height()

        window_width = top_window.winfo_reqwidth()
        window_height = top_window.winfo_reqheight()

        x = root_x + (root_width - window_width) // 4
        y = root_y + (root_height - window_height) // 4
        
        top_window.geometry("+%d+%d" % (x, y))
        top_window.update_idletasks()
        top_window.grab_set()


    #Use polymorphism to customize the handler function
    def handler(self, queens):

        game_lose_window = Toplevel(self.parent_window)
        game_lose_window.geometry("400x200")
        game_lose_window.resizable(False, False)
        game_lose_window.title("No Answers")

        label = Label(game_lose_window, text=f"There is no solution to\nthe {queens} Queens Problem\nStarting with this row.", 
                      font="Arial 14 bold", fg="red")
        label.pack(pady= 50)
        self.center_game_over_window(game_lose_window)
