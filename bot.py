import datetime
import json
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from data_manager import game_data, save_chat_data, get_last_action, get_location, \
    save_game_progress, get_options_label_list, get_random_item, get_options_picture_url_list, \
    get_actions_history, user_data, get_next_location_key_by_value
from kandinsky import get_images
from pet import create_pet
from picture_manager import generate_images
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


@bot.message_handler(commands=["status"])
def handle_status(message):
    user_id = str(message.chat.id)
    status = user_data[user_id]["user_pet"]["pet"].Print_characteristics()
    status_text = (f"Имя: {status["name"]}\n"
                   f"Животное: {status["animal"]}\n"
                   f"Здоровье: {status["health"]}\n"
                   f"Сытость: {status["food"]}\n"
                   f"Веселость: {status["fun"]}\n"
                   f"Бодрость: {status["vivacity"]}\n"
                   f"{status["time"]}")
    bot.send_message(message.chat.id, status_text)


@bot.message_handler(content_types=["text"])
def handle_text(message, location_key: str = ''):
    user_id = str(message.chat.id)
    button_text = message.text
    value = message.text
    last_action = get_last_action(user_id)
    last_location_key = last_action.get('next_location_key')
    last_location = get_location(last_location_key)

    if not last_location_key and button_text == 'давай!' or button_text == 'да, давай ещё раз!' or button_text == 'заново':
        last_location_key = 'start'
        next_location_key = "pet"
    else:
        if location_key:
            next_location_key = location_key
        else:
            next_location_key = get_next_location_key_by_value(last_location, button_text)

    if user_data[user_id]["user_pet"]["creating"]:
        markup = make_keyboard([])
        bot.send_message(message.chat.id, 'Питомец еще не родился... Ждите!', reply_markup=markup)
        return

    action_location_key = last_location_key
    if last_action['location_key'] == last_location_key:
        action_location_key = '_' + last_location_key
    action = {
        'location_key': action_location_key,
        'value': value,
        'next_location_key': next_location_key,
        'inventory_items': [],
        'used_item': None,
        'action_at': str(datetime.datetime.now()),
    }

    save_game_progress(user_id, action)

    if (next_location_key and last_location['options_new'].get(next_location_key) and
            last_location['options_new'][next_location_key].get('input') and not location_key):
        bot.register_next_step_handler(message, handle_text, next_location_key)
        return

    if next_location_key == "name":
        actions_history = get_actions_history(user_id)
        animal = actions_history.get('pet').get('last_value')
        pet_name = actions_history.get('name').get('last_value')
        color = actions_history.get('color').get('last_value')
        bot.send_message(message.chat.id, 'Теперь нужно немного подождать "рождения" твоего питомца...', reply_markup=None)

        user_data[user_id]["user_pet"]["creating"] = True
        pictures = generate_images(user_id, animal, pet_name, color)

        pet, thread = create_pet(pet_name, animal, pictures)
        user_data[user_id]["user_pet"]["pet"] = pet  # отсюда взаимодействие с данными питомца
        user_data[user_id]["user_pet"]["thread"] = thread
        user_data[user_id]["user_pet"]["creating"] = False
        bot.send_photo(message.chat.id, pictures['orig'], 'Привет, хозяин!')

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
    # location_prompt = next_location.get("image_prompt")
    # if location_prompt:
    #     history_data = get_history_data_for_image(user_id)
    #     history_prompt = history_data['history_as_string'] + ' ' + button_text
    #     origin_image_uuid = history_data['origin_image_uuid']
    #     prompt = history_prompt + ' ' + location_prompt
    #     image_data = get_images(user_id, 'test', prompt)
    #     # image_uuid = image_data['image_uuid']
    #     image = image_data
    #     bot.send_photo(message.chat.id, image)

    # Функция возвращающая значения времени по каждому действию питомца
    # можно использовать для генерации событий бота
    # print(get_actions_history(user_id))

    options_picture_url_list = get_options_picture_url_list(next_location)
    media_photos = make_media_photos(options_picture_url_list)
    if len(media_photos):
        bot.send_media_group(message.chat.id, media_photos)

    msg, pic = [None, None]
    if next_location_key == 'feed':
        msg, pic = user_data[user_id]["user_pet"]["pet"].Food()
    if next_location_key == 'play':
        msg, pic = user_data[user_id]["user_pet"]["pet"].Play()
    if next_location_key == 'sleep':
        msg, pic = user_data[user_id]["user_pet"]["pet"].Sleep()
    if next_location_key == 'wake':
        msg, pic = user_data[user_id]["user_pet"]["pet"].wake_up()
    if next_location_key == 'clean':
        msg, pic = user_data[user_id]["user_pet"]["pet"].To_clean()
    if next_location_key == 'toilet':
        msg, pic = user_data[user_id]["user_pet"]["pet"].to_toilet()
    if next_location_key == 'sad':
        msg, pic = user_data[user_id]["user_pet"]["pet"].Sad()
    if next_location_key == 'hunger':
        msg, pic = user_data[user_id]["user_pet"]["pet"].Hunger()
    if msg and pic:
        bot.send_photo(message.chat.id, pic, msg)


bot.polling()
