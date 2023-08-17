from controllerClient import controllerClient
from tkinter import *
from threading import Thread
from time import sleep

class controllerButton(Label):
    def __init__(self, master, ctlr, *args, direction: str = None, **kwargs):
        super().__init__(master, font = ("Helevetica", 50, "bold"), fg = "#000000", bg = "#f1f1f1", *args, **kwargs)

        self.ctlr = ctlr
        self.direction = direction

        self.bind("<ButtonPress>", self.onPress)
        self.bind("<ButtonRelease>", self.onRelease)
    
    def onPress(self, event):
        self.configure(bg = "#e5e5e5")
        self.updateLog("CMD START_" + self.direction)
    
    def onRelease(self, event):
        self.configure(bg = "#f1f1f1")
        self.updateLog("CMD STOP_" + self.direction)
    
    def updateLog(self, cmd):
        if self.direction in ["FORWARDS", "BACKWARDS"]:
            self.ctlr.driveCommandLog.append(cmd)
        else:
            self.ctlr.steeringCommandLog.append(cmd)

class Controller:
    def __init__(self, server_ip: str, server_port: int):
        self.server_ip = server_ip
        self.server_port = server_port

        self.cc = controllerClient()

        self.driveCommandLog = []
        self.steeringCommandLog = []
    
    def driveCommandMessenger(self):
        while self.window_isAlive:
            if self.cc.connected and len(self.driveCommandLog) > 0:
                self.cc.sendMessage(self.driveCommandLog[0])
                del self.driveCommandLog[0]
            sleep(0.05)
    
    def steeringCommandMessenger(self):
        while self.window_isAlive:
            if self.cc.connected and len(self.steeringCommandLog) > 0:
                self.cc.sendMessage(self.steeringCommandLog[0])
                del self.steeringCommandLog[0]
            sleep(0.05)

    def connectionHandler(self):
        while self.window_isAlive:
            if not self.cc.connected:
                self.updateConnectionDisplay()
                self.cc.connectToServer(self.server_ip, self.server_port)
                sleep(0.5)
            self.updateConnectionDisplay()

    def updateConnectionDisplay(self):
        if self.cc.connected:
            statusText = "CONNECTED"
            statusBg = "#00f000"
        else:
            statusText = "DISCONNECTED"
            statusBg = "#f04010"
        
        self.connectionDisplay.configure(text = statusText, bg = statusBg)

    def onWindowClose(self):
        if self.cc.connected:
            self.cc.sendMessage("SYS CLOSE_CONNECTION")
            print("Disconnected from server")
        self.cc.connected = False

        self.cc.closeConnection()

        self.window_isAlive = False
        self.driveMessage_thread.join()
        self.steeringMessage_thread.join()
        self.connHandler_thread.join()
        self.window.destroy()

    
    def start(self):
        self.window = Tk()
        self.window.geometry("550x400")
        self.window.configure(bg = "#cccccc")
        self.window.protocol("WM_DELETE_WINDOW", self.onWindowClose)
        self.window_isAlive = True

        self.commandTerminal = Frame(self.window, bg = "#ffffff")
        self.commandTerminal.place(x = 20, y = 50, width = 510, height = 100)

        self.connectionDisplay = Label(self.commandTerminal, font = ("Helevetica", 15), fg = "#000000")
        self.connectionDisplay.place(x = 20, y = 30, width = 150, height = 40)
        self.updateConnectionDisplay()

        #add other displays if needed

        self.buttonFrame = Frame(self.window, bg = "#ffffff")
        self.buttonFrame.place(x = 20, y = 180, width = 510, height = 200)


        self.fwdButton = controllerButton(self.buttonFrame, self, text = "↑", direction = "FORWARDS")
        self.fwdButton.place(x = 25, y = 15, width = 165, height = 80)
        self.window.bind("<KeyPress-Up>", lambda event: self.fwdButton.event_generate("<ButtonPress>"))
        self.window.bind("<KeyRelease-Up>", lambda event: self.fwdButton.event_generate("<ButtonRelease>"))

        self.bwdButton = controllerButton(self.buttonFrame, self, text = "↓", direction = "BACKWARDS")
        self.bwdButton.place(x = 25, y = 100, width = 165, height = 80)
        self.window.bind("<KeyPress-Down>", lambda event: self.bwdButton.event_generate("<ButtonPress>"))
        self.window.bind("<KeyRelease-Down>", lambda event: self.bwdButton.event_generate("<ButtonRelease>"))

        self.driveMessage_thread = Thread(target = self.driveCommandMessenger, daemon = True)
        self.driveMessage_thread.start()


        self.leftButton = controllerButton(self.buttonFrame, self, text = "←", direction = "LEFT")
        self.leftButton.place(x = 320, y = 15, width = 80, height = 165)
        self.window.bind("<KeyPress-Left>", lambda event: self.leftButton.event_generate("<ButtonPress>"))
        self.window.bind("<KeyRelease-Left>", lambda event: self.leftButton.event_generate("<ButtonRelease>"))

        self.rightButton = controllerButton(self.buttonFrame, self, text = "→", direction = "RIGHT")
        self.rightButton.place(x = 405, y = 15, width = 80, height = 165)
        self.window.bind("<KeyPress-Right>", lambda event: self.rightButton.event_generate("<ButtonPress>"))
        self.window.bind("<KeyRelease-Right>", lambda event: self.rightButton.event_generate("<ButtonRelease>"))

        self.steeringMessage_thread = Thread(target = self.steeringCommandMessenger, daemon = True)
        self.steeringMessage_thread.start()


        self.connHandler_thread = Thread(target = self.connectionHandler, daemon = True)
        self.connHandler_thread.start()

        self.window.mainloop()

if __name__ == "__main__":
    ctlr = Controller("raspberrypi.local", 8000)
    #ctlr = Controller("localhost", 10000)
    ctlr.start()