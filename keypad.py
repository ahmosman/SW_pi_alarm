import RPi.GPIO as GPIO
import time

# my pi row pins: 29, 31, 33, 35
# my pi col pins: 32, 36, 38

class Keypad:
    def __init__(self, row_pins, col_pins):


        self.row_list = row_pins
        self.col_list = col_pins
        self.input = ""

        self.key_list = [["1", "2", "3"],
                         ["4", "5", "6"],
                         ["7", "8", "9"],
                         ["*", "0", "#"]]

        GPIO.setmode(GPIO.BOARD)

        for row in self.row_list:
            GPIO.setup(row, GPIO.OUT)
            GPIO.output(row, GPIO.HIGH)

        for col in self.col_list:
            GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    def getKey(self):
        for r in self.row_list:
            GPIO.output(r, GPIO.LOW)
            result = [GPIO.input(self.col_list[0]), GPIO.input(self.col_list[1]), GPIO.input(self.col_list[2])]
            if min(result) == 0:
                key = self.key_list[int(self.row_list.index(r))][int(result.index(0))]
                GPIO.output(r, GPIO.HIGH)
                return key
            GPIO.output(r, GPIO.HIGH)
        return None

    def isKey(self, key):
        if self.getKey() == key:
            return True
        return False
    
    def cleanup(self):
        GPIO.cleanup()

    def getInput(self):
        key = self.getKey()
        if key is not None and not self.isKey("*"):
            if key == "#":
                self.input = self.input[:-1]
            else:
                self.input += key
            time.sleep(0.2)
            return self.input
        return self.input
    
    def clearInput(self):
        self.input = ""