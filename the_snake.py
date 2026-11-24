"""Реализация учебной игры «Змейка» на Pygame."""

from random import choice

import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(self):
        """Инициализировать позицию и цвет объекта."""
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = None

    def draw(self):
        """Определить базовый способ отрисовки без рисующих действий."""


class Apple(GameObject):
    """Класс яблока, которое можно перемещать по игровому полю."""

    def __init__(self, snake=None):
        """Создать яблоко в случайной свободной клетке поля."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position(snake)

    def randomize_position(self, snake=None):
        """Выбрать свободную клетку, не занятую телом змейки."""
        occupied = set(snake.positions) if snake is not None else set()
        free_positions = [
            (x * GRID_SIZE, y * GRID_SIZE)
            for x in range(GRID_WIDTH)
            for y in range(GRID_HEIGHT)
            if (x * GRID_SIZE, y * GRID_SIZE) not in occupied
        ]
        if free_positions:
            self.position = choice(free_positions)

    def draw(self):
        """Отрисовать яблоко с границей клетки."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс змейки, которая движется по сетке игрового поля."""

    def __init__(self):
        """Создать змейку из одного сегмента в центре поля."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Вернуть координаты головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Применить направление, выбранное обработчиком клавиш."""
        if not self.next_direction:
            return
        new_direction = self.next_direction
        is_reverse = (
            new_direction[0] == -self.direction[0]
            and new_direction[1] == -self.direction[1]
        )
        if not is_reverse:
            self.direction = new_direction
        self.next_direction = None

    def move(self):
        """Переместить змейку с проходом через границы поля."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.positions.insert(0, new_head)
        self.position = new_head
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def draw(self):
        """Отрисовать змейку и стереть удалённый хвост."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(
            self.get_head_position(), (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            self.last = None

    def reset(self):
        """Вернуть змейку в начальное состояние."""
        self.length = 1
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None


def handle_keys(game_object):
    """Обработать события выхода и управления стрелками."""
    directions = {
        pygame.K_UP: UP,
        pygame.K_DOWN: DOWN,
        pygame.K_LEFT: LEFT,
        pygame.K_RIGHT: RIGHT,
    }
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        if event.type != pygame.KEYDOWN:
            continue
        new_direction = directions.get(event.key)
        if new_direction is None:
            continue
        is_reverse = (
            new_direction[0] == -game_object.direction[0]
            and new_direction[1] == -game_object.direction[1]
        )
        if not is_reverse:
            game_object.next_direction = new_direction


def main():
    """Запустить игровой цикл змейки."""
    pygame.init()
    snake = Snake()
    apple = Apple(snake=snake)

    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake)

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            apple.randomize_position(snake)

        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw()
        snake.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
