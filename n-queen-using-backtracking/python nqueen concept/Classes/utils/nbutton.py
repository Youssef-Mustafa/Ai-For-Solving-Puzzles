from tkinter import Button,CENTER

class NButton:
    def __init__(self, parent, text, color, callback=lambda: None, state="normal"):
        self.__parent = parent
        self.__width = 20
        self.__hieght = 2
        self.__text = text
        self.__color = color
        self.__font = ("Arial", 12)
        self.btn = Button(
            self.__parent,
            width=self.__width,
            height=self.__hieght,
            text=self.__text,
            bg=self.__color,
            font=self.__font,
            command=callback,
            state=state,
        )
        self.btn.config(disabledforeground=self.btn.cget("fg"))
        self.btn.pack(anchor=CENTER, pady=10)