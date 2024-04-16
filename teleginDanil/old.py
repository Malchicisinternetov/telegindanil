from telebot.async_telebot import AsyncTeleBot
from time import sleep
from threading import Timer
import asyncio

users = []
bad_words = []
good_words = []
class tUser:
    def __init__(self, id):
        self.id = id
        self.wait_games = False
        self.respect = 0
    
    def find(id):
        for user in users:
            if user.id == id:
                return user
        return None

bot = AsyncTeleBot('6442150141:AAGXiSQNNrYO_Ri6zKWpL1_KcFL3dcr9dAQ')

@bot.message_handler(content_types=['text'])
async def get_text_messages(msg):
    if tUser.find(msg.from_user.id) is None:
        users.append(tUser(msg.from_user.id))

    if msg.text == "/start":
        start(msg)
    elif msg.text == "/restart":
        restart(msg)
    else:
        talk(msg)

async def start(message):
    await bot.send_message(message.from_user.id, "Привет, попиздим?")

async def restart(message):
    await bot.send_message(message.from_user.id, "Привет, попиздим?")

async def say(id, text):
    await bot.send_message(id, text)

async def talk(msg):
    text = msg.text
    
    if text[-2:].lower() == "да":
        say(msg.from_user.id, "пизда")

asyncio.run(bot.polling())
