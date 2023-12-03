class Team:
    def __init__(self, id):
        self.id = id
        self.win = 0
        self.lose = 0
        self.draw = 0

    def get_key(self):
        return f'({self.win},{self.lose},{self.draw})'