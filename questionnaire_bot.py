import telebot
from telebot import types
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InputFile
from questionnaire_info import questions, start_message, help_message, users, file_generation, check_result

token = ''
bot = telebot.TeleBot(token)
test_start = False
answers_list = []


def next_question(message):
    user_id = message.chat.id
    if users[user_id]['done'] == 5:
        users[user_id]['current-theme'] = 'Гуманитарные науки'
        users[user_id]['current-index'] += 1
        users[user_id]['current-index'] %= 2
    if users[user_id]['done'] < 10:
        markup = ReplyKeyboardMarkup()
        buttons = []
        for i in range(len(questions[users[user_id]['current-theme']]['answers'][users[user_id]['done'] % 5]) - 1):
            buttons.append(KeyboardButton(text=questions[users[user_id]['current-theme']]
                           ['answers'][users[user_id]['done'] % 5][i]))
        for j in range(len(buttons)):
            if j % 2 == 0:
                try:
                    markup.row(buttons[j], buttons[j + 1])
                except IndexError:
                    markup.row(buttons[j])
        with open(file_generation(questions[users[user_id]['current-theme']]['topic'],
                                  users[user_id]['done'] % 5 + 1), 'rb') as file:
            bot.send_photo(user_id, InputFile(file),
                           reply_markup=markup)
        file.close()
    else:
        users[user_id]['test-process'] = False
        text, photo = check_result(users[user_id])
        with open(photo, 'rb') as file:
            bot.send_photo(user_id, InputFile(file), caption=text, reply_markup=types.ReplyKeyboardRemove())
        file.close()
        print(users)


@bot.message_handler(commands=['start'])
def send_start_message(message):
    bot.send_message(message.chat.id, start_message, reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['help'])
def send_help_message(message):
    bot.send_message(message.chat.id, help_message, reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['starttest'])
def start_test(message):
    global test_start
    test_start = True
    users[message.chat.id] = {'done': 0,
                              'test-process': True,
                              'current-theme': 'Математика',
                              'current-index': 0,
                              'answers': [[], []],
                              'math': 0,
                              'humanitarian': 0}
    next_question(message)


@bot.message_handler(content_types=['text'])
def send_question(message):
    print(users)
    user_id = message.chat.id
    try:
        if users != {} and users[user_id]['test-process']:
            if message.text in questions[users[user_id]['current-theme']]['answers'][users[user_id]['done'] % 5][:4]:
                users[user_id]['answers'][users[user_id]['current-index']].append(message.text)
                if questions[users[user_id]['current-theme']]['answers'][users[user_id]['done'] % 5].index(message.text) == \
                        questions[users[user_id]['current-theme']]['answers'][users[user_id]['done'] % 5][4]:
                    users[user_id][questions[users[user_id]['current-theme']]['topic']] += 1
                users[user_id]['done'] += 1
                next_question(message)
            else:
                bot.send_message(message.chat.id, '❗ Пожалуйста, пользуйтесь кнопками и командами')
        else:
            bot.send_message(message.chat.id, '❗ Пожалуйста, пользуйтесь командами')
    except AttributeError or KeyError:
        bot.send_message(message.chat.id, '❗ Ой, произошла какая-то ошибка. Скоро её исправят!')
        print('❗ Ой, произошла какая-то ошибка. Скоро её исправят!')


@bot.message_handler(content_types=['photo', 'audio', 'video', 'document', 'sticker', 'voice'])
def send_question(message):
    bot.send_message(message.chat.id, '❗ Бот отвечает только на текстовые сообщения')

bot.polling()
