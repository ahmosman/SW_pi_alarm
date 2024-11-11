from rpi_lcd import LCD

class Display:
    def __init__(self):
        self.lcd = LCD()

    def printTop(self, message):
        self.lcd.text(message, 1)

    def printBottom(self, message):
        self.lcd.text(message, 2)

    def clear(self):
        self.lcd.clear()