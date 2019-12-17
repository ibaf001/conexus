import json


def load_db():
    with open("flashcards_db.json") as f:
        return json.load(f)


db = load_db()


class Employee:
    def __init__(self, id, code, name):
        self.id = id
        self.name = name
        self.code = code
