import random


#states description:
# alarm_unarmed: alarm is unarmed
# alarm_armed: alarm is armed
# get_password: get password from user
# wrong_password: wrong password entered
# alarm_triggered: alarm is triggered
# alarm_arm_pending: alarm is pending to be armed

class Alarm:
    def __init__(self):
        self.state = "alarm_unarmed"
        self.input_password = ""
        self.password_attempts = 0
        self.correct_password = None
    
    def setState(self, state):
        self.state = state
    
    def getPassword(self):
        return self.password
    
    def isMotionDetected(self, input):
        if input == "22*":
            return True
        return False
    
    def isState(self, state):
        return self.state == state

    def resetPassword(self):
        self.correct_password = str(random.randint(1000, 9999))

    def checkPassword(self, password):
        # Remove * from end of password if it exists
        password = password.rstrip('*')
        if password == self.correct_password:
            return True
        self.password_attempts += 1
        return False
