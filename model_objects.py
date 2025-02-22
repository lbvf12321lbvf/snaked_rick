import pygame
# Цвета
RED = 0xFF0000
BLUE = 0x0000FF
YELLOW = 0xFFC91F
GREEN = 0x00FF00
MAGENTA = 0xFF03B8
CYAN = 0x00FFCC
BLACK = (0, 0, 0)
WHITE = 0xFFFFFF
GREY = 0x7D7D7D
AQUAMARINE = (127, 255, 212)
YELLOW_GREEN = (154, 205, 50)
ORANGE = (217, 232, 12)

WIDTH = 41
HEIGHT = 41


class Wall:
    def __init__(self, x_begin, y_begin, x_end, y_end):
        """
        Инициализация стен в виде прямоугольника, которые ограничивают пространство для движения змейки
        """
        self.x_begin = x_begin
        self.y_begin = y_begin
        self.x_end = x_end
        self.y_end = y_end
        self.color = BLACK

    def collision(self, x_snake, y_snake):
        """
        :param x_snake: абсцисса головы змейки
        :param y_snake: ордината головы змейки
        :return: true или false в зависимости от того, столкнулась или нет змея со стеной.
        """
        if self.x_begin <= x_snake <= self.x_end or self.x_end <= x_snake <= self.x_begin:
            if self.y_begin <= y_snake <= self.y_end or self.y_end <= y_snake <= self.y_begin:
                return True
        return False


class Snakes:
    def __init__(self, coordinates, direction):
        """
        :param coordinates: координаты всех квадратиков змейки, начиная с головы
        :param direction: направление движения змейки в данный момент, характеризуется одной
        из букв 'w', 'a', 's', 'd'
        """
        self.coordinates = coordinates
        self.direction = direction
        self.live = True

    def collision(self, coordinates):
        """
        :param coordinates - массив координат квадратиков другой змейки
        :return: 0 - дополнительная змейка врезалась в данную, 1 - наоборот, 2 - ничего не произошло
        """
        for i in range(1, len(self.coordinates)):
            x = self.coordinates[i][0]
            y = self.coordinates[i][1]
            if x == coordinates[0][0] and y == coordinates[0][1]:
                return 0
        for i in range(1, len(coordinates)):
            x = coordinates[i][0]
            y = coordinates[i][1]
            if x == self.coordinates[0][0] and y == self.coordinates[0][1]:
                return 1
        return 2

    def move_tail(self):
        end = [self.coordinates[-1][0], self.coordinates[-1][1]]
        length = len(self.coordinates)
        for number in range(1, length, 1):
            self.coordinates[length - number][0] = self.coordinates[length - number - 1][0]
            self.coordinates[length - number][1] = self.coordinates[length - number - 1][1]
        return end

    def move_head(self, new_direction):
        """
        Функция отвечает за движение головы змейки - поворот и продвижение
        :param new_direction: новое направление движения
        """
        if (self.direction == 'w' or self.direction == 's') and (new_direction == 'a' or new_direction == 'd'):
            self.direction = new_direction
        elif (self.direction == 'a' or self.direction == 'd') and (new_direction == 'w' or new_direction == 's'):
            self.direction = new_direction

        if self.coordinates[0][0] > WIDTH:
            self.coordinates[0][0] = 0
        if self.coordinates[0][0] < 0:
            self.coordinates[0][0] = WIDTH - 1
        if self.coordinates[0][1] > HEIGHT:
            self.coordinates[0][1] = 0
        if self.coordinates[0][1] < 0:
            self.coordinates[0][1] = HEIGHT - 1

        if self.direction == 'd':
            self.coordinates[0][0] += 1
        elif self.direction == 'a':
            self.coordinates[0][0] -= 1
        elif self.direction == 'w':
            self.coordinates[0][1] -= 1
        else:
            self.coordinates[0][1] += 1


class MainSnake(Snakes):
    def __init__(self, coordinates, direction):
        Snakes.__init__(self, coordinates, direction)
        self.color = BLUE
        self.head_color = AQUAMARINE
        self.death = 0

    def elongation(self, x_end, y_end):
        self.coordinates.append([x_end, y_end])

    def veer(self):
        '''

        Функция поворачивает голову змеи, в зависимости от нажатой клавиши.

        Змея не повернёт в противоположную сторону.

        На вход функция получает ивент

        В результате функция отдаёт новое значение ориентации головы змеи
        '''
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            if abs(self.coordinates[0][1] - self.coordinates[1][1]) != 1:
                self.direction = 'w'

        if pressed[pygame.K_s]:
            if abs(self.coordinates[0][1] - self.coordinates[1][1]) != 1:
                self.direction = 's'

        if pressed[pygame.K_a]:
            if abs(self.coordinates[0][0] - self.coordinates[1][0]) != 1:
                self.direction = 'a'

        if pressed[pygame.K_d]:
            if abs(self.coordinates[0][0] - self.coordinates[1][0]) != 1:
                self.direction = 'd'


class Food(Snakes):
    def __init__(self, coordinates, direction):
        Snakes.__init__(self, coordinates, direction)
        self.color = GREEN
        self.head_color = YELLOW_GREEN
        self.actions = []  # Массив действий змейки-еды
        self.miss = 1
        self.move_miss = 0

    def eating(self, coordinates):
        """
        :param coordinates: координаты "побочной змейки"
        :return: вывод прибавки к счёту по итогу обработки
        """
        if self.collision(coordinates) == 0:
            self.live = False
            return True
        return False

    def death(self, coordinates):
        if self.collision(coordinates) == 1:
            self.live = False

    def turn(self, x_begin, y_begin, x_end, y_end):
        dir = self.direction
        if dir == 'w':
            x = self.coordinates[0][0]
            y = self.coordinates[0][1] - 1
        elif dir == 's':
            x = self.coordinates[0][0]
            y = self.coordinates[0][1] + 1
        elif dir == 'a':
            x = self.coordinates[0][0] - 1
            y = self.coordinates[0][1]
        else:
            x = self.coordinates[0][0] + 1
            y = self.coordinates[0][1]

        if x_begin <= x <= x_end and y_begin <= y <= y_end:
            if dir == 'w':
                dir = 's'
            elif dir == 's':
                dir = 'w'
            elif dir == 'a':
                dir = 'd'
            else:
                dir = 'a'

        self.direction = dir


class Enemy(Snakes):
    def __init__(self, coordinates, direction):
        Snakes.__init__(self, coordinates, direction)
        self.color = MAGENTA
