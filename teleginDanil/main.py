# cd Desktop\telegindanil
# python main.py
import telebot
import pathlib
import os
from time import sleep
import threading
import random

bot = telebot.TeleBot('6442150141:AAGXiSQNNrYO_Ri6zKWpL1_KcFL3dcr9dAQ')
users = []
bad_words = []
good_words = []
class tUser:
    def __init__(self, id):
        self.id = id
        self.wait_games = False
        self.respect = 10
        self.start = False
    
    def write(self, text):
        for word in text.split():
            if word in bad_words:
                self.respect -= 1
            if word in good_words:
                self.respect += 1
    
    def find(id):
        for user in users:
            if user.id == id:
                return user
        return None
def isYes(text):
    text = text.lower()
    if text[:2] == "ок" or text[:2] == "да" or text[:2] == "го" or "согласен" in text or " да" in text:
        return True
    return False
def isNo(text):
    text = text.lower()
    if text[:2] == "не":
        return True
    return False
def add_user(msg):
    if tUser.find(msg.from_user.id) is None:
        users.append(tUser(msg.from_user.id))
    return users[-1]
def get_user(msg):
    return tUser.find(msg.from_user.id)
def question(msg):
    pass
def heroes(msg):
    pass
def why(msg):
    pass
@bot.message_handler(commands=['start', 'restart'])
def send_welcome(message):
    user = add_user(message)
    bot.send_message(message.from_user.id, "Привет, попиздим?")
    user.start = True

@bot.message_handler(content_types=['text'])
def logic_message(message):
    user = get_user(message)
    msg = message.text
    if user.start:
        if isYes(msg):
            question(message)
        elif isNo(msg):
            bot.send_message(user.id, "ну ладно, может тогда в героев?")
            if isYes(msg):
                heroes(message)
            elif isNo(msg):
                messages = ["", "и в чём твой аргумент", "ну ок, иди нахуй", "бля", "ну ладно, я всё равно занят", "что ещё можно было ожидать"]
                k = random.randint(6)
                if k == 0:
                    why(message)
                else:
                    bot.send_message(user.id, messages[k])
                bot.send_message(user.id, "почему")
                
            else:
                bot.send_message(user.id, "Ответь на мой вопрос")
        else:
            bot.send_message(user.id, "Ответь на мой вопрос")
    else:
        pass

@bot.message_handler(content_types=['voice'])
def audio_message(message):
    bot.send_voice(message.from_user.id, open('chocho.ogg', 'rb'))

def spam():
    while True:
        sleep(1)
        for user in users:
            if random.randint(0, 50000) < user.respect:
                bot.send_message(user.id, "Го в героев?")
                

new_thread = threading.Thread(target=spam)
new_thread.start()
bot.polling()

