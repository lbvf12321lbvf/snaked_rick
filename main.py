import pygame
from random import randint

from input import *
from model_objects import *
from vis import *
import time

FPS = 10
score = 0

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

WIDTH = 41
HEIGHT = 41
SIZE = 20


def veer(event):
    pressed = pygame.key.get_pressed()
    if pressed[pygame.K_w]:
        if abs(main_snake.coordinates[0][1] - main_snake.coordinates[1][1]) != 1:
            main_snake.direction = 'w'

    if pressed[pygame.K_s]:
        if abs(main_snake.coordinates[0][1] - main_snake.coordinates[1][1]) != 1:
            main_snake.direction = 's'

    if pressed[pygame.K_a]:
        if abs(main_snake.coordinates[0][0] - main_snake.coordinates[1][0]) != 1:
            main_snake.direction = 'a'

    if pressed[pygame.K_d]:
        if abs(main_snake.coordinates[0][0] - main_snake.coordinates[1][0]) != 1:
            main_snake.direction = 'd'


screen = pygame.display.set_mode((WIDTH * SIZE, HEIGHT * SIZE))

pygame.display.update()
clock = pygame.time.Clock()
finished = False

main_snake = read_main_snake_data_from_file('main_snake.txt')
walls = read_wall_data_from_file('walls.txt')
food = read_food_data_from_file('food.txt')

for wall in walls:
    DrawWall(wall.x_begin, wall.y_begin, wall.x_end, wall.y_end, wall.color, screen)

food_number = randint(0, len(food) - 1)
DrawSnake(food[food_number].coordinates, food[food_number].color, food[food_number].head_color, screen)

DrawSnake(main_snake.coordinates, main_snake.color, main_snake.head_color, screen)
DrawField(screen)

while not finished and main_snake.death == 0:
    clock.tick(FPS)
    pygame.display.update()
    screen.fill(WHITE)

    for wall in walls:
        DrawWall(wall.x_begin, wall.y_begin, wall.x_end, wall.y_end, wall.color, screen)
        if wall.collision(main_snake.coordinates[0][0], main_snake.coordinates[0][1]):
            main_snake.death = 1

        food[food_number].turn(wall.x_begin, wall.y_begin, wall.x_end, wall.y_end)


    DrawSnake(food[food_number].coordinates, food[food_number].color, food[food_number].head_color, screen)

    if main_snake.collision(food[food_number].coordinates) == 1:
        l = len(main_snake.coordinates)
        x_end = main_snake.coordinates[l - 1][0]
        y_end = main_snake.coordinates[l - 1][0]
        main_snake.elongation(x_end, y_end)
        score += 1
        food_number = randint(0, len(food) - 1)

    if main_snake.collision(main_snake.coordinates) == 0:
        main_snake.death = 1


    DrawSnake(main_snake.coordinates, main_snake.color, main_snake.head_color, screen)

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            veer(event)

    main_snake.move_tail()
    main_snake.move_head(main_snake.direction)
    food[food_number].move_miss = (food[food_number].move_miss + 1) % (food[food_number].miss + 1)
    if food[food_number].move_miss == food[food_number].miss:
        food[food_number].move_tail()
        food[food_number].move_head(food[food_number].direction)

finished = False
right_pressed = False
name = ''

while not finished and not right_pressed:
    pygame.display.update()
    screen.fill(WHITE)
    End_game_display(screen, score, name)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            letter = Alphabet(event)
            if letter == 'BACKSPACE':
                name = name[:-1]
            elif letter == 'RIGHT':
                right_pressed = True
            else:
                name += letter

table = top_entry(score, name)

bottom_pressed = False
while not finished and not bottom_pressed:
    pygame.display.update()
    screen.fill(WHITE)
    Draw_table(screen, table, table[20])
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            bottom_pressed = True

pygame.quit()