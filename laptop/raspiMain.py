from raspiServer import raspiServer
import RPi.GPIO as GPIO
from time import sleep
from threading import Thread

class gpioDriver:
    def __init__(self, rs: raspiServer):
        self.rs = rs
    
    def start(self):
        self.setupGpio()
        
        while True:
            if len(self.rs.cmdStack) > 0:
                cmdPacket = self.rs.cmdStack[0]
                cmd, direction = self.unpackCmd(cmdPacket)

                self.executeCommand(cmd, direction)
                
                del self.rs.cmdStack[0]
            sleep(0.1)
        #GPIO.cleanup()
    
    def executeCommand(self, cmd, direction):
        if cmd == "START":
            if direction == "FORWARDS":
                GPIO.output(self.in1, GPIO.LOW)
                GPIO.output(self.in2, GPIO.HIGH)
            elif direction == "BACKWARDS":
                GPIO.output(self.in1, GPIO.HIGH)
                GPIO.output(self.in2, GPIO.LOW)
            elif direction == "LEFT":
                GPIO.output(self.in3, GPIO.HIGH)
                GPIO.output(self.in4, GPIO.LOW)
            elif direction == "RIGHT":
                GPIO.output(self.in3, GPIO.LOW)
                GPIO.output(self.in4, GPIO.HIGH)
        elif cmd == "STOP":
            if direction in ["FORWARDS", "BACKWARDS"]:
                GPIO.output(self.in1, GPIO.LOW)
                GPIO.output(self.in2, GPIO.LOW)
            else:
                GPIO.output(self.in3, GPIO.LOW)
                GPIO.output(self.in4, GPIO.LOW)
    
    def setupGpio(self):
        self.in1 = 33 
        self.in2 = 35
        self.ena = 37
        
        self.in3 = 36
        self.in4 = 38
        self.enb = 40
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.in1, GPIO.OUT)
        GPIO.setup(self.in2, GPIO.OUT)
        GPIO.setup(self.ena, GPIO.OUT)
        GPIO.output(self.in1, GPIO.LOW)
        GPIO.output(self.in2, GPIO.LOW)
        self.driverMotor = GPIO.PWM(self.ena, 100)
        self.driverMotor.start(100)
        
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.in3, GPIO.OUT)
        GPIO.setup(self.in4, GPIO.OUT)
        GPIO.setup(self.enb, GPIO.OUT)
        GPIO.output(self.in3, GPIO.LOW)
        GPIO.output(self.in4, GPIO.LOW)
        self.steeringMotor = GPIO.PWM(self.enb, 100)
        self.steeringMotor.start(100)
    
    def unpackCmd(self, cmdPacket: str):
        commands = cmdPacket.split("_", maxsplit = 1)
        return commands[0], commands[1]
        

if __name__ == "__main__":
    rs = raspiServer()
    
    rs_thread = Thread(target = rs.startServer, daemon = True)
    rs_thread.start()
    
    gd = gpioDriver(rs)
    driver_thread = Thread(target = gd.start, daemon = True)
    driver_thread.start()

    