# bird.py
from tkinter import PhotoImage
from constants import WINDOW_WIDTH, WINDOW_HEIGHT, GRAVITY, JUMP_STRENGTH, BIRD_SIZE


class Bird:
    def __init__(self, canvas):
        self.canvas = canvas
        self.x = WINDOW_WIDTH // 3
        self.y = WINDOW_HEIGHT // 2
        self.velocity = 0

        # Загружаем оригинальное изображение птицы
        orig_image = PhotoImage(file="bird.png")
        w, h = orig_image.width(), orig_image.height()

        # Определяем, насколько надо уменьшить изображение
        scale_factor = max(w, h) // (BIRD_SIZE * 2)

        if scale_factor > 1:
            self.image = orig_image.subsample(scale_factor, scale_factor)
        else:
            self.image = orig_image  # Если изображение уже маленькое, оставляем как есть

        # Рисуем изображение на холсте
        self.id = canvas.create_image(self.x, self.y, image=self.image)

    def update(self):
        self.velocity += GRAVITY
        self.y += self.velocity
        self.canvas.coords(self.id, self.x, self.y)

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def get_bbox(self):
        """Возвращает ограничивающий прямоугольник птицы в формате [x1, y1, x2, y2]."""
        width = self.image.width()
        height = self.image.height()
        return [self.x - width // 2, self.y - height // 2,
                self.x + width // 2, self.y + height // 2]
