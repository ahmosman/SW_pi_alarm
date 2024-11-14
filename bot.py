import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os
import json

class Bot:
    def __init__(self, alarm):
        load_dotenv()
        token = os.getenv("TELEPOT_TOKEN")
        self.bot = telepot.Bot(token)
        self.bot.message_loop(self.botLoop)
        self.verified_chats = self.loadVerifiedChats()
        self.alarm = alarm

    def botLoop(self, msg):
        print(msg)

        chat_id = self.getChatIdFromMessage(msg)
        msg_text = msg.get('text')
        data = msg.get('data')
        
        if not self.isVerifiedChat(chat_id):
            if msg_text != "/start":
                self.bot.sendMessage(chat_id, "You are not verified. Please use /start to verify.")
            else:
                self.addNewChatCommand(msg['chat'])
            return


        if msg_text:
            self.handleTextMessage(msg_text, chat_id)
        elif data:
            self.handleCallbackQuery(data, msg['id'])

    def handleTextMessage(self, msg_text, chat_id):
        if msg_text == "/start":
            self.bot.sendMessage(chat_id, "You are already verified.", reply_markup=self.getReplyMarkup())
        if msg_text == "/list":
            self.listVerifiedChats(chat_id)

    def handleCallbackQuery(self, data, query_id):
        if data == 'arm_alarm':
            self.alarmArmPending(query_id)

    def addNewChatCommand(self, chat_data):
        chat_id = chat_data['id']
        if not self.alarm.isState("alarm_unarmed"):
            self.bot.sendMessage(chat_id, "Can't add user when alarm is armed.")
            return

        if not self.alarm.canAddChat(chat_id):
            self.bot.sendMessage(chat_id, "Another user is adding a chat.")
            return

        self.alarm.setAddingChat(chat_data)
        code = self.alarm.generateCodeForChat()
        self.bot.sendMessage(chat_id, f"Your code is: {code}. Please enter this code in the keypad.")
        self.alarm.setState("adding_chat")

    def alarmArmPending(self, query_id):
        if self.alarm.canArm():
            self.alarm.setState("alarm_arm_pending")
            self.bot.answerCallbackQuery(query_id, text="Alarm arm pending.")
        else:
            self.bot.answerCallbackQuery(query_id, text="Alarm is not ready to arm.")

    def notifyChats(self, message, reply_markup=None):
        for chat_id in self.verified_chats:
            self.bot.sendMessage(chat_id, message, reply_markup=reply_markup)

    def alarmArmed(self):
        self.notifyChats("Alarm armed.")

    def sendPassword(self):
        self.notifyChats(f"Your password: {self.alarm.correct_password}")

    def triggeredAlarm(self):
        self.notifyChats("Alarm triggered!")

    def unarmedAlarm(self):
        self.notifyChats("Alarm un-armed.", reply_markup=self.getReplyMarkup())

    def wrongPassword(self):
        self.notifyChats("Wrong password entered.")

    def chatVerified(self):
        chat_id = int(self.alarm.adding_chat['id'])
        self.verified_chats[chat_id] = self.alarm.adding_chat
        self.bot.sendMessage(chat_id, "Welcome to alarm bot! Your alarm system is ready.", reply_markup=self.getReplyMarkup())
        self.saveVerifiedChats()

    def getReplyMarkup(self):
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text='Arm Alarm', callback_data='arm_alarm')]
        ])

    def saveVerifiedChats(self):
        os.makedirs('./data', exist_ok=True)
        with open('./data/verified_chats.json', 'w') as f:
            json.dump(self.verified_chats, f)

    def loadVerifiedChats(self):
        try:
            with open('./data/verified_chats.json', 'r') as f:
                data = json.load(f)
                data = {int(k): v for k, v in data.items()}
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def isVerifiedChat(self, chat_id):
        print("verified_chats", self.verified_chats)
        return chat_id in self.verified_chats
    
    def listVerifiedChats(self, chat_id):
        
        #list as e.g.:
        #1. John Doe, joined on 2024-01-01 12:00
        #2. Jack Black, joined on 2024-11-30 23:59
    
        chat_list = []
        for i, (key, chat) in enumerate(self.verified_chats.items(), start=1):
            chat_list.append(f"{i}. {chat['first_name']} {chat['last_name']}, joined on {chat['date_joined']}")
        
        chat_list_str = "\n".join(chat_list)
        
        self.bot.sendMessage(chat_id, chat_list_str)
    
    def getChatIdFromMessage(self, msg):
        if 'chat' in msg:
            return msg['chat']['id']
        if 'from' in msg:
            return msg['from']['id']
        return None
