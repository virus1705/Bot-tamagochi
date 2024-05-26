import datetime
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
    return {}
    # return loaded_user_data


user_data = load_user_data()


def update_user_data():
    return
    # file_for_json = open('user_data.json', 'w', encoding='utf8')
    # json.dump(user_data, file_for_json, ensure_ascii=False)
    # file_for_json.close()


def get_location(location_key):
    location = game_data['location_data'].get(location_key)
    if location:
        return location
    location_404 = game_data['location_data']['404']
    return location_404


def get_last_action(user_id):
    last_action = {
        'location_key': '',
        'value': '',
        'next_location_key': '',
        'inventory_items': [],
        'used_item': None,
        'action_at': '',
    }
    user_data_by_id = user_data.get(user_id)
    if user_data_by_id:
        history = user_data_by_id["history"]
        if len(history):
            last_action = history[-1]
    return last_action


def get_next_location_key_by_value(last_location, option_text):
    next_location_key = ""
    options = last_location["options_new"]
    options_keys = list(options)
    for option_key in options_keys:
        if options[option_key]["label"] == option_text:
            next_location_key = option_key
    return next_location_key


def get_history_data_for_image(user_id):
    history_as_string = ""
    origin_image_uuid = None
    user_data_by_id = user_data.get(user_id)
    if user_data_by_id:
        history = user_data_by_id["history"]
        for history_item in history:
            image_uuid = history_item.get('image_uuid')
            if not origin_image_uuid and image_uuid:
                origin_image_uuid = image_uuid

            history_as_string += ' ' + history_item.get('value')

    return {'history_as_string': history_as_string, 'origin_image_uuid': origin_image_uuid}


def get_actions_history(user_id):
    actions_history = {}
    user_data_by_id = user_data.get(user_id)
    if user_data_by_id:
        history = user_data_by_id["history"]
        current_datetime = datetime.datetime.now().timestamp()
        for history_item in history:
            location_key = history_item['location_key']
            action_datetime = datetime.datetime.fromisoformat(history_item['action_at']).timestamp()
            action_at_list = []
            value_list = []
            if actions_history.get(location_key) and actions_history[location_key]['action_at_list']:
                action_at_list = actions_history[location_key]['action_at_list']
                value_list = actions_history[location_key]['value_list']
            action_at_list.append(history_item['action_at'])
            value_list.append(history_item['value'])
            actions_history[location_key] = {
                'action_at_list': action_at_list,
                'value_list': value_list,
                'last_value': history_item['value'],
                'last_action_at': history_item['action_at'],
                'time_passed_in_seconds': current_datetime - action_datetime,
            }

    return actions_history


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
    user_data[user_id]['history'] = []
    user_data[user_id]["user_pet"] = {
        "creating": False,
        "pet": "",
        "thread": "",
    }
    update_user_data()


def save_game_progress(user_id, action):
    location_key = action['location_key']
    value = action['value']
    action_at = action['action_at']
    next_location_key = action['next_location_key']
    if location_key:
        user_data[user_id]['locations_history'].append(location_key)
        user_data[user_id]['history'].append({'location_key': location_key, 'value': value, 'action_at': action_at,
                                              'next_location_key': next_location_key})
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
