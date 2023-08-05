from datetime import date


class User:
    def __init__(self, full_name: str, email: str, phone_number: str, birthdate: date):
        self._full_name = full_name
        self._email = email
        self._phone = phone_number
        self.birthday = birthdate

