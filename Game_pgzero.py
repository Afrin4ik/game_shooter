import pgzrun
import random

import pgzero.game
import pgzero.keyboard
from pgzero.actor import Actor
from pgzero.constants import mouse

keyboard: pgzero.keyboard.keyboard
screen: pgzero.game.screen

WIDTH = 600
HEIGHT = 400

TITLE = "Космичесике путешествия"

FPS = 30

mode = "menu"

count = 0



# Код игры

space = Actor("space")
ship = Actor("ship", (300, 400))
type1 = Actor("ship", (100, 250))
type2 = Actor("ship-2", (300, 250))
type3 = Actor("ship-3", (500, 250))

bullets = []


enemies = []
for i in range(5):
    x = random.randint(0, 600)
    y = random.randint(-450, -50)
    enemy = Actor("enemy", (x, y))
    enemy.speed = random.randint(2, 10)
    enemies.append(enemy)


def draw():
    if mode == "menu":
        space.draw()
        screen.draw.text("Выберите корабль", center=(WIDTH / 2, HEIGHT / 2 - 120), color="white", fontsize=36)
        # отрисовать корабли
        type1.draw()
        type2.draw()
        type3.draw()

    if mode == "game":
        space.draw()
        ship.draw()
        screen.draw.text(f"Score: {str(count)}", center=(45, 15), color="white", fontsize=30)
        for i in range(len(enemies)):
            enemies[i].draw()
        for i in range(len(bullets)):
            bullets[i].draw()
    elif mode == "end":
        space.draw()
        screen.draw.text("GAME OVER", center=(WIDTH/2, HEIGHT/2), color="white", fontsize=36)
        screen.draw.text(f"Score: {str(count)}", center=(WIDTH/2, HEIGHT/2 + 40), color="white", fontsize=30)



def on_mouse_move(pos):
    ship.pos = pos


def new_enemy():
    x = random.randint(0, 600)
    y = random.randint(-450, -50)
    enemy = Actor("enemy", (x, y))
    enemy.speed = random.randint(2, 10)
    enemies.append(enemy)


def enemy_ship():
    global count
    for i in range(len(enemies)):
        if enemies[i].y < 650:
            enemies[i].y = enemies[i].y + enemies[i].speed
        else:
            enemies.pop(i)
            new_enemy()
            # count += 1


def collisions():
    global mode, count
    for i in range(len(enemies)):
        if ship.colliderect(enemies[i]):
            mode = "end"
        for j in range(len(bullets)):
            if bullets[j].colliderect(enemies[i]):
                count = count + 1
                enemies.pop(i)
                bullets.pop(j)
                new_enemy()
                break




def update(dt):
    if mode == "game":
        enemy_ship()
        collisions()
        for i in range(len(bullets)):
            if bullets[i].y < 0:
                bullets.pop(i)
                break
            else:
                bullets[i].y = bullets[i].y - 10


def on_mouse_down(button, pos):
    global mode, ship
    if mode == "menu" and type1.collidepoint(pos):
        ship.image = "ship"
        mode = "game"
    elif mode == "menu" and type2.collidepoint(pos):
        ship.image = "ship-2"
        mode = "game"
    elif mode == "menu" and type3.collidepoint(pos):
        ship.image = "ship-3"
        mode = "game"

    # стрельба
    elif mode == "game" and button == mouse.LEFT:
        bullet = Actor("bullet")
        bullet.pos = ship.pos
        bullets.append(bullet)




pgzrun.go()