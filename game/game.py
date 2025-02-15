# game.py
import tkinter as tk
import time
from bird import Bird
from pipe import Pipe
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, PIPE_INTERVAL, PIPE_WIDTH


class Game:
    def __init__(self, root):
        self.root = root
        self.root.title("Flappy Bird")
        self.canvas = tk.Canvas(root, width=WINDOW_WIDTH, height=WINDOW_HEIGHT, bg="skyblue")
        self.canvas.pack()

        # Инициализируем текущий счёт и его отображение на холсте
        self.score = 0
        self.score_text = self.canvas.create_text(10, 10, anchor="nw",
                                                  text=f"Score: {self.score}",
                                                  font=("Arial", 16), fill="black")
        # Загружаем лучший счёт из файла
        self.best_score = self.load_best_score()

        self.bird = Bird(self.canvas)
        self.pipes = []
        self.last_pipe_time = time.time() * 1000

        self.game_over = False

        # Обработка нажатий клавиши пробел и кликов мышью
        self.root.bind("<space>", self.handle_input)
        self.root.bind("<Button-1>", self.handle_input)

        self.update()

    def load_best_score(self):
        try:
            with open("score.txt", "r") as f:
                return int(f.read())
        except FileNotFoundError:
            return 0

    def save_best_score(self):
        with open("score.txt", "w") as f:
            f.write(str(self.best_score))

    def handle_input(self, event):
        if not self.game_over:
            self.bird.jump()
        else:
            self.restart()

    def update(self):
        if self.game_over:
            return

        self.bird.update()

        now = time.time() * 1000  # текущее время в мс
        if now - self.last_pipe_time > PIPE_INTERVAL:
            self.pipes.append(Pipe(self.canvas))
            self.last_pipe_time = now

        # Обновляем трубы и проверяем, прошла ли птица мимо трубы
        for pipe in self.pipes:
            pipe.update()
            # Если правая сторона трубы прошла левую сторону птицы и счёт ещё не увеличен
            if not pipe.scored and pipe.x + PIPE_WIDTH < self.bird.x:
                self.score += 1
                pipe.scored = True
                self.canvas.itemconfig(self.score_text, text=f"Score: {self.score}")

        # Удаляем трубы, вышедшие за экран
        self.pipes = [pipe for pipe in self.pipes if not pipe.off_screen()]

        if self.check_collisions():
            self.end_game()
            return

        self.root.after(20, self.update)

    def check_collisions(self):
        # Получаем ограничивающий прямоугольник птицы
        bird_bbox = self.bird.get_bbox()
        # Если птица выходит за верх или низ экрана
        if bird_bbox[1] < 0 or bird_bbox[3] > WINDOW_HEIGHT:
            return True

        # Проверяем столкновения с трубами
        for pipe in self.pipes:
            upper_coords = self.canvas.coords(pipe.upper_pipe_id)
            lower_coords = self.canvas.coords(pipe.lower_pipe_id)
            if self.rect_overlap(bird_bbox, upper_coords) or self.rect_overlap(bird_bbox, lower_coords):
                return True
        return False

    def rect_overlap(self, rect1, rect2):
        # rect представляется списком [x1, y1, x2, y2]
        return not (rect1[2] < rect2[0] or rect1[0] > rect2[2] or
                    rect1[3] < rect2[1] or rect1[1] > rect2[3])

    def end_game(self):
        self.game_over = True

        if self.score > self.best_score:
            self.best_score = self.score
            self.save_best_score()

        self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 - 40,
                                text=f"Game Over! Score: {self.score}",
                                font=("Arial", 24), fill="red")
        self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2,
                                text=f"Best: {self.best_score}",
                                font=("Arial", 18), fill="red")
        self.canvas.create_text(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2 + 40,
                                text="Нажмите пробел или клик для рестарта",
                                font=("Arial", 16), fill="red")

    def restart(self):
        self.canvas.delete("all")
        self.score = 0
        self.score_text = self.canvas.create_text(10, 10, anchor="nw",
                                                  text=f"Score: {self.score}",
                                                  font=("Arial", 16), fill="black")
        self.bird = Bird(self.canvas)
        self.pipes = []
        self.last_pipe_time = time.time() * 1000
        self.game_over = False
        self.update()
