from signal import signal, SIGTERM, SIGHUP
from display import Display
from keypad import Keypad
from alarm import Alarm

display = Display()
keypad = Keypad([29, 31, 33, 35], [32, 36, 38])
alarm = Alarm()

def safe_exit(signum, frame):
    print('Exiting...')
    exit(0)

signal(SIGTERM, safe_exit)
signal(SIGHUP, safe_exit)

if __name__ == "__main__":
    try:
        keypad_chars = ""
        alarm.setState("get_password")
        while True:
            display.printTop(alarm.getMessage())
            if alarm.state == "get_password":
                display.printBottom(keypad.getInput())
                if keypad.isKey("*"):
                    alarm.setPassword(keypad.input)
                    keypad.clearInput()
            if alarm.state == "password_set":
                display.printBottom(alarm.getPassword())
                if keypad.isKey("#"):
                    alarm.setState("get_password")
    except KeyboardInterrupt:
        pass # display.clear()
    finally:
        print("Cleaning up...")
        display.clear()
        keypad.cleanup()