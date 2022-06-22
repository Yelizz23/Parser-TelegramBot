import requests
from bs4 import BeautifulSoup as bs
import random
import telebot
from telebot import types


URL = 'https://www.anekdot.ru/last/good/'
API_TOKEN = '5511532136:AAHXafwmPHqgw6uSvEFcj9Q0nuBSQqz917o'


def parser(url):
    r = requests.get(url)
    # print(r.status_code)
    # print(r.text)

    soup = bs(r.text, 'html.parser')
    jokes = soup.find_all('div', class_='text')
    # print (jokes)
    return [c.text for c in jokes]


# clear_jokes = [c.text for c in jokes]
# print(clear_jokes)

jokes_list = parser(URL)
random.shuffle(jokes_list)
bot = telebot.TeleBot(API_TOKEN)


@bot.message_handler(content_types=['photo'])
def get_photo(message):
    bot.send_message(message.chat.id, 'Wow, cool photo!')


@bot.message_handler(commands=['website'])
def website(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton('Visit website', url='https://www.anekdot.ru'))
    bot.send_message(message.chat.id, 'Go to the website', reply_markup=markup)


@bot.message_handler(commands=['start'])
def start(message):
    msg = f'Hello, <b>{message.from_user.first_name} <u>{message.from_user.last_name}!</u></b>\n' \
          f"Enter any number form 1 to 9, or enter 'Help' for more information.\n\n!!!ENJOY!!!"
    bot.send_message(message.chat.id, msg, parse_mode='html')


@bot.message_handler(content_types=['text'])
def joke(message):
    if message.text.lower() in '123456789':
        bot.send_message(message.chat.id, jokes_list[0])
        del jokes_list[0]
    elif message.text.lower() == 'hello':
        bot.send_message(message.chat.id, 'Hey, there!', parse_mode='html')
    elif message.text.lower() == 'help':
        help = f'<b>Enter following keywords:\nid</b> - show my ID number\n' \
               f'<b>website</b> - if you like to visit website\n' \
               f'<b>Or you could send me your photo :)</b>'
        bot.send_message(message.chat.id, help, parse_mode='html')
    elif message.text.lower() == 'how are you?':
        bot.send_message(message.chat.id, 'Very well, thank you!', parse_mode='html')
    elif message.text.lower() == 'id':
        bot.send_message(message.chat.id, f'Your ID is {message.from_user.id}', parse_mode='html')
    else:
        bot.send_message(message.chat.id, "I don't understand you!", parse_mode='html')


@bot.message_handler(commands=['website'])
def website(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    markup.add(types.InlineKeyboardButton('Would you like to visit website?', url='https://www.anekdot.ru'))
    bot.send_message(message.chat.id, 'Go to the website', reply_markup=markup)


bot.polling(none_stop=True)
