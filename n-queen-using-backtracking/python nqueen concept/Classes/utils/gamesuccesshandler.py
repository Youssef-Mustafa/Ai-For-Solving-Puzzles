from tkinter import Toplevel,Label

class GameSuccessHandler():

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
    
    def handler(self,my_dict):
        game_success_window = Toplevel(self.parent_window)
        game_success_window.resizable(False, False)
        game_success_window.title("Game Info")

        label_text = f"Congratulations!!!\nYou have solved the {my_dict.get('NumberOfQueens',4)}\n Queens Problem Using ({my_dict.get('Algorithm','backTracking')})\n\n" 

        label = Label(game_success_window, text=label_text, font="Arial 14 bold", fg="green")
        label.pack(pady=25)
        
        text_width = max(map(len, label_text.split('\n')))
        text_height = len(label_text.split('\n'))

        # Adjust the window size based on the content
        window_width = max(400, text_width * 11)  # Set a minimum width of 400, adjust as needed
        window_height = max(200, text_height * 25)  # Set a minimum height of 400, adjust as needed

        game_success_window.geometry(f"{window_width}x{window_height}")
        
        self.center_game_over_window(game_success_window)
