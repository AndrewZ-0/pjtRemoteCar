from controller_client import controllerClient
from tkinter import *


class Controller:
    def __init__(self):
        self.cc = controllerClient

    def start(self):
        self.window = Tk()
        self.window.geometry("500x400")

        self.upButton = Button(self)
        self.upButton.place(x = 20, y = 100, width = 100, height = 50)

        self.window.mainloop()

if __name__ == "__main__":
    ctlr = Controller()
    ctlr.start()