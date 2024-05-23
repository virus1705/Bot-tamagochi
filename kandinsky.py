import json
import time
import requests
import os
import base64

secret_key = "8BFF3C36AEADCBA85D94ADBE92252A9E"
api_key = "EEF60CE05FAD276CC374C8059FDD00CF"

class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, style, images=1, width=512, height=512):
        styles = {
            "Детальное фото": "UHD",
            "Аниме": "ANIME",
            "Свой стиль": "DEFAULT"
        }
        params = {
            "type": "GENERATE",
            "style": styles[style],
            "width": width,
            "height": height,
            "num_images": images,
            "negativePromptUnclip": "кислотность, высокая контрастность",
            "generateParams": {
                "query": prompt
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        print(data)
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)


def get_images(user, filename, prompt, style="Детальное фото", origin=None):
    api = Text2ImageAPI('https://api-key.fusionbrain.ai/', f'{api_key}', f'{secret_key}')
    model_id = api.get_model()
    if origin != None:
        prompt += f"Cделать животное также, как здесь: {str(origin)}"
    uuid = api.generate(prompt, model_id, style)
    images = api.check_generation(uuid)

    image_base64 = images[0]
    image_data = base64.b64decode(image_base64)
    try:
        with open(f"users_media/{user}/{filename}.jpg", "wb") as file:
            file.write(image_data)
    except:
        os.mkdir(f"users_media/{user}", mode=0o777, dir_fd=None)
        with open(f"users_media/{user}/{filename}.jpg", "wb") as file:
            file.write(image_data)
    return


#orig = get_images(user="aab", filename="cat", prompt=f"{"рыжий"} {"кот"}, миловидный, пушистый, в портретном стиле на фоне травы и неба. Животное на картинке {"смотрит в твою сторону"}. Фон должен быть немного размытым, а животное чётко изображено.", style="Детальное фото")
#angry = get_images(user="aab", filename="cat1", prompt=f"{"рыжий"} {"кот"}, миловидный, пушистый, в портретном стиле на фоне травы и неба. Животное на картинке {"злится"}. Фон должен быть немного размытым, а животное чётко изображено. ", style="Детальное фото", origin="jetbrains://pycharm/navigate/reference?project=bot_tamagochi&path=users_media/aab/cat.jpg")
