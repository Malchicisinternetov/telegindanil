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
        self.respect = 0
        self.start = False
        self.block = False
        self.heroes = False
        self.russian = False
        self.yesterday = False
        self.heroesname = False

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

def inituser(user):
    user.block = False
    user.wait_games = False
    user.heroes = False
    user.russian = False
    user.yesterday = False
    user.heroesname = False

def isNo(text):
    text = text.lower()
    if text[:2] == "не":
        return True
    return False


def add_user(msg):
    if tUser.find(msg.from_user.id) is None:
        users.append(tUser(msg.from_user.id))
        return users[-1]
    return tUser.find(msg.from_user.id)


def get_user(msg):
    return tUser.find(msg.from_user.id)


def tquestion(msg):
    user = get_user(msg)
    say(user, "хочу задать такой вопрос", 1, False)
    k = random.randint(0, 1)
    if k == 0:
        say(user, "что ты делал вчера?", 2)
        user.yesterday = True
    else:
        say(user, "ты сделал русский?", 2)
        user.russian = True
def question(msg):
    nt = threading.Thread(target=tquestion, args=(msg,))
    nt.start()

def theroes(msg):
    user = get_user(msg)

def heroes(msg):
    nt = threading.Thread(target=theroes, args=(msg,))
    nt.start()

def twhy(msg):
    user = get_user(msg)
    say(user, "почему", 5, False)
    say(user, "почему", 10, False)
    say(user, "почему", 15)
def why(msg):
    nt = threading.Thread(target=twhy, args=(msg,))
    nt.start()

def sendsleepmessage(user, text, time, bl):
    if bl:
        user.block = True
    sleep(time)
    bot.send_message(user.id, text)
    if bl:
        user.block = False
def sendsleepvoice(user, vc, time, bl):
    if bl:
        user.block = True
    sleep(time)
    bot.send_voice(user.id, vc)
    if bl:
        user.block = False
def say(user, text, time = 1, bl = True):
    nt = threading.Thread(target=sendsleepmessage, args=(user, text, time, bl,))
    nt.start()
def voice(user, vc, time = 1, bl = True):
    nt = threading.Thread(target=sendsleepvoice, args=(user, vc, time, bl,))
    nt.start(user, vc)


@bot.message_handler(commands=['start', 'restart'])
def send_welcome(message):
    user = add_user(message)
    inituser(user)
    say(user, "Привет, попиздим?")
    user.start = True


@bot.message_handler(content_types=['text'])
def logic_message(message):
    user = get_user(message)
    msg = message.text
    if user.block:
        return
    if user.start:
        if isYes(msg):
            question(message)
            user.start = False
        elif isNo(msg):
            say(user, "ну ладно, может тогда в героев?")
            user.start = False
            user.heroes = True
        else:
            say(user, "ответь на мой вопрос")
    elif user.heroesname:
        user.heroesname = False
        say(user, "тебе выпали ресы:", 1, False)
        resources = ["древесина", "руда", "ртуть", "кристаллы", "сера", "драгоценные камни", "золото"]
        random.shuffle(resources)
        say(user, resources[0], 2, False)
        say(user, resources[1], 2, False)
        say(user, resources[2], 2, False)
        k = random.randint(0, 1)
        if k == 0:
            say(user, "а у меня имба ресы!", 5, False)
            say(user, "тебе конец чел", 15, False)
            say(user, "поздравляю тебя, я выиграл", 25)
        else:
            say(user, "а у меня гавно ресы бля", 5, False)
            say(user, "человек дырявая бошка", 15, False)
            say(user, "бля как же он хорош", 25, False)
            say(user, "ну молодец, ты победил", 28, False)
            say(user, "красава", 31, False)
            say(user, "с сарказмом если что", 32)
    elif user.heroes:
        if isYes(msg):
            user.heroesname = True
            say(user, "напиши как зовут твоего героя")
            user.heroes = False
        elif isNo(msg):
            messages = ["", "и в чём твой аргумент", "ну ок, иди нахуй", "бля", "ну ладно, я всё равно занят",
                        "мм, что ещё можно было ожидать"]
            k = random.randint(0, 5)
            if k == 0:
                why(message)
            else:
                say(user, messages[k])
            user.heroes = False
        else:
            say(user, "ответь на мой вопрос")
    elif user.russian:
        if isYes(msg):
            user.russian = False
        elif isNo(msg):
            user.russian = False
        else:
            say(user, "ответь на мой вопрос")
    elif user.yesterday:
        if isYes(msg):
            user.yesterday = False
        elif isNo(msg):
            user.yesterday = False
        else:
            say(user, "ответь на мой вопрос")
    else:
        if "почему" in msg:
            say(user, "а почему бы и нет?")
        elif len(msg) >= 3 and msg[:3] == "как":
            say(user, "обычно")
        elif len(msg) >= 5 and msg[:5] == "зачем":
            say(user, "затем")
        elif msg[-1] == '?':
            say(user, "не задавай лишних вопросов")
        else:
            pass

@bot.message_handler(content_types=['voice'])
def audio_message(message):
    return
    voice(get_user(message), open('chocho.ogg', 'rb'))


def spam():
    return
    while True:
        sleep(1)
        for user in users:
            if random.randint(0, 50000) < user.respect:
                bot.send_message(user.id, "Го в героев?")


new_thread = threading.Thread(target=spam)
new_thread.start()
bot.polling()
