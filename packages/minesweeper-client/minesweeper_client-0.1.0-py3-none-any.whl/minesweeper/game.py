import os


class Game:
    api_base = os.getenv("MINES_API", "https://minesweeper.makecodes.dev")

    def __init__(self):
        print("API TEST BASE", self.api_base)
