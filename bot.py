import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from data_manager import game_data, save_chat_data, get_last_location_key, get_location, get_next_location_key, \
    save_game_progress, get_options_label_list, get_random_item, get_options_picture_url_list
from texts import texts, get_go_message

token = '7127498607:AAGXrqLuP6w7D_KovytWZ_1qzyjjV6Z3mxI'
bot = telebot.TeleBot(token=token)

chat_id = 1376797948

bot.send_message(chat_id, f"бот был запущен")


def make_keyboard(items):
    markup = ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
    for item in items:
        markup.add(KeyboardButton(item))

    return markup


def make_media_photos(url_list):
    media_photos = []
    for url in url_list:
        media_photos.append(telebot.types.InputMediaPhoto(url))
    return media_photos


@bot.message_handler(commands=["start"])
def handle_start(message):
    print(message.chat.username, ": ", message.text)
    save_chat_data(message.chat)
    bot.send_message(message.chat.id, texts["welcome"])
    markup = make_keyboard(['давай!'])

    cover_url = game_data["cover_url"]
    if cover_url:
        caption = get_go_message(game_data["title"])
        bot.send_photo(message.chat.id, cover_url, caption, reply_markup=markup)
    else:
        text = get_go_message(game_data["title"])
        bot.send_message(message.chat.id, text, reply_markup=markup)


@bot.message_handler(commands=["again"])
def handle_start(message):
    print(message.chat.username, ": ", message.text)
    save_chat_data(message.chat)
    markup = make_keyboard(['да, давай ещё раз!'])
    bot.send_message(message.chat.id, get_go_message(game_data["title"]), reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handle_text(message):
    user_id = str(message.chat.id)
    button_text = message.text

    last_location_key = get_last_location_key(user_id)
    last_location = get_location(last_location_key)

    if not last_location_key and button_text == 'давай!' or button_text == 'да, давай ещё раз!':
        next_location_key = "start"
    else:
        next_location_key = get_next_location_key(last_location, button_text)

    next_location = get_location(next_location_key)
    action = {
        'location_key': next_location["id"],
        'inventory_items': [],
        'used_item': None
    }
    save_game_progress(user_id, action)

    options_label_list = get_options_label_list(next_location)
    markup = make_keyboard(options_label_list)

    picture_url = get_random_item(next_location["picture_urls"])
    if picture_url:
        caption = next_location["description"]
        bot.send_photo(message.chat.id, picture_url, caption, reply_markup=markup)
    else:
        text = next_location["description"]
        bot.send_message(message.chat.id, text, reply_markup=markup)
    options_picture_url_list = get_options_picture_url_list(next_location)
    media_photos = make_media_photos(options_picture_url_list)
    if len(media_photos):
        bot.send_media_group(message.chat.id, media_photos)


bot.polling()
