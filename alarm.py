import random
from datetime import datetime
import time

# States description:
# alarm_unarmed: alarm is unarmed
# alarm_armed: alarm is armed
# get_password: get password from user
# wrong_password: wrong password entered
# alarm_triggered: alarm is triggered
# alarm_arm_pending: alarm is pending to be armed
# adding_chat: adding chat to alarm system

class Alarm:
    ALLOWED_PASSWORD_ATTEMPTS = 3
    TIME_TO_PROVIDE_PASSWORD = 21  # in seconds
    ARM_PENDING_TIME = 5  # in seconds

    def __init__(self):
        self.state = "alarm_unarmed"
        self.correct_password = None
        self.adding_chat = {}
        self.chat_code = None
        self.password_attempts = 0
        self.remaining_time = None

    def setState(self, state):
        self.state = state

    def isState(self, state):
        return self.state == state

    def resetPassword(self):
        self.correct_password = str(random.randint(1000, 9999))
        self.remaining_time = Alarm.TIME_TO_PROVIDE_PASSWORD

    def checkPassword(self, password):
        if password.rstrip('*') == self.correct_password:
            return True
        self.password_attempts += 1
        return False

    def setAddingChat(self, chat_data):
        self.adding_chat = {
            'id': chat_data['id'],
            'first_name': chat_data.get('first_name', ''),
            'last_name': chat_data.get('last_name', ''),
            'date_joined': datetime.now().strftime('%Y-%m-%d %H:%M')
        }

    def generateCodeForChat(self):
        self.chat_code = str(random.randint(1000, 9999))
        return self.chat_code

    def canAddChat(self, chat_id):
        return self.adding_chat.get('id') == chat_id or not self.adding_chat

    def checkChatCode(self, code):
        return code == self.chat_code

    def resetAddingChat(self):
        self.adding_chat = {}
        self.chat_code = None
    
    def canArm(self):
        return all(not self.isState(state) for state in ["alarm_armed", "alarm_arm_pending", "get_password", "wrong_password"])