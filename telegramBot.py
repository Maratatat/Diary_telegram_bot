import telebot
from telebot import types
from DiaryRequests.AuthService import *
from Database import *
from DiaryRequests.TokenService import *

token = '7375063902:AAFmLWHxv93NaHXnomaZjav18lSdI55ydbE'

bot = telebot.TeleBot(token)
auth_button_states = {}
try_again_button_states = {}


# print every message
# when clear history end any process(registration, login, etc.)
@bot.callback_query_handler(func=lambda call: call.data == "try again")
@bot.message_handler(commands=['start'])
def start(message):
    is_callback = hasattr(message, "message")
    if is_callback:
        if message.message.chat.id not in try_again_button_states:
            try_again_button_states[message.message.chat.id] = False
        if not try_again_button_states[message.message.chat.id]:
            try_again_button_states[message.message.chat.id] = True
            pass
        else:
            return
        if message.message.chat.id not in auth_button_states:
            auth_button_states[message.message.chat.id] = False
        if not auth_button_states[message.message.chat.id]:
            pass
        else:
            return
        # try again  can not be called while authorization
    user = GetUserByTelegramId(message.from_user.id)
    if len(user) == 0:
        markup = types.InlineKeyboardMarkup()
        registerItem = types.InlineKeyboardButton("Register", callback_data="register")
        markup.add(registerItem)
        loginItem = types.InlineKeyboardButton("Login", callback_data="login")
        markup.add(loginItem)
        if is_callback:
            bot.send_message(message.message.chat.id,
                             'Welcome to Diary Telegram Bot! Here you can create, update, delete and get your reports.')
            bot.send_message(message.message.chat.id, 'Please select the option below', reply_markup=markup)
        else:
            bot.send_message(message.chat.id,
                             'Welcome to Diary Telegram Bot!Here you can create, update, delete and get your reports.')
            bot.send_message(message.chat.id, 'Please select the option below', reply_markup=markup)
    else:
        if is_callback:
            bot.send_message(message.message.chat.id, "You are already authorized.")
        else:
            response = RefreshToken(user[0][3], user[0][4])
            if response["isSuccess"]:
                LoginUser(response["data"]["userId"], response["data"]["accessToken"], response["data"]["refreshToken"])
                bot.send_message(message.chat.id, "Welcome back")
            else:
                bot.send_message(message.chat.id, "Sorry, your token has expired. Please login again.")
                handle_login(message, True)


@bot.callback_query_handler(func=lambda call: call.data == "register")
def handle_registration(callback_query):
    user = GetUserByTelegramId(callback_query.from_user.id)
    if len(user) == 0:
        if callback_query.message.chat.id not in auth_button_states:
            auth_button_states[callback_query.message.chat.id] = False
        if not auth_button_states[callback_query.message.chat.id]:
            auth_button_states[callback_query.message.chat.id] = True
            user = GetUserByTelegramId(callback_query.message.from_user.id)
            if len(user) == 0:
                user_auth_data = {}
                bot.send_message(callback_query.message.chat.id, "Enter login:")
                bot.register_next_step_handler(callback_query.message, handle_password, user_auth_data, "Register")
    else:
        bot.send_message(callback_query.message.chat.id, "You are already registered.")

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
    try_again_button_states[message.chat.id] = False
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
            markup = types.InlineKeyboardMarkup()
            tryAgainItem = types.InlineKeyboardButton("Try again", callback_data="try again")
            markup.add(tryAgainItem)
            bot.send_message(message.chat.id, "Failed to register. " + responseLogin["errorMessage"] + '.',
                             reply_markup=markup)

    else:
        markup = types.InlineKeyboardMarkup()
        tryAgainItem = types.InlineKeyboardButton("Try again", callback_data="try again")
        markup.add(tryAgainItem)
        bot.send_message(message.chat.id, "Failed to register. " + responseRegister["errorMessage"] + '.',
                         reply_markup=markup)
    auth_button_states[message.chat.id] = False


@bot.callback_query_handler(func=lambda call: call.data == "login")
def handle_login(callback_query):
    user = GetUserByTelegramId(callback_query.from_user.id)
    if len(user) == 0:
        if callback_query.message.chat.id not in auth_button_states:
            auth_button_states[callback_query.message.chat.id] = False
        if not auth_button_states[callback_query.message.chat.id]:
            auth_button_states[callback_query.message.chat.id] = True
            user_auth_data = {}
            bot.send_message(callback_query.message.chat.id, "Enter login:")
            bot.register_next_step_handler(callback_query.message, handle_password, user_auth_data, "Login")
    else:
        bot.send_message(callback_query.message.chat.id, "You are already logged in.")


def complete_login(message, user_auth_data):
    try_again_button_states[message.chat.id] = False
    bot.send_message(message.chat.id, "⏳")
    user_auth_data["password"] = message.text
    responseLogin = Login(user_auth_data["login"], user_auth_data["password"])
    if responseLogin["isSuccess"]:
        LoginUser(responseLogin["data"]["userId"], responseLogin["data"]["accessToken"],
                  responseLogin["data"]["refreshToken"])
        bot.send_message(message.chat.id, "Successfully logged in.")
    else:
        markup = types.InlineKeyboardMarkup()
        tryAgainItem = types.InlineKeyboardButton("Try again", callback_data="try again")
        markup.add(tryAgainItem)
        bot.send_message(message.chat.id, "Failed to login. " + responseLogin["errorMessage"] + '.',
                         reply_markup=markup)
    auth_button_states[message.chat.id] = False


bot.polling(none_stop=True)
