from signal import signal, SIGTERM, SIGHUP
from display import Display
from keypad import Keypad
from alarm import Alarm
from bot import Bot
from gpiozero import MotionSensor
import time

class AlarmSystem:
    def __init__(self):
        self.display = Display()
        self.keypad = Keypad([29, 31, 33, 35], [32, 36, 38])
        self.motion_sensor = MotionSensor(14)
        self.alarm = Alarm()
        self.bot = Bot(self.alarm)
        self.last_time_checked = time.time()
        signal(SIGTERM, self.safe_exit)
        signal(SIGHUP, self.safe_exit)

    def safe_exit(self, signum, frame):
        print('Exiting...')
        exit(0)

    def run(self):
        try:
            while True:
                current_time = time.time()

                if self.alarm.isState("alarm_unarmed"):
                    self.display.print("Alarm un-armed", "Use bot to arm")
                
                elif self.alarm.isState("alarm_arm_pending"):
                    pending_time = Alarm.ARM_PENDING_TIME
                    for i in range(pending_time):
                        self.display.print("Alarm armed in", str(pending_time-i) + "s")
                        time.sleep(1)
                    self.armAlarm()

                elif self.alarm.isState("alarm_armed"):
                    self.display.print("Alarm armed")

                    if self.isMotionDetected():
                        self.setGetPassword()
                        self.keypad.clearInput()

                elif self.alarm.isState("get_password"):
                    if current_time - self.last_time_checked >= 1:
                        self.alarm.remaining_time -= 1
                        self.last_time_checked = current_time

                    self.display.print(f"Password:    {self.alarm.remaining_time}s", self.keypad.getInput())

                    if self.keypad.isKey("*"):
                        self.handlePassword()
                        self.keypad.clearInput()

                    if self.alarm.remaining_time <= 0:
                        self.triggerAlarm()

                elif self.alarm.isState("wrong_password"):
                    self.display.print("Wrong password")

                elif self.alarm.isState("alarm_triggered"):
                    self.display.print("Alarm triggered!")
                    # TODO: add telegram Disarm button
                
                elif self.alarm.isState("adding_chat"):
                    self.display.print("Chat key:", self.keypad.getInput())
                    if self.keypad.isKey("*"):
                        self.handleChatCode()
                        self.keypad.clearInput()

        except KeyboardInterrupt:
            pass
        finally:
            print("Cleaning up...")
            self.display.clear()
            self.keypad.cleanup()

    def handlePassword(self):
        if self.alarm.checkPassword(self.keypad.input):
            self.unarmAlarm()
        elif self.alarm.password_attempts >= Alarm.ALLOWED_PASSWORD_ATTEMPTS:
            self.triggerAlarm()
        else:
            self.setWrongPassword()

    def setGetPassword(self):
        self.alarm.setState("get_password")
        self.alarm.resetPassword()
        self.bot.sendPassword()

    def triggerAlarm(self):
        self.alarm.setState("alarm_triggered")
        self.bot.triggeredAlarm()
    
    def armAlarm(self):
        self.alarm.setState("alarm_armed")
        self.bot.alarmArmed()

    def unarmAlarm(self):
        self.alarm.setState("alarm_unarmed")
        self.bot.unarmedAlarm()

    def setWrongPassword(self):
        self.alarm.setState("wrong_password")
        self.display.print("Wrong password")
        self.bot.wrongPassword()
        time.sleep(3)
        self.setGetPassword()

    def handleChatCode(self):
        if self.alarm.checkChatCode(self.keypad.input):
            self.bot.chatVerified()
        else:
            self.display.print("Wrong chat code")
            time.sleep(3)
        self.alarm.resetAddingChat()
        self.alarm.setState("alarm_unarmed")
    
    def isMotionDetected(self):
        return self.motion_sensor.motion_detected

if __name__ == "__main__":
    alarm_system = AlarmSystem()
    alarm_system.run()