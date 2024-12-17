from tkinter import Button
from tkinter.messagebox import askyesno
from Classes.utils.levelconfiger import LevelConfiger


class LevelConfiguration(LevelConfiger):
    
    def __init__(self):
        LevelConfiger.__init__(self)

    def create_level_button(self):
        self.level_button = Button(self.window, text="Choose Level", bg="#87CEEB", command=self.create_level_config_box, width=25, font=("Arial",12 )).grid(column=0, row=0,pady=(20,0))
        
    def exit(self):
        if askyesno("Quit", "Are you sure you want to Quit?"):
            exit(1)
        else:
            return
