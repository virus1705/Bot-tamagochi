texts = {
    "welcome": "Здравствуй!\nЭтот бот - твой личный Тамагочи\nСоздай своего питомца, чтобы любить и заботиться о нем 🤍"
}


def get_go_message(title: str, command: str | None = ""):
    return f'Сыграем в {title}? {command}'