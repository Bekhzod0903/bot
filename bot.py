import telebot
from telebot import types

bot = telebot.TeleBot('7325213593:AAE7kERLzBkVzkGNxp7qEDePz3AOXsK_1Rc')

# In-memory storage for registered users and state tracking
registered_users = {}
user_states = {}

# Define states
STATE_WAITING_FOR_USERNAME = 1
STATE_WAITING_FOR_PASSWORD = 2

@bot.message_handler(commands=['start'])
def start_message(message):
    username = message.from_user.username if message.from_user.username else "User"
    bot.send_message(message.chat.id,
                     f'Salom @{username}, agar site da muammo bolgan bolsa 1ni jonating\n'
                     'agar sizgaham shunga oxshash sitelar kerak bolsa 2 ni jonating\n'
                     'agar sizda taklif yoki shikoyatlar bolgan bolsa 3 ni jonating')

@bot.message_handler(func=lambda message: True)
def info(message):
    user_id = message.from_user.id
    if message.text == '1':
        bot.send_message(message.chat.id, 'Agar sizda site da muammo bolgan bolsa @Code_Snake7 ga boglaning')
    elif message.text == '2':
        if user_id in registered_users:
            bot.send_message(message.chat.id, 'Siz allaqachon royxatdan otgansiz.')
        else:
            bot.send_message(message.chat.id, 'Sizni royxatdan otkazishimiz uchun iltimos usernameingizni kiriting:')
            user_states[user_id] = STATE_WAITING_FOR_USERNAME
    elif message.text == '3':
        bot.send_message(message.chat.id, 'Agar sizda taklif yoki shikoyatlar bolgan bolsa @userga murojat qiling')
    else:
        current_state = user_states.get(user_id)
        if current_state == STATE_WAITING_FOR_USERNAME:
            # Save username and ask for password
            user_states[user_id] = (STATE_WAITING_FOR_PASSWORD, message.text)
            bot.send_message(message.chat.id, 'Iltimos, parolingizni kiriting:')
        elif current_state and current_state[0] == STATE_WAITING_FOR_PASSWORD:
            # Save password and complete registration
            username = current_state[1]
            password = message.text
            registered_users[user_id] = {
                'username': username,
                'password': password,
                'telegram_username': message.from_user.username,
                'first_name': message.from_user.first_name,
                'last_name': message.from_user.last_name
            }
            del user_states[user_id]
            bot.send_message(message.chat.id, 'Siz muvaffaqiyatli royxatdan otdingiz! Sizga 24 soat ichida adminlarimizdan biri aloqaga chiqadi.')
        else:
            bot.send_message(message.chat.id, 'Iltimos 1, 2 yoki 3 ni tanlang')

bot.polling()
