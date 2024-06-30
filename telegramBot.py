import functools
import telebot
from telebot import types
from DiaryRequests.AuthService import *
from Database import *
from DiaryRequests.TokenService import *
from DiaryRequests.ReportService import *

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
        else:
            return
        if message.message.chat.id not in auth_button_states:
            auth_button_states[message.message.chat.id] = False
        if auth_button_states[message.message.chat.id]:
            return
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
                handle_login(message)


@bot.callback_query_handler(func=lambda call: call.data == "register")
def handle_registration(callback_query):
    user = GetUserByTelegramId(callback_query.from_user.id)
    if len(user) == 0:
        if callback_query.message.chat.id not in auth_button_states:
            auth_button_states[callback_query.message.chat.id] = False
        if not auth_button_states[callback_query.message.chat.id]:
            auth_button_states[callback_query.message.chat.id] = True
            user = GetUserByTelegramId(callback_query.from_user.id)
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
    is_callback = hasattr(callback_query, "message")
    is_login_again = False
    if is_callback:
        message = callback_query.message
    else:
        message = callback_query
        is_login_again = True
    if len(user) == 0 or is_login_again:
        if message.chat.id not in auth_button_states:
            auth_button_states[message.chat.id] = False
        if not auth_button_states[message.chat.id]:
            auth_button_states[message.chat.id] = True
            user_auth_data = {}
            bot.send_message(message.chat.id, "Enter login:")
            bot.register_next_step_handler(message, handle_password, user_auth_data, "Login")
    else:
        bot.send_message(message.chat.id, "You are already logged in.")


def complete_login(message, user_auth_data):
    try_again_button_states[message.chat.id] = False

    user_auth_data["password"] = message.text
    responseLogin = Login(user_auth_data["login"], user_auth_data["password"])
    if responseLogin["isSuccess"]:
        user = GetUserByTelegramId(message.from_user.id)
        if len(user) == 0:
            RegisterUser(responseLogin["data"]["userId"], message.from_user.id, responseLogin["data"]["accessToken"],
                         responseLogin["data"]["refreshToken"])
        else:
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


@bot.message_handler(commands=['getmyreports'])
def HandleGetMyReports(message):
    if CheckIsUserAuthorized(message):
        user = GetUserByTelegramId(message.from_user.id)[0]
        response = GetReportsOfUser(user[1], user[3])
        if "isSuccess" in response:
            if response["isSuccess"]:
                tgResponse = ''
                counter = 0
                for report in response["data"]:
                    tgResponse += f'{report["dateCreated"]}\n<b>{report["name"]}</b>\n{report["description"]}\nId: {report["id"]}'
                    if counter < len(response["data"]) - 1:
                        tgResponse += '\n\n'
                    counter += 1

                bot.send_message(message.chat.id, "Your reports:\n" + tgResponse, parse_mode='HTML')
            else:
                bot.send_message(message.chat.id, "Failed to get your reports:\n" + response["errorMessage"])
        else:
            AuthorizeAndCompleteAction(user, HandleGetMyReports, message)


@bot.message_handler(commands=['getreportbyid'])
def HandleGetReportById(message):
    if CheckIsUserAuthorized(message):
        user = GetUserByTelegramId(message.from_user.id)[0]
        bot.send_message(message.chat.id, "Enter report id:")
        bot.register_next_step_handler(message, functools.partial(CompleteGetReportById, user=user))


def CompleteGetReportById(message, user):
    id = message.text
    if not id.isdigit():
        bot.send_message(message.chat.id, "Report id must be an integer")
        return
    response = GetReportById(id, user[3])
    if "isSuccess" in response:
        if response["isSuccess"]:
            tgResponse = f'{response["data"]["dateCreated"]}\n<b>{response["data"]["name"]}</b>\n{response["data"]["description"]}\nId: {response["data"]["id"]}'
            bot.send_message(message.chat.id, "Your report:\n" + tgResponse, parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, "Failed to get your report:\n" + response["errorMessage"])
    elif response["responseStatusCode"] == 403:
        bot.send_message(message.chat.id, "This is not your report")
    else:
        AuthorizeAndCompleteAction(user, functools.partial(CompleteGetReportById, message=message), message)


@bot.message_handler(commands=['deletereport'])
def HandleDeleteReportById(message):
    if CheckIsUserAuthorized(message):
        user = GetUserByTelegramId(message.from_user.id)[0]
        bot.send_message(message.chat.id, "Enter report id:")
        bot.register_next_step_handler(message, functools.partial(CompleteDeleteReportById, user=user))


def CompleteDeleteReportById(message, user):
    id = message.text
    if not id.isdigit():
        bot.send_message(message.chat.id, "Report id must be an integer")
        return
    response = DeleteReport(id, user[3])
    if "isSuccess" in response:
        if response["isSuccess"]:
            tgResponse = f'{response["data"]["dateCreated"]}\n<b>{response["data"]["name"]}</b>\n{response["data"]["description"]}\nId: {response["data"]["id"]}'
            bot.send_message(message.chat.id, "Your report has been deleted:\n" + tgResponse, parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, "Failed to delete your report:\n" + response["errorMessage"])
    elif response["responseStatusCode"] == 403:
        bot.send_message(message.chat.id, "This is not your report")
    else:
        AuthorizeAndCompleteAction(user, functools.partial(CompleteDeleteReportById, message=message), message)


@bot.message_handler(commands=['createreport'])
def HandleCreateReport(message):
    if CheckIsUserAuthorized(message):
        user = GetUserByTelegramId(message.from_user.id)[0]
        bot.send_message(message.chat.id, "Enter report name:")
        reportData = {}
        bot.register_next_step_handler(message, handleReportDescription, reportData, user, "create")


def handleReportDescription(message, reportData, user, action):
    reportData["name"] = message.text
    bot.send_message(message.chat.id, "Enter report description:")
    if action == "create":
        bot.register_next_step_handler(message, CompleteCreateReport, user, reportData)
    if action == "update":
        bot.register_next_step_handler(message, CompleteUpdateReport, user, reportData)


def CompleteCreateReport(message, user, reportData):
    reportData["description"] = message.text
    response = CreateReport(reportData["name"], reportData["description"], user[1], user[3])
    if "isSuccess" in response:
        if response["isSuccess"]:
            tgResponse = f'{response["data"]["dateCreated"]}\n<b>{response["data"]["name"]}</b>\n{response["data"]["description"]}\nId: {response["data"]["id"]}'
            bot.send_message(message.chat.id, "Your report has been created:\n" + tgResponse, parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, "Failed to create your report:\n" + response["errorMessage"])
    elif response["responseStatusCode"] == 403:
        bot.send_message(message.chat.id, "This is not your report")
    else:
        AuthorizeAndCompleteAction(user, functools.partial(CompleteCreateReport, message=message,
                                                           reportData=reportData), message)


@bot.message_handler(commands=['updatereport'])
def HandleUpdateReport(message):
    if CheckIsUserAuthorized(message):
        user = GetUserByTelegramId(message.from_user.id)[0]
        bot.send_message(message.chat.id, "Enter report id:")
        reportData = {}
        bot.register_next_step_handler(message, handleReportId, reportData, user)


def handleReportId(message, reportData, user):
    reportData["id"] = message.text
    bot.send_message(message.chat.id, "Enter report name:")
    bot.register_next_step_handler(message, handleReportDescription, reportData, user, "update")


def CompleteUpdateReport(message, user, reportData):
    reportData["description"] = message.text
    if not reportData["id"].isdigit():
        bot.send_message(message.chat.id, "Report id must be an integer")
        return
    response = UpdateReport(reportData["id"], reportData["name"], reportData["description"], user[3])
    if "isSuccess" in response:
        if response["isSuccess"]:
            tgResponse = f'{response["data"]["dateCreated"]}\n<b>{response["data"]["name"]}</b>\n{response["data"]["description"]}\nId: {response["data"]["id"]}'
            bot.send_message(message.chat.id, "Your report has been updated:\n" + tgResponse, parse_mode='HTML')
        else:
            bot.send_message(message.chat.id, "Failed to updateAll your report:\n" + response["errorMessage"])
    elif response["responseStatusCode"] == 403:
        bot.send_message(message.chat.id, "This is not your report")
    else:
        AuthorizeAndCompleteAction(user, functools.partial(CompleteCreateReport, message=message,
                                                           reportData=reportData), message)


def AuthorizeAndCompleteAction(user, callback, message):
    refreshResponse = RefreshToken(user[3], user[4])
    if refreshResponse["isSuccess"]:
        LoginUser(refreshResponse["data"]["userId"], refreshResponse["data"]["accessToken"],
                  refreshResponse["data"]["refreshToken"])
        callback(user=GetUserByTelegramId(message.from_user.id)[0])
    else:
        bot.send_message(message.chat.id, "Sorry, your token has expired. Please login again.")
        handle_login(message)


def CheckIsUserAuthorized(message):
    user = GetUserByTelegramId(message.from_user.id)
    if len(user) != 0:
        return True
    bot.send_message(message.chat.id, "You are not authorized.")
    return False


bot.polling(none_stop=True)
