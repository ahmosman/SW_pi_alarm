import RPi.GPIO as GPIO
import time

# Set the Row Pins
ROW_1 = 29
ROW_2 = 31
ROW_3 = 33
ROW_4 = 35

# Set the Column Pins
COL_1 = 32
COL_2 = 36
COL_3 = 38

row_list = [ROW_1, ROW_2, ROW_3, ROW_4]
col_list = [COL_1, COL_2, COL_3]

GPIO.setmode(GPIO.BOARD)

for row in row_list:
    GPIO.setup(row, GPIO.OUT)
    GPIO.output(row, GPIO.HIGH)

for col in col_list:
    GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_UP)

key_list = [["1", "2", "3"],
            ["4", "5", "6"],
            ["7", "8", "9"],
            ["*", "0", "#"]]

def keypad(col, row):
    for r in row:
        GPIO.output(r, GPIO.LOW)
        result = [GPIO.input(col[0]), GPIO.input(col[1]), GPIO.input(col[2])]
        if min(result) == 0:
            key = key_list[int(row.index(r))][int(result.index(0))]
            GPIO.output(r, GPIO.HIGH)
            return key
        GPIO.output(r, GPIO.HIGH)

try:
    while True:
        key = keypad(col_list, row_list)
        if key is not None:
            print("key: " + key)
            time.sleep(0.3)
finally:
    GPIO.cleanup()