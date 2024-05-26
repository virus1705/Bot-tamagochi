from data_manager import user_data, get_actions_history
from kandinsky import get_images


def create_image(user_id, filename, color, animal, pet_name, action, origin=False):
    if origin:
        origin = f"http://localhost:8000/{user_id}/orig.jpg"  # потом заменить на нелокальный
    else:
        origin = None

    get_images(user=user_id, filename=filename,
               prompt=f"{color} {animal}  по имени {pet_name}, миловидный, в портретном стиле на фоне травы и неба."
                      f" Животное на картинке {action}. Фон должен быть немного размытым, "
                      f"а животное чётко изображено.",
               style="Детальное фото", origin=origin)


def generate_images(user_id, animal, pet_name, color=''):
    create_image(user_id, "orig", color, animal, pet_name, "смотрит в твою сторону")
    create_image(user_id, "glad", color, animal, pet_name, "выглядит довольным", True)
    create_image(user_id, "sad", color, animal, pet_name, "выглядит грустным", True)
    create_image(user_id, "angry", color, animal, pet_name, "выглядит сердитым", True)
    create_image(user_id, "joy", color, animal, pet_name, "выглядит радостным", True)

    pictures = {
        "orig": open(f"user_media/{user_id}/orig.jpg", "rb").read(),
        "glad": open(f"user_media/{user_id}/glad.jpg", "rb").read(),  # доволен
        "sad": open(f"user_media/{user_id}/sad.jpg", "rb").read(),  # грустит
        "angry": open(f"user_media/{user_id}/angry.jpg", "rb").read(),  # сердится
        "joy": open(f"user_media/{user_id}/joy.jpg", "rb").read()  # радуется
    }

    return pictures
