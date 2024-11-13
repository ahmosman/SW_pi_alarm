import telepot
from telepot.namedtuple import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os

class Bot:
    def __init__(self, alarm):
        load_dotenv()  # Load environment variables from .env file
        token = os.getenv("TELEPOT_TOKEN")
        self.bot = telepot.Bot(token)
        self.bot.message_loop(self.botLoop)
        self.startedChats = []
        self.alarm = alarm

    def botLoop(self, msg):
        print(msg)
        if 'text' in msg:
            self.handleTextMessage(msg)
        elif 'data' in msg:
            self.handleCallbackQuery(msg)

    def handleTextMessage(self, msg):
        chatId = msg['chat']['id']
        msgText = msg['text']
        if msgText == "/start":
            self.startCommand(chatId)
        elif msgText == "/reset":
            self.resetCommand(chatId)

    def handleCallbackQuery(self, msg):
        queryId = msg['id']
        chatId = msg['message']['chat']['id']
        data = msg['data']
        if data == 'arm_alarm':
            self.alarmArmPending(queryId)

    def startCommand(self, chatId):
        if chatId not in self.startedChats:
            markup = InlineKeyboardMarkup(inline_keyboard=[
                [InlineKeyboardButton(text='Arm Alarm', callback_data='arm_alarm')]
            ])
            self.bot.sendMessage(chatId, "Welcome to alarm bot! Your alarm system is ready.", reply_markup=markup)
            
            if chatId not in self.startedChats:
                self.startedChats.append(chatId)

    def resetCommand(self, chatId):
        if chatId in self.startedChats:
            self.startedChats.remove(chatId)
            self.bot.sendMessage(chatId, "The alarm bot has been reset.")
            self.alarm.setState("alarm_unarmed")

    def alarmArmPending(self, queryId):
        self.bot.answerCallbackQuery(queryId, text="Alarm arm pending.")
        self.alarm.setState("alarm_arm_pending")

    def alarmArmed(self):
        for chatId in self.startedChats:
            self.bot.sendMessage(chatId, "Alarm armed.")

    def sendPassword(self):
        for chatId in self.startedChats:
            self.bot.sendMessage(chatId, "Your password: " + self.alarm.correct_password)
    
    def triggeredAlarm(self):
        for chatId in self.startedChats:
            self.bot.sendMessage(chatId, "Alarm triggered!")
    
    def unarmedAlarm(self):
        for chatId in self.startedChats:
            self.bot.sendMessage(chatId, "Alarm un-armed.")
    
    def wrongPassword(self):
        for chatId in self.startedChats:
            self.bot.sendMessage(chatId, "Wrong password entered.")

