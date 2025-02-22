import random

import pygame
from random import randint

import input
import model_objects as mo
import vis
import time
pygame.init()
'''

Параметры игры (ФПС - влияет на скорость игры, начальное кол-во очков (Почти всегда это 0))
'''
FPS = 30
score = 0
number_of_food = 3

'''

Цвета
'''
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

'''

Параметры экрана (Ширина, Высота и масштаб, т.е. кол-во пикселей в одном игровом квадратике)
'''
WIDTH = 41
HEIGHT = 41
SIZE = vis.SIZE

'''

Задаём параметры экрана
'''
screen = pygame.display.set_mode((WIDTH * SIZE, HEIGHT * SIZE))


def StartDisplay(event, size):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if size * mo.HEIGHT / 3 <= event.pos[1] <= 4 * size * mo.HEIGHT / 9:
            if size * 90 * mo.WIDTH / 700 <= event.pos[0] <= size * (9 / 70 + 99 / 500) * mo.WIDTH:
                return 1
            elif size * 290 * mo.WIDTH / 700 <= event.pos[0] <= size * (29 / 70 + 99 / 500) * mo.WIDTH:
                return 2
            elif size * 490 * mo.WIDTH / 700 <= event.pos[0] <= size * (49 / 70 + 99 / 500) * mo.WIDTH:
                return 3
    return 0


def TableButtons(event, size):
    if (event.pos[0] - size * 15 * mo.WIDTH / 70) ** 2 + (event.pos[1] - size * 2 * mo.HEIGHT / 3) ** 2 <= (
            size * mo.HEIGHT / 10) ** 2:
        return 1
    elif (event.pos[0] - size * 35 * mo.WIDTH / 70) ** 2 + (event.pos[1] - size * 2 * mo.HEIGHT / 3) ** 2 <= (
            size * mo.HEIGHT / 10) ** 2:
        return 2
    elif (event.pos[0] - size * 55 * mo.WIDTH / 70) ** 2 + (event.pos[1] - size * 2 * mo.HEIGHT / 3) ** 2 <= (
            size * mo.HEIGHT / 10) ** 2:
        return 3


def ChoiceDisplay(event, size):
    if event.type == pygame.MOUSEBUTTONDOWN:
        if size / 3 * mo.WIDTH <= event.pos[0] <= 2 * size / 3 * mo.WIDTH:
            if size * mo.HEIGHT / 7 <= event.pos[1] <= 2 * size * mo.HEIGHT / 7:
                return 1
            elif 3 * size * mo.HEIGHT / 7 <= event.pos[1] <= 4 * size * mo.HEIGHT / 7:
                return 2
            elif 5 * size * mo.HEIGHT / 7 <= event.pos[1] <= 6 * size * mo.HEIGHT / 7:
                return 3
    return 0


def update(event):
    """
    Проверка на закрытие программы
    :param event: пайгеймовский евент
    :return: True если евент был закрытие программы, иначе False
    """
    if event.type == pygame.QUIT:
        return True
    elif event.type == pygame.KEYUP and event.key == pygame.K_ESCAPE:
        return True
    else:
        return False
    # finished = update(event)


pygame.display.update()
clock = pygame.time.Clock()
screen_number = 1
finished = False
result = 0
pygame.mixer.music.load('music\\fasterdoesit.mp3')
pygame.mixer.music.play(-1)
while not finished and result == 0:
    pygame.display.update()
    for event in pygame.event.get():
        vis.DrawStartDisplay(screen, event, SIZE)
        result = StartDisplay(event, SIZE)
        finished = update(event)

if result == 1:
    walls = input.read_wall_data('levels\\Lvl_1.txt')
elif result == 2:
    walls = input.read_wall_data('levels\\Lvl_2.txt')
elif result == 3:
    walls = input.read_wall_data('levels\\Lvl_3.txt')

result = 0
while not finished and result == 0:
    pygame.display.update()
    for event in pygame.event.get():
        vis.DrawChoiceDisplay(screen, event, SIZE)
        result = ChoiceDisplay(event, SIZE)
        finished = update(event)

if result == 1:
    FPS = 10
    score_for_food = 1
elif result == 2:
    FPS = 20
    score_for_food = 2
elif result == 3:
    FPS = 30
    score_for_food = 3


'''

Считываем файлы с параметрами змейки, стен и змеек - еды
'''
main_snake = input.read_main_snake_data('other\\main_snake.txt')
food = input.read_food_data('other\\food.txt')

'''

Рисуем начальные положения всех объектов

Из всех змеек-еды выбираем одну с помощью рандома
'''
for wall in walls:
    vis.DrawWall(wall.x_begin, wall.y_begin, wall.x_end, wall.y_end, wall.color, screen)

live_food = [0] * number_of_food
for num in range(number_of_food):
    flag = 0
    while flag == 0:
        live_food[num] = randint(0, len(food) - 1)
        x = food[live_food[num]].coordinates[0][0]
        y = food[live_food[num]].coordinates[0][1]
        for wall in walls:
            if not (wall.x_begin <= x <= wall.x_end and wall.y_begin <= y <= wall.y_end):
                flag = 1
        for another_num in range(num):
            if live_food[another_num] == live_food[num]:
                flag = 0

    vis.DrawSnake(food[num].coordinates, food[num].color, food[num].head_color, screen)

vis.DrawSnake(main_snake.coordinates, main_snake.color, main_snake.head_color, screen)
vis.DrawField(screen)

'''

Тут мы начинаем гонять нашу игру, пока змея не врежется в стену или не укусит сама себя
'''
rnd = random.randint(1, 3)
if rnd == 1:
    pygame.mixer.music.load('music\\breaktime.mp3')
    pygame.mixer.music.play(-1)
elif rnd == 2:
    pygame.mixer.music.load('music\\carefree.mp3')
    pygame.mixer.music.play(-1)
elif rnd == 3:
    pygame.mixer.music.load('music\\fretless.mp3')
    pygame.mixer.music.play(-1)


while not finished and main_snake.death == 0:

    clock.tick(FPS)
    '''
    
    Создаём чистый экран
    '''
    pygame.display.update()
    screen.fill(WHITE)

    '''
    
    Работаем со стенами (С каждой отдельно)
    '''
    for wall in walls:
        '''
        
        Рисуем стену
        '''
        vis.DrawWall(wall.x_begin, wall.y_begin, wall.x_end, wall.y_end, wall.color, screen)
        '''
        
        Проверяем, ударилась ли главная змея со стеной
        
        Если да, то главная змея умирает
        '''
        if wall.collision(main_snake.coordinates[0][0], main_snake.coordinates[0][1]):
            main_snake.death = 1

        '''
        
        Проверяем, дошла ли змея - еда до стены
        
        Если да, то она развернётся
        '''
        for num in live_food:
            food[num].turn(wall.x_begin, wall.y_begin, wall.x_end, wall.y_end)

    '''
    
    Рисуем змейку-еду
    '''
    for num in live_food:
        vis.DrawSnake(food[num].coordinates, food[num].color, food[num].head_color, screen)

    '''
    
    Проверяем, скушала ли змея еду
    
    Если да, то создаётся новая еда, а змейка вырастает на одну ячейку
    '''
    for num in range(number_of_food):
        food_number = live_food[num]
        if main_snake.collision(food[food_number].coordinates) == 1:
            l = len(main_snake.coordinates)
            x_end = main_snake.coordinates[l - 1][0]
            y_end = main_snake.coordinates[l - 1][1]
            main_snake.elongation(x_end, y_end)
            score += score_for_food

            flag = 0
            while flag == 0:
                live_food[num] = randint(0, len(food) - 1)
                x = food[live_food[num]].coordinates[0][0]
                y = food[live_food[num]].coordinates[0][1]
                for wall in walls:
                    if not (wall.x_begin <= x <= wall.x_end and wall.y_begin <= y <= wall.y_end):
                        flag = 1
                for another_num in range(num):
                    if live_food[another_num] == live_food[num]:
                        flag = 0

    '''
    
    Проверяем, не укусила ли змея сама себя
    
    Если да, то змея умирает
    '''
    if main_snake.collision(main_snake.coordinates) == 0:
        main_snake.death = 1

    '''
    
    Рисуем змею
    '''
    vis.DrawSnake(main_snake.coordinates, main_snake.color, main_snake.head_color, screen)

    '''
    
    Проверяем нажатые клавиши
    
    Если нажата клавиша w, a, s или d, то змея поворачивается в нужном направлении
    '''
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            main_snake.veer()
        finished = update(event)

    '''
    
    Двигаем змею
    
    Сначала хвост, потом голову
    '''
    main_snake.move_tail()
    main_snake.move_head(main_snake.direction)

    '''
    
    Змея - еда двигается в зависимости от своей скорости
    
    Еда двигается на клетку каждый 2 ход (food[food_number].miss + 1)
    '''
    for num in live_food:
        food[num].move_miss = (food[num].move_miss + 1) % (food[num].miss + 1)
        if food[num].move_miss == food[num].miss:
            food[num].move_tail()
            food[num].move_head(food[num].direction)

'''

Игра закончилась, подготавливаемся к экрану конца игры

name - это имя, которое введёт пользователь

right_pressed - флаг, который сработает, когда нажмётся стрелочка вправо
'''
finished = False
right_pressed = False
name = ''

'''

Экран ввода имени

Работает, пока не нажата стрелочка вправо
'''
pygame.mixer.music.load('music\\fivecardshuffle.mp3')
pygame.mixer.music.play(-1)
while not finished and not right_pressed:

    '''
    
    Рисуем экран, на котором пишется всякая всячина
    '''
    pygame.display.update()
    screen.fill(WHITE)
    vis.EndGameDisplay(screen, score, name, SIZE)

    '''
    
    Проверяем, нажата ли какая-либо клавиша
    
    Если нажата, то заставляем функцию Alphabet возвращает эту кнопку
    
    При нажатом BACKSPACE стирается последний символ
    
    При нажатии правой стрелочки ввод заканчивается 
    '''
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            letter = vis.Alphabet()
            if letter == 'BACKSPACE':
                name = name[:-1]
            elif letter == 'RIGHT':
                right_pressed = True
            else:
                name += letter
        finished = update(event)

'''

Здесь читается, анализируется, переписывается и записывается обратно в файл таблица лидеров
'''
table = input.top_entry(score, name)

'''

Здесь игрок модет полубоваться таблицей лидеров

Закрыть окно можно, нажав любую кнопку
'''
bottom_pressed = False
while not finished and not bottom_pressed:
    pygame.display.update()
    screen.fill(WHITE)
    vis.DrawTable(screen, table, table[20], SIZE)
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            bottom_pressed = True
        finished = update(event)

pygame.quit()
