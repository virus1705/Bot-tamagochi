import time
import threading

""" пример словаря pictures

    pictures = {
        "glad": "",  # доволен
        "sad": "",  # грустит
        "angry": "",  # сердится
        "joy": ""  # радуется
    }

"""
""" пример создания и работы с питомцем
import time
from pet import create_pet



pictures = {
        "glad": "a",  # доволен
        "sad": "b",  # грустит
        "angry": "c",  # сердится
        "joy": "d"  # радуется
}

cat, thread = create_pet("Phoenix", "cat", pictures)
time.sleep(60)
print(cat.Print_characteristics())
cat.Play()
print(cat.Print_characteristics())
"""

def create_pet(name: str, animal: str, pictures: dict):
    parameters = {
        "name": name,
        "animal": animal,
        "pictures": {
            "glad": pictures["glad"],  # доволен
            "sad": pictures["sad"],  # грустит
            "angry": pictures["angry"],  # сердится
            "joy": pictures["joy"]  # радуется
        }
    }
    pet = PET(parameters)
    thread = threading.Thread(target=pet.Exist).start()
    return pet, thread

class PET:
    def __init__(self, parameters):
        self.name = parameters["name"]
        self.animal = parameters["animal"]
        self.health = 100
        self.food = 100  # сытость
        self.fun = 100  # веселость
        self.vivacity = 100  # бодрость
        self.pictures = parameters["pictures"]
        self.exists = True
        self.Time = 0 # время жизни в минутах
        self.is_sleep = False
        self.sleep_time = 0


    def Hunger(self):
        if self.food > 0:
            self.food -= 1
            if self.food > 50:
                self.fun -= 1
        else:
            self.health -= 1
            self.fun -= 2
            self.vivacity -= 5
        return

    def Food(self):  # покормить
        self.food = min(self.food + 10, 100)
        self.health = min(self.health + 4, 100)
        self.fun = min(self.fun + 5, 100)
        self.vivacity = min(self.vivacity + 5, 100)
        msg = "Ням-ням!"
        return msg, self.pictures["glad"]

    def Sad(self):
        if self.fun >= 80:
            self.fun -= 1
        if self.fun >= 30:
            self.vivacity -= 2
        if self.fun < 30:
            self.health -= 1
            self.vivacity -= 3
        return


    def Play(self):  # поиграть
        self.health = min(self.health + 4, 100)
        self.fun = min(self.fun + 15, 100)
        self.vivacity -= 10
        msg = "Урааа! Играть!"
        return msg, self.pictures["joy"]

    def Sleep(self):
        self.is_sleep = True
        while self.is_sleep and self.sleep_time < 1200:
            time.sleep(1)
            self.sleep_time += 1
        self.vivacity = min(self.vivacity + self.sleep_time//40, 100)  # прибавит max 30
        self.fun = min(self.fun + self.sleep_time//240, 100)  # прибавит max 5
        self.health = min(self.health + self.sleep_time//600, 100)  # прибавит max 2
        self.Hunger()
        self.Sad()
        return
    def wake_up(self):  # разбудить
        self.is_sleep = False
        if self.sleep_time >= 660:  # 11 минут
            msg = "* Зевок *. Хорошо поспал!"
            return msg, self.pictures["glad"]
        else:
            msg = "* Зевок *. Ну ещё хотя бы 5 минут!"
            return msg, self.pictures["angry"]


    def Print_characteristics(self):  # отправить характеристики
        charact = {
            "name": self.name,
            "animal": self.animal,
            "health": f"{self.health} / 100",
            "food": f"{self.food} / 100",
            "fun": f"{self.fun} / 100",
            "vivacity": f"{self.vivacity} / 100",
            "time": f"прожил {self.Time} минут"
        }
        return charact

    def Exist(self):
        while self.exists:
            time.sleep(59.9)
            self.Time += 1
            self.Hunger()
            if self.Time % 5 == 0:
                self.Sad()
            if self.vivacity % 40 == 0:
                self.Sleep()
                self.is_sleep = False
                self.sleep_time = 0
            if self.health == 0:
                self.exists = False
        return





