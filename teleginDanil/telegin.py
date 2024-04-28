# cd Desktop\telegindanil
# python telegin.py
import telebot
import pathlib
import os
from time import sleep
import threading
import random

bot = telebot.TeleBot('6442150141:AAGXiSQNNrYO_Ri6zKWpL1_KcFL3dcr9dAQ')
EALP = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
users = []
bad_words = []
sIns = []
hIns = []
good_words = ["молодец", "хорош", "красава", "красавчик", "крутой", "гений", "база", "топ", "топчик", "машина", "смешно", "круто", "ахах", "10/10", "10", "зашибись", "смешной", "отличный", "5/5", "5", "7/7", "7"]
phrases = []
fl1 = open("phrases.txt", mode="r")
for st in fl1:
    phrases.append(st.strip())
fl2 = open("badWordsUser.txt", mode="r")
for st in fl2:
    bad_words.append(st.strip())
fl3 = open("simpleInsults.txt", mode="r")
for st in fl3:
    sIns.append(st.strip())
fl4 = open("harshInsults.txt", mode="r")
for st in fl4:
    hIns.append(st.strip())
class tUser:
    def __init__(self, id):
        self.id = id
        self.wait_games = False
        self.reputation = 0
        self.start = False
        self.block = False
        self.heroes = False
        self.russian = False
        self.yesterday = False
        self.heroesname = False
        self.echo = False
        self.whywhywhy = False
        self.mem = False
        self.sorry = False

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
    user.echo = False
    user.whywhywhy = False
    user.mem = False
    user.sorry = False

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


def tquestion(user):
    say(user, "хочу задать такой вопрос", 1, False)
    k = random.randint(0, 1)
    if k == 0:
        say(user, "что ты делал вчера?", 2)
        user.yesterday = True
    else:
        say(user, "ты сделал русский?", 2)
        user.russian = True
def question(user):
    nt = threading.Thread(target=tquestion, args=(user,))
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
    user.whywhywhy = True
def why(msg):
    nt = threading.Thread(target=twhy, args=(msg,))
    nt.start()

def sendsleepmessage(user, text, time, bl):
    if bl:
        user.block = True
    if "*" in text:
        a = text.split("*")
    else:
        a = list()
        a.append(text)
    for now in a:
        sleep(time)
        bot.send_message(user.id, now)
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

def eng(text):
    for letter in text:
            if letter in EALP:
                return True
    return False
def chto(text):
    for word in text.split():
        if word == "че" or word == "чё" or word == "что" or word == "чо" or word == "ачо":
            return True
    return False
def badmsg(text):
    for now in bad_words:
        if now in text:
            return True
    for now in text.split():
        if now.lower() in sIns:
            return True
        elif now.lower() in hIns:
            return True
    return False
def goodmsg(text):
    for now in text.split():
        if now.lower() in good_words:
            return True
    return False

@bot.message_handler(commands=['start', 'restart'])
def send_welcome(message):
    user = add_user(message)
    inituser(user)
    say(user, "Привет, попиздим?")
    user.start = True


@bot.message_handler(content_types=['text'])
def logic_message(message):
    user = get_user(message)
    if user == None:
        return
    msg = message.text
    if user.block:
        return
    if user.start:
        if isYes(msg):
            question(user)
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
            random.shuffle(phrases)
            say(user, phrases[0])
            user.russian = False
        elif isNo(msg):
            say(user, "извинись")
            user.sorry = True
            user.russian = False
        else:
            say(user, "ответь на мой вопрос")
    elif user.sorry:
        if "извини" in msg or "прости" in msg:
            say(user, "прощаю")
            user.sorry = False 
    elif user.yesterday:
        t = ["круто", "а я вчера ботал русский", "ну молодец, и что?", "понятно, это база", "ты прикалываешься"]
        random.shuffle(t)
        say(user, t[0])
        user.yesterday = False
    elif user.echo:
        say(user, msg)
        user.echo = False
    elif user.mem:
        if badmsg(msg):
            say(user, "а, ну ок, иди нахуй")
        elif goodmsg(msg):
            t = ["базовый мем)", "красава", "да ну ты меня обманываешь"]
            random.shuffle(t)
            say(user, t)
        else:
            say(user, "ну ок...")
        user.mem = False
    else:
        if "героев" in msg:
            say(user, "Давай", 1, False)
            say(user, "напиши как зовут твоего героя", 2)
            user.heroesname = True
        elif badmsg(msg) and user.whywhywhy:
            say(user, "я просто задал вопрос почему")
        elif len(msg) >= 2 and (msg[-2].lower() + msg[-1]) == "да":
            say(user, "пизда") 
        elif msg.lower() == "пока":
            say(user, "ну ок, пока")
        elif eng(msg):
            say(user, "скажи по русски")
        elif "почему" in msg:
            t = ["а почему бы и нет?", "а разве нет?", "потому", "ну, ну... мм..", "ну не знаю, подумай"]
            random.shuffle(t)
            say(user, t[0])
        elif len(msg) >= 3 and msg[:3] == "как":
            t = ["ну вот так", "обычно", "мм..", "ну не знаю, подумай"]
            if random.randint(0, 4) == 4:
                say(user, "дай подумать", 1, False)
                say(user, "ну вот так", 12)
            else:
                random.shuffle(t)
                say(user, t[0])
        elif len(msg) >= 5 and msg[:5] == "зачем":
            t = ["а почему бы и нет?", "чтоб ты спросил", "затем", "мм..", "ну не знаю, подумай"]
            if random.randint(0, 5) == 5:
                say(user, "дай подумать", 1, False)
                say(user, "ну не знаю, подумай", 6)
            else:
                random.shuffle(t)
                say(user, t[0])
        elif chto(msg):
            t = ["ЧООО?", "ниче", "ну и всё*ничо", "хм...", "и в чем он не прав", "ой, я тебя умоляю"]
            random.shuffle(t)
            say(user, t[0])
        elif msg[-1] == '?':
            if random.randint(1, 2) == 1:
                t = ["не задавай лишних вопросов", "да*как тебе такой ответ", "нет*как тебе такой ответ"]
                random.shuffle(t)
                say(user, t[0])
            else:
                say(user, "подожди...", 2, False)
                say(user, "дай подумать", 5, False)
                say(user, "мм...", 8, False)
                say(user, "Я не понял твой вопрос, повтори", 10)
                user.echo = True
        elif "пранк" in msg.lower():
            say(user, "Что такое пранк?")
        elif "кринж" in msg.lower():
            say(user, "Что такое кринж?")
        elif "рофл" in msg.lower():
            say(user, "Что такое рофл?")
        elif "прикол" in msg.lower():
            say(user, "Что такое прикол?*это же...")
        else:
            random.shuffle(phrases)
            say(user, phrases[0])
        user.whywhywhy = False

@bot.message_handler(content_types=['voice'])
def audio_message(message):
    path = "chocho"
    path += str(random.randint(1, 4))
    path += ".ogg"
    voice(get_user(message), open(path, 'rb'))

@bot.message_handler(content_types=["audio", "document", "photo", "sticker", "video", "video_note"])
def other_message(message):
    t = ["фу", "че за хуйня?", "база", "гавно"]
    random.shuffle(t)
    say(get_user(message), t[0])

def spam_heroes():
    while True:
        sleep(172800)
        for user in users:
            inituser(user)
            say(user, "Го в героев?")
            user.heroes=True
def spam_memes():
    sleep(1000)
    while True:
        sleep(86400)
        for user in users:
            inituser(user)
            path = "mem"
            path += str(random.randint(1, 11))
            path += ".png"
            bot.send_photo(user.id, open(path, 'rb'))
            say(user, "оцени мем")
            user.mem = True
def spam_questions():
    sleep(2000)
    while True:
        sleep(36000)
        for user in users:
            inituser(user)
            question(user)

nt1 = threading.Thread(target=spam_heroes)
nt1.start()
nt2 = threading.Thread(target=spam_memes)
nt2.start()
nt3 = threading.Thread(target=spam_questions)
nt3.start()
bot.polling()
