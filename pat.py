import time

""" пример словаря parameters
parameters = {
    "name": "",
    "animal": "",
    "pictures": {
        "glad": "",  # доволен
        "sad": "",  # грустит
        "angry": "",  # сердится
        "joy": ""  # радуется
    }
}
"""

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
        self.Exist()

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

    def Food(self):
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

    def Play(self):
        self.health = min(self.health + 4, 100)
        self.fun = min(self.fun + 15, 100)
        self.vivacity -= 10
        msg = "Урааа! Играть!"
        return msg, self.pictures["joy"]

    def Sleep(self):
        time.sleep(1200)
        self.vivacity = min(self.vivacity + 30, 100)
        self.fun = min(self.fun + 5, 100)
        self.health = min(self.health + 2, 100)
        return self.Hunger(), self.Sad()

    def Exist(self):
        while self.exists:
            time.sleep(60)
            self.Time += 1
            self.Hunger()
            if self.Time % 5 == 0:
                self.Sad()
            if self.vivacity % 20 == 0:
                self.Sleep()
            if self.health == 0:
                self.exists = False





