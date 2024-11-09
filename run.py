from signal import signal, SIGTERM, SIGHUP, pause
from rpi_lcd import LCD
import time

lcd = LCD()

def safe_exit(signum, frame):
    print('Exiting...')
    exit(0)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

try:
    lcd.text("Hello World!", 1)
    i = 0
    while True:
        lcd.text("Ahmi Ania " + str(i), 2)
        i += 1
        time.sleep(1)
    pause()
except KeyboardInterrupt:
    pass
finally:
    lcd.clear()