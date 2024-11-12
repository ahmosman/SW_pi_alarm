from gpiozero import LED, Buzzer, Button, OutputDevice
from time import time, sleep, strftime
from datetime import datetime
import telepot

led1 = LED(17)
led2 = LED(18)
led3 = LED(27)
led4 = LED(22)
led5 = LED(25)
led6 = LED(12)
led7 = LED(13)
led8 = LED(19)
sw1 = Button(21)
sw2 = Button(16)
sw3 = Button(20)
buzzer = Buzzer(26)

def handle(msg):
  global telegramText
  global chat_id
  global receiveTelegramMessage
  
  chat_id = msg['chat']['id']
  telegramText = msg['text']
  
  print("Message received from " + str(chat_id))
  
  if telegramText == "/start":
    bot.sendMessage(chat_id, "Welcome to Idris Bot")
  
  else:
    buzzer.beep(0.1, 0.1, 1)
    receiveTelegramMessage = True

def sw1Pressed():
    global statusText
    global sendTelegramMessage
    statusText = "SW1 is pressed"
    sendTelegramMessage = True
    buzzer.beep(0.1, 0.1, 1)

def sw2Pressed():
    global statusText
    global sendTelegramMessage
    statusText = "SW2 is pressed"
    sendTelegramMessage = True
    buzzer.beep(0.1, 0.1, 1)
    
def sw3Pressed():
    global statusText
    global sendTelegramMessage
    statusText = "SW3 is pressed"
    sendTelegramMessage = True
    buzzer.beep(0.1, 0.1, 1)

bot = telepot.Bot('PUT YOUR TELEGRAM BOT TOKEN HERE')
bot.message_loop(handle)

print("Telegram bot is ready")

sw1.when_pressed = sw1Pressed
sw2.when_pressed = sw2Pressed
sw3.when_pressed = sw3Pressed

receiveTelegramMessage = False
sendTelegramMessage = False

statusText = ""
led1Status = False
led2Status = False
led3Status = False
led4Status = False
led5Status = False
led6Status = False
led7Status = False
led8Status = False

buzzer.beep(0.1, 0.1, 2)

try:
    while True:
        if receiveTelegramMessage == True:
            receiveTelegramMessage = False

            statusText = ""
            
            if telegramText == "LED1 ON":
                print("Turn on LED1")
                led1Status = True
                led1.on()
            elif telegramText == "LED1 OFF":
                print("Turn off LED1")
                led1Status = False
                led1.off()
            elif telegramText == "LED2 ON":
                print("Turn on LED2")
                led2Status = True
                led2.on()
            elif telegramText == "LED2 OFF":
                print("Turn off LED2")
                led2Status = False
                led2.off()
            elif telegramText == "LED3 ON":
                print("Turn on LED3")
                led3Status = True
                led3.on()
            elif telegramText == "LED3 OFF":
                print("Turn off LED3")
                led3Status = False
                led3.off()
            elif telegramText == "LED4 ON":
                print("Turn on LED4")
                led4Status = True
                led4.on()
            elif telegramText == "LED4 OFF":
                print("Turn off LED4")
                led4Status = False
                led4.off()
            elif telegramText == "LED5 ON":
                print("Turn on LED5")
                led5Status = True
                led5.on()
            elif telegramText == "LED5 OFF":
                print("Turn off LED5")
                led5Status = False
                led5.off()
            elif telegramText == "LED6 ON":
                print("Turn on LED6")
                led6Status = True
                led6.on()
            elif telegramText == "LED6 OFF":
                print("Turn off LED6")
                led6Status = False
                led6.off()
            elif telegramText == "LED7 ON":
                print("Turn on LED7")
                led7Status = True
                led7.on()
            elif telegramText == "LED7 OFF":
                print("Turn off LED2")
                led7Status = False
                led7.off()
            elif telegramText == "LED8 ON":
                print("Turn on LED8")
                led8Status = True
                led8.on()
            elif telegramText == "LED8 OFF":
                print("Turn off LED8")
                led8Status = False
                led8.off()
            else:
                statusText = "Command not valid\n\n"

            statusText = statusText + "Status:\n"
            if led1Status == True:
                statusText = statusText + "LED1 ON\n"
            elif led1Status == False:
                statusText = statusText + "LED1 OFF\n"
            if led2Status == True:
                statusText = statusText + "LED2 ON\n"
            elif led2Status == False:
                statusText = statusText + "LED2 OFF\n"
            if led3Status == True:
                statusText = statusText + "LED3 ON\n"
            elif led3Status == False:
                statusText = statusText + "LED3 OFF\n"
            if led4Status == True:
                statusText = statusText + 'LED4 ON\n'
            elif led4Status == False:
                statusText = statusText + 'LED4 OFF\n'
            if led5Status == True:
                statusText = statusText + 'LED5 ON\n'
            elif led5Status == False:
                statusText = statusText + 'LED5 OFF\n'
            if led6Status == True:
                statusText = statusText + 'LED6 ON\n'
            elif led6Status == False:
                statusText = statusText + 'LED6 OFF\n'
            if led7Status == True:
                statusText = statusText + 'LED7 ON\n'
            elif led7Status == False:
                statusText = statusText + 'LED7 OFF\n'
            if led8Status == True:
                statusText = statusText + 'LED8 ON'
            elif led8Status == False:
                statusText = statusText + 'LED8 OFF'
            
            sendTelegramMessage = True

        if sendTelegramMessage == True:
            sendTelegramMessage = False
            bot.sendMessage(chat_id, statusText)
            

except KeyboardInterrupt:
    led1.off()
    led2.off()
    led3.off()
    led4.off()
    led5.off()
    led6.off()
    led7.off()
    led8.off()
    sys.exit(0)