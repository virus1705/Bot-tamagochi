import json
from random import randint


def load_game_data():
    file_with_json = open('game_data.json', 'r+', encoding='utf8')
    loaded_game_data = json.load(file_with_json)
    file_with_json.close()
    return loaded_game_data


game_data = load_game_data()


def load_user_data():
    file_with_json = open('user_data.json', 'r+', encoding='utf8')
    loaded_user_data = json.load(file_with_json)
    file_with_json.close()
    return loaded_user_data


user_data = load_user_data()


def update_user_data():
    file_for_json = open('user_data.json', 'w', encoding='utf8')
    json.dump(user_data, file_for_json, ensure_ascii=False)
    file_for_json.close()


def get_location(location_key):

    location = game_data['location_data'].get(location_key)
    print(location_key, location)
    if location:
        return location
    location_404 = game_data['location_data']['404']
    return location_404


def get_last_location_key(user_id):
    last_location_key = ""
    user_data_by_id = user_data.get(user_id)
    if user_data_by_id:
        history = user_data_by_id["locations_history"]
        if len(history):
            last_location_key = history[-1]
    return last_location_key


def get_next_location_key(last_location, option_text):
    next_location_key = ""
    options = last_location["options_new"]
    options_keys = list(options)
    for option_key in options_keys:
        if options[option_key]["label"] == option_text:
            next_location_key = option_key
    return next_location_key


def get_random_item(items_list):
    random_index = randint(0, len(items_list) - 1)
    item = items_list[random_index]
    return item


def save_chat_data(chat_data):
    user_id = str(chat_data.id)
    name = chat_data.first_name
    username = chat_data.username
    user_data[user_id] = {}
    user_data[user_id]['user_id'] = user_id
    user_data[user_id]['name'] = name
    user_data[user_id]['username'] = username
    user_data[user_id]['locations_history'] = []
    user_data[user_id]['inventory'] = []
    user_data[user_id]['used_inventory'] = []
    update_user_data()


def save_game_progress(user_id, action):
    location_key = action['location_key']
    inventory_items = action['inventory_items']
    used_inventory_item = action['used_item']
    if location_key:
        user_data[user_id]['locations_history'].append(location_key)
    if inventory_items:
        user_data[user_id]['inventory'].extend(inventory_items)
    if used_inventory_item:
        user_data[user_id]['used_inventory'].append(used_inventory_item)
    update_user_data()


def get_options_label_list(location):
    button_list = []
    data = location["options_new"].values()
    for item in data:
        label = item["label"]
        button_list.append(label)
    return button_list


def get_options_picture_url_list(location):
    button_list = []
    data = location["options_new"].values()
    for item in data:
        url = item["picture_url"]
        if url:
            button_list.append(url)
    return button_list
