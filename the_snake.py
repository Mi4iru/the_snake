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
    """Абстрактный класс игрового объекта содержит поля: position
    и body_color. Предполагается, что класс не будет использоваться напрямую,
    а будет наследоваться для написания собственных игровых объектов.
    """

    def __init__(self):
        self.position = (GRID_WIDTH // 2 * GRID_SIZE,
                         GRID_HEIGHT // 2 * GRID_SIZE)
        self.body_color = None

    def draw(self):
        """Абстрактный метод draw предназначен для отрсиовки объекта."""
        pass


class Apple(GameObject):
    """
    Класс описывающий поведение игрового объекта Яблоко.
    Цвет задан по умолчанию, позиция определяется случайным
    образом.
    """

    def __init__(self):
        self.body_color = (255, 0, 0)
        self.randomize_position()

    def randomize_position(self):
        """Метод перемещает яблоко в новую случайную позицию."""
        self.position = (choice(range(GRID_WIDTH)) * GRID_SIZE,
                         choice(range(GRID_HEIGHT)) * GRID_SIZE)

    def draw(self):
        """Метод рисует яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс описывающий игровой объект змея."""

    def __init__(self):
        super().__init__()
        self.reset()
        self.direction = RIGHT
        self.body_color = (0, 255, 0)
        self.last = None

    def update_direction(self):
        """Метод обновляет направление движения змеи."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def get_head_position(self):
        """Метод возвращают позицию головы змеи в пикселях."""
        return self.positions[0]

    def draw(self):
        """Метод отрисоывавает объект на игровом поле."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """
        Метод используется для перезапуска игры. Параметры объекта
        возвращаются в исходное при создании положение.
        """
        self.length = 1
        self.position = (GRID_WIDTH // 2 * GRID_SIZE,
                         GRID_HEIGHT // 2 * GRID_SIZE)
        self.positions = [self.position]
        self.direction = choice((RIGHT, LEFT, UP, DOWN))
        self.next_direction = None

    def move(self):
        """
        Метод обрабатывает перемещение змейки, вычисляя новое положение
        её частей.
        """
        head = self.get_head_position()
        head = ((head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
                (head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT)
        if head in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, head)
        if len(self.positions) > self.length + 1:
            self.positions.pop()


# Функция обработки действий пользователя
def handle_keys(game_object):
    """
    Функция обрабатывает события нажатия стрелочек. На вход принимает
    объект класса, содержащий поле 'next_direction'
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция обрабатывающая игру."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    apple = Apple()
    snake = Snake()
    apple.draw()
    snake.draw()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        head = snake.get_head_position()
        if head[0] == apple.position[0] and head[1] == apple.position[1]:
            snake.length += 1
            apple.randomize_position()
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
