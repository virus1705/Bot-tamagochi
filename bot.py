import datetime

import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from data_manager import game_data, save_chat_data, get_last_location_key, get_location, get_next_location_key, \
    save_game_progress, get_options_label_list, get_random_item, get_options_picture_url_list, \
    get_history_data_for_image, get_last_action_at, user_data
from kandinsky import get_images
from pet import create_pet
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

def create_image(user_id, filename, colour, animal, action, origin=False):
    if origin:
        origin = f"http://localhost:8000/{user_id}/orig.jpg"  # потом заменить на нелокальный
    else:
        origin = None

    get_images(user=user_id, filename=filename,
               prompt=f"{colour} {animal}, миловидный, в портретном стиле на фоне травы и неба."
                      f" Животное на картинке {action}. Фон должен быть немного размытым, "
                      f"а животное чётко изображено.",
               style="Детальное фото", origin=origin)


def make_media_photos(url_list):
    media_photos = []
    for url in url_list:
        media_photos.append(telebot.types.InputMediaPhoto(url))
    return media_photos


@bot.message_handler(commands=["start"])
def handle_start(message):
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
    save_chat_data(message.chat)
    markup = make_keyboard(['да, давай ещё раз!'])
    bot.send_message(message.chat.id, get_go_message(game_data["title"]), reply_markup=markup)


@bot.message_handler(content_types=["text"])
def handle_text(message, location_key: str = None):
    user_id = str(message.chat.id)
    button_text = message.text
    last_location_key = get_last_location_key(user_id)
    last_location = get_location(last_location_key)

    if not last_location_key and button_text == 'давай!' or button_text == 'да, давай ещё раз!':
        next_location_key = "start"
    else:
        if location_key:
            next_location_key = location_key
        else:
            next_location_key = get_next_location_key(last_location, button_text)

    if next_location_key and last_location['options_new'][next_location_key].get('input') and not location_key:
        bot.register_next_step_handler(message, handle_text, next_location_key)
        return

    if get_last_location_key(user_id) == "create":
        animal = user_data[user_id]["history"][-3]["value"]
        pet_name = user_data[user_id]["history"][-2]["value"]
        colour = user_data[user_id]["history"][-1]["value"]

        create_image(user_id, "orig", colour, animal, "смотрит в твою сторону")
        create_image(user_id, "glad", colour, animal, "выглядит довольным", True)
        create_image(user_id, "sad", colour, animal, "выглядит грустным", True)
        create_image(user_id, "angry", colour, animal, "выглядит сердитым", True)
        create_image(user_id, "joy", colour, animal, "выглядит радостным", True)

        pictures = {
            "orig": open(f"user_media/{user_id}/orig.jpg", "rb").read(),
            "glad": open(f"user_media/{user_id}/glad.jpg", "rb").read(),  # доволен
            "sad": open(f"user_media/{user_id}/sad.jpg", "rb").read(),  # грустит
            "angry": open(f"user_media/{user_id}/angry.jpg", "rb").read(),  # сердится
            "joy": open(f"user_media/{user_id}/joy.jpg", "rb").read()  # радуется
        }
        pet, thread = create_pet(pet_name, animal, pictures)
        user_data[user_id]["user_pet"]["pet"] = pet
        user_data[user_id]["user_pet"]["thread"] = thread
        # user_data[user_id]["user_pet"]["pet"].Food() - так теперь аналогично использовать остальные функции,
        # пока не подключена БД


    next_location = get_location(next_location_key)

    options_label_list = get_options_label_list(next_location)
    markup = make_keyboard(options_label_list)

    picture_url = get_random_item(next_location["picture_urls"])
    if picture_url:
        caption = next_location["description"]
        bot.send_photo(message.chat.id, picture_url, caption, reply_markup=markup)
    else:
        text = next_location["description"]
        bot.send_message(message.chat.id, text, reply_markup=markup)
    location_prompt = next_location.get("image_prompt")
    image_uuid = None
    if location_prompt:
        history_data = get_history_data_for_image(user_id)
        history_prompt = history_data['history_as_string'] + ' ' + button_text
        origin_image_uuid = history_data['origin_image_uuid']
        prompt = history_prompt + ' ' + location_prompt
        image_data = get_images(user_id, 'test', prompt)
        image_uuid = image_data['image_uuid']
        image = image_data['image']
        bot.send_photo(message.chat.id, image)

    action = {
        'location_key': next_location["id"],
        'value': button_text,
        'inventory_items': [],
        'used_item': None,
        'image_uuid': image_uuid,
        'action_at': str(datetime.datetime.now()),
    }
    save_game_progress(user_id, action)

    # Функция возвращающая значения времени по каждому действию питомца
    # можно использовать для генерации событий бота
    print(get_last_action_at(user_id))

    options_picture_url_list = get_options_picture_url_list(next_location)
    media_photos = make_media_photos(options_picture_url_list)
    if len(media_photos):
        bot.send_media_group(message.chat.id, media_photos)


bot.polling()
