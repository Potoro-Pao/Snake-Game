import random
import time

import pygame
from pygame import Vector2
from pygame.locals import *

pygame.init()

# ---Game Setting---------------
pygame.display.set_caption("Snake Game")
WIN_WIDTH = 500
WIN_HEIGHT = 700
win = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
game_over = False
bg = pygame.Surface(win.get_size())
bg = bg.convert()
bg.fill((0, 0, 0))
clock = pygame.time.Clock()
FPS = 10
SCORE = 0
UP_EYE = True
LEFT_EYE = False
RIGHT_EYE = False
BOTTOM_EYE = False


# --------Function Section---------------------
# to make the snake come appear at another side if they hit wall
def wrap_position(position, screen):
    x, y = position
    w, h = screen.get_size()
    return Vector2(x % w, y % h)


def display_score(score):
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    text = font.render(f"Score: {str(score)}", 1, (255, 255, 255))
    win.blit(text, (0, 0))


def display_game_over():
    pygame.font.init()
    font = pygame.font.SysFont('comicsans', 60)
    text = font.render('Game Over!', 1, (255, 255, 255))
    win.blit(text, ((win.get_width() // 2 - text.get_width() // 2), (win.get_height() // 2 - text.get_height())))


# ---Game Class------
class Snake:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.position = Vector2((self.x, self.y))
        self.velocity = Vector2(0, 0)
        self.color = color
        self.body = [self.position]  # start with just the head

    def movement(self):
        if event.type == pygame.KEYDOWN:
            if event.key == K_LEFT:
                self.velocity = Vector2(-10, 0)
            elif event.key == K_RIGHT:
                self.velocity = Vector2(10, 0)
            elif event.key == K_UP:
                self.velocity = Vector2(0, -10)
            elif event.key == K_DOWN:
                self.velocity = Vector2(0, 10)
        self.position += self.velocity

    def update(self):
        self.position = wrap_position(self.position, win)

        # this will take the remainder of pos x / width of window
        # pos y / height of window thus it will appear automatically
        # on the other side if the position > win(width/height)

        win.fill((0, 0, 0))

        # once the snake move, the head will immediately put at the next position, and removed(popped)
        for pos in self.body:
            pygame.draw.rect(win, self.color, (pos[0], pos[1], 30, 30))
        self.body.insert(0, self.position)

        if len(self.body) > 1:
            self.body.pop()
        # prevent the head has the same pos as the body
        # and increasing length

    def touch_body(self):
        global game_over
        # self.position.distance_to(snake_pos)
        head_pos = self.body[0]
        for body_pos in self.body[2:]:
            if head_pos == body_pos:
                display_game_over()
                pygame.display.update()
                time.sleep(3)
                game_over = True


class Food:
    def __init__(self, position, color):
        self.position = Vector2(position)
        self.color = color

    def update(self):
        pygame.draw.rect(win, self.color, (self.position[0], self.position[1], 20, 20))

    def eatten(self, snake_pos):
        global SCORE
        # if food get eaten, the food will respawn at different position
        if self.position.distance_to(snake_pos) <= 25:
            self.position[0] = random.randint(0, win.get_width() - 20)
            self.position[1] = random.randint(0, win.get_height() - 20)
            self.position = Vector2((self.position[0], self.position[1]))
            # if snake eat the food, then the snake body will append the position to increase the body length
            snake.body.append(snake.body[-1])
            SCORE += 1


# ------Initialize Snake and Food------------
snake = Snake(0, 500, (123, 123, 123))

food = Food((400, 400), (255, 0, 0))

# ----Main Game Loop--------------------------

while not game_over:
    bg = bg.convert()
    dt = clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
    snake.movement()
    snake.update()
    snake.touch_body()
    food.update()
    food.eatten(snake.position)
    if event.type == pygame.KEYDOWN:
        if event.key == K_LEFT:
            UP_EYE = False
            LEFT_EYE = True
            RIGHT_EYE = False
            BOTTOM_EYE = False
        if event.key == K_UP:
            UP_EYE = True
            LEFT_EYE = False
            RIGHT_EYE = False
            BOTTOM_EYE = False
        if event.key == K_RIGHT:
            UP_EYE = False
            LEFT_EYE = False
            RIGHT_EYE = True
            BOTTOM_EYE = False
        if event.key == K_DOWN:
            UP_EYE = False
            LEFT_EYE = False
            RIGHT_EYE = False
            BOTTOM_EYE = True

    if (UP_EYE):
        pygame.draw.rect(win, (0, 0, 0), (snake.position[0] + 5, snake.position[1], 5, 10))
        pygame.draw.rect(win, (0, 0, 0), (snake.position[0] + 20, snake.position[1], 5, 10))
    elif (LEFT_EYE):
        pygame.draw.rect(win, (0, 0, 0), (snake.position[0], snake.position[1] + 5, 10, 5))
        pygame.draw.rect(win, (0, 0, 0), (snake.position[0], snake.position[1] + 20, 10, 5))
    elif (RIGHT_EYE):
        pygame.draw.rect(win, (0, 0, 0), (snake.position[0] + 20, snake.position[1] + 5, 10, 5))
        pygame.draw.rect(win, (0, 0, 0), (snake.position[0] + 20, snake.position[1] + 20, 10, 5))
    elif (BOTTOM_EYE):
        pygame.draw.rect(win, (0, 0, 0), (snake.position[0] + 5, snake.position[1] + 20, 5, 10))
        pygame.draw.rect(win, (0, 0, 0), (snake.position[0] + 20, snake.position[1] + 20, 5, 10))
    display_score(SCORE)
    pygame.display.update()
pygame.quit()
