# puzzle_generator.py
import random
import numpy as np

DIRECTIONS = [
    (0, 1),  # right
    (1, 0),  # down
    (1, 1),  # diagonal down-right
    (-1, 1), # diagonal up-right
]

class WordSearch:
    def __init__(self, size=15, words=None):
        self.size = size
        self.grid = np.full((size, size), fill_value='.', dtype=str)
        self.words = words or []
        self.placed_words = []

    def can_place_word(self, word, row, col, direction):
        dr, dc = direction
        for i in range(len(word)):
            r = row + dr * i
            c = col + dc * i
            if r < 0 or r >= self.size or c < 0 or c >= self.size:
                return False
            if self.grid[r, c] != '.' and self.grid[r, c] != word[i]:
                return False
        return True

    def place_word(self, word):
        attempts = 100
        while attempts > 0:
            direction = random.choice(DIRECTIONS)
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            if self.can_place_word(word, row, col, direction):
                dr, dc = direction
                for i in range(len(word)):
                    self.grid[row + dr * i, col + dc * i] = word[i]
                self.placed_words.append(word)
                return True
            attempts -= 1
        return False

    def fill_empty(self):
        letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r, c] == '.':
                    self.grid[r, c] = random.choice(letters)

    def generate(self):
        self.grid = np.full((self.size, self.size), fill_value='.', dtype=str)
        self.placed_words.clear()
        for word in self.words:
            self.place_word(word.upper())
        self.fill_empty()
        return self.grid, self.placed_words

    def grid_to_str(self):
        return '\n'.join(' '.join(row) for row in self.grid)
