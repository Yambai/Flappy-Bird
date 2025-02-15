# pipe.py
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, PIPE_WIDTH, PIPE_GAP, PIPE_SPEED
import random


class Pipe:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = WINDOW_WIDTH
        # Случайное положение зазора для прохождения птицей
        self.gap_y = random.randint(PIPE_GAP, WINDOW_HEIGHT - PIPE_GAP)
        self.scored = False  # Флаг, что данная труба уже учтена в счёте
        # Создаём верхнюю трубу
        self.upper_pipe_id = canvas.create_rectangle(
            self.x, 0,
            self.x + PIPE_WIDTH, self.gap_y - PIPE_GAP / 2,
            fill="green"
        )
        # Создаём нижнюю трубу
        self.lower_pipe_id = canvas.create_rectangle(
            self.x, self.gap_y + PIPE_GAP / 2,
                    self.x + PIPE_WIDTH, WINDOW_HEIGHT,
            fill="green"
        )

    def update(self):
        self.x -= PIPE_SPEED
        self.canvas.coords(
            self.upper_pipe_id,
            self.x, 0,
            self.x + PIPE_WIDTH, self.gap_y - PIPE_GAP / 2
        )
        self.canvas.coords(
            self.lower_pipe_id,
            self.x, self.gap_y + PIPE_GAP / 2,
                    self.x + PIPE_WIDTH, WINDOW_HEIGHT
        )

    def off_screen(self):
        return self.x + PIPE_WIDTH < 0
