import config
import telebot
from telebot import types
import json
import requests


bot = telebot.TeleBot(config.token)


# не забудьте про from telebot import types
@bot.message_handler(commands=["start"])
def navigation(message):
    # Эти параметры для клавиатуры необязательны, просто для удобства
    keyboard = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    button_taps = types.KeyboardButton(text="Пиво на кранах")
    button_bottles = types.KeyboardButton(text="Пиво в бутылках")
    button_menu = types.KeyboardButton(text="Меню")
    keyboard.add(button_taps, button_bottles, button_menu)
    bot.send_message(message.chat.id, "Привет! 🖖 \n\nЯ буду делиться с тобой актуальной пивной картой в нашем пабе \"Beerbook\"! 😉  \n\nКакую категорию пива хочешь просмотреть?", reply_markup=keyboard)


@bot.message_handler(content_types=["text"])
def check_message(message):
    # Если сообщение из чата с ботом
    if format(message.text) == "Пиво на кранах":
        with open("beer_taps.json", "r") as taps_response:
            positions = json.load(taps_response)
        readyText = ""
        num = 1
        for position in positions:
            readyText += "⚡️ " + str(num) + ". " + position["position"] + "\n"
            num += 1

        bot.send_message(message.chat.id, readyText)
    elif format(message.text) == "Пиво в бутылках":
        with open("beer_bottles.json", "r") as bottles_response:
            positions = json.load(bottles_response)
        readyText = ""
        beerSorts = []
        for sort in positions:
            if sort["beer"] not in beerSorts:
                beerSorts.append(sort["beer"])
        print(beerSorts)
        for sort in beerSorts:
            readyText += "\n🍻 " + sort + ":\n"
            for position in positions:
                if position["beer"] == sort:
                    readyText += "📍 " + position["position"] + "\n"

        bot.send_message(message.chat.id, readyText)
    elif format(message.text) == "Меню":

        bot.send_media_group(message.chat.id, [{'type': 'photo', 'media': 'http://stomat.testupwork.in.ua/wp-content/uploads/beer_menu.jpg' }, {'type': 'photo', 'media': 'http://stomat.testupwork.in.ua/wp-content/uploads/beer_menu.jpg'}])
        # bot.send_photo(chat_id=message.chat.id, photo=open('beer_menu.jpg', 'rb'))

if __name__ == '__main__':
    bot.polling(none_stop=True)


