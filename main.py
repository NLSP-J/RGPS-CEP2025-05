import pygame as pg
import random, time
import asyncio
pg.init()
clock = pg.time.Clock()

black = (0, 0, 0)

win_width = 800
win_height = 600
screen = pg.display.set_mode((win_width, win_height))
pg.display.set_caption('Falling Debris')

font = pg.font.Font(None, 30)
speed = 2
score = 0
running = True
lives = 20

player_size = 40
player_pos = [win_width / 2, win_height - player_size]  # 400, 600-40
player_image = pg.image.load('./assets/images/mario.png')
player_image = pg.transform.scale(player_image, (player_size, player_size))  # 40,40

obj_size = 60
obj_data = []     # List to store object positions and their images
obj = pg.image.load('./assets/images/apple.png')
obj = pg.transform.scale(obj, (obj_size, obj_size))

bg_image = pg.image.load('./assets/images/background.png')
bg_image = pg.transform.scale(bg_image, (win_width, win_height))

def change_speed(score):
    global speed
    if score < 5:
        speed = 5
    elif score < 10:
        speed = 8
    elif score < 15:
        speed = 10

def create_object(obj_data):
    if len(obj_data) < 5 and random.random() < 0.1:    
        x = random.randint(0, win_width - obj_size)
        y = 0                                         
        obj_data.append([x, y, obj])


def update_objects(obj_data):
    global lives
    for object in obj_data:
        x, y, image_data = object
        if y < win_height:
            y += speed
            object[1] = y
            screen.blit(image_data, (x, y))
        else:
            obj_data.remove(object)
            lives -= 1
            if lives == 0:
                time.sleep(2)
                running = False
                break


def collision_check(obj_data, player_pos):
    global running, score
    for object in obj_data:
        x, y, image_data = object
        player_x, player_y = player_pos[0], player_pos[1]
        obj_rect = pg.Rect(x, y, obj_size, obj_size)
        player_rect = pg.Rect(player_x, player_y, player_size, player_size)
        if player_rect.colliderect(obj_rect):
            score += 1
            obj_data.remove(object)


async def main():
    global running, player_pos

    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            if event.type == pg.KEYDOWN:
                x, y = player_pos[0], player_pos[1]
                if event.key == pg.K_LEFT:
                    if x > 20:
                        x -= 40
                    else:
                        x = 0
                elif event.key == pg.K_RIGHT:
                    if x < 760:
                        x += 40
                player_pos = [x, y]

        screen.blit(bg_image, (0, 0))
        screen.blit(player_image, (player_pos[0], player_pos[1]))

        text = f'Score: {score}'
        text = font.render(text, 10, black)
        screen.blit(text, (win_width - 200, win_height - 40))
    
        lives_text = f'Lives: {lives}'
        lives_text = font.render(lives_text, 10, black)
        screen.blit(lives_text, (win_width - 200, win_height - 60))

        create_object(obj_data)
        update_objects(obj_data)
        collision_check(obj_data, player_pos)

        clock.tick(30)
        pg.display.flip()

        await asyncio.sleep(0)

asyncio.run(main())