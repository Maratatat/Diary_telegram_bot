import telebot
from telebot import types
from DiaryRequests.AuthService import *
from Database import *

token = '7375063902:AAFmLWHxv93NaHXnomaZjav18lSdI55ydbE'

bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start(message):
    print(message)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    registerItem = types.KeyboardButton("Register")
    markup.add(registerItem)
    loginItem = types.KeyboardButton("Login")
    markup.add(loginItem)
    fastLoginItem = types.KeyboardButton("Fast Login")
    markup.add(fastLoginItem)
    bot.send_message(message.chat.id,
                     'Welcome to Diary Telegram Bot!Here you can create, update, delete and get your reports.')
    bot.send_message(message.chat.id, 'Please select the option below', reply_markup=markup)


@bot.message_handler(func=lambda message: message.text == "Register")
def handle_login(message):
    user_auth_data = {}
    bot.send_message(message.chat.id, "Enter login:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, handle_password, user_auth_data, "Register")


def handle_password(message, user_auth_data, type):
    user_auth_data["login"] = message.text
    bot.send_message(message.chat.id, "Enter password:")
    if type == "Register":
        bot.register_next_step_handler(message, handle_confirm_password, user_auth_data)
    if type == "Login":
        bot.register_next_step_handler(message, complete_login, user_auth_data)


def handle_confirm_password(message, user_auth_data):
    user_auth_data["password"] = message.text
    bot.send_message(message.chat.id, "Confirm password")
    bot.register_next_step_handler(message, complete_registration, user_auth_data)


def complete_registration(message, user_auth_data):
    bot.send_message(message.chat.id, "⏳")
    user_auth_data["passwordConfirm"] = message.text
    responseRegister = Register(user_auth_data["login"], user_auth_data["password"], user_auth_data["passwordConfirm"])
    if responseRegister["isSuccess"]:
        responseLogin = Login(user_auth_data["login"], user_auth_data["password"])
        if responseLogin["isSuccess"]:
            RegisterUser(responseLogin["data"]["userId"], message.from_user.id, responseLogin["data"]["accessToken"],
                         responseLogin["data"]["refreshToken"])
            bot.send_message(message.chat.id, "Successfully registered.")
        else:
            bot.send_message(message.chat.id, "Failed to register. " + responseLogin["errorMessage"] + '.')

    else:
        bot.send_message(message.chat.id, "Failed to register. " + responseRegister["errorMessage"] + '.')


@bot.message_handler(func=lambda message: message.text == "Login")
def handle_login(message):
    user_auth_data = {}
    bot.send_message(message.chat.id, "Enter login:", reply_markup=types.ReplyKeyboardRemove())
    bot.register_next_step_handler(message, handle_password, user_auth_data, "Login")


def complete_login(message, user_auth_data):
    bot.send_message(message.chat.id, "⏳")
    user_auth_data["password"] = message.text
    responseLogin = Login(user_auth_data["login"], user_auth_data["password"])
    if responseLogin["isSuccess"]:
        LoginUser(responseLogin["data"]["userId"], responseLogin["data"]["accessToken"],
                  responseLogin["data"]["refreshToken"])
        bot.send_message(message.chat.id, "Successfully login.")
    else:
        bot.send_message(message.chat.id, "Failed to login. " + responseLogin["errorMessage"] + '.')


bot.polling(none_stop=True)
