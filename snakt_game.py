import pygame
import random
import math

from os import path

img_dir = path.join(path.dirname(__file__), 'img')
music_dir = path.join(path.dirname(__file__), 'music')


pygame.init()
WIDTH=800
HEIGHT= 800
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
COLUMNS, ROWS, SIZE = 20, 20, 20
WIDTH, HEIGHT = COLUMNS*SIZE, ROWS*SIZE
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock  = pygame.time.Clock()
#загрузка музыки
pygame.mixer.music.load(path.join(music_dir, 'Intense.mp3'))
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)
am = pygame.mixer.Sound(path.join(music_dir,'apple_bite.ogg'))
am.set_volume(0.5)

#background = pygame.Surface((WIDTH, HEIGHT))
#background.fill((255, 255, 255))
background = pygame.image.load(path.join(img_dir,
                                         'imgonline-com-ua-Osvetlenie-EtCbIPWgr5F4eDs.jpg')).convert()
background = pygame.transform.scale(background, (WIDTH, HEIGHT))
background_rect = background.get_rect()
'''for i in range(1, COLUMNS):
    pygame.draw.line(background, (128, 128, 128), (i*SIZE-1, 0), (i*SIZE-1, ROWS*SIZE), 2)
for i in range(1, ROWS):
    pygame.draw.line(background, (128, 128, 128), (0, i*SIZE-1), (COLUMNS*SIZE, i*SIZE-1), 2)'''
#шрифты для надписей
font_style = pygame.font.SysFont(None, 32)
score_font = pygame.font.SysFont("comicsansms", 25)
#функция для вывода финальной записи
def message(msg, color):
    mes = font_style.render(msg, True, color)
    screen.blit(mes, [WIDTH/16, HEIGHT/2])
#функция подсчета очков
def score_for_snake(score):
    value = score_font.render("Ваш счет: " + str(score), True, WHITE)
    screen.blit(value, [0, 0])
    
def hit(pos_a, pos_b, distance):
    dx, dy = pos_a[0]-pos_b[0], pos_a[1]-pos_b[1]
    return math.sqrt(dx*dx + dy*dy) < distance

def hit_body(pos_a, pos_b, length, distance):
    if length > 2:        
        for seg in pos_b:
            #print( seg, pos_a)
            dx, dy = pos_a[0]-seg[0], pos_a[1]-seg[1]
            res = math.sqrt(dx*dx + dy*dy) < distance
            if res:
                return res

    
def random_pos(body):
    pos = None
    while True:
        pos = random.randint(SIZE//2, WIDTH-SIZE//2), random.randint(SIZE//2, HEIGHT-SIZE//2)
        if not any([hit(pos, bpos, 20) for bpos in body]):
            break    
    return pos

def create_body(track, no_pearls, distance):
    body = [(track[0])]
    track_i = 1
    for i in range(1, no_pearls):
        while track_i < len(track):
            pos = track[track_i]
            track_i += 1
            dx, dy = body[-1][0]-pos[0], body[-1][1]-pos[1]
            if math.sqrt(dx*dx + dy*dy) >= distance:
                body.append(pos)
                break
    while len(body) < no_pearls:
        body.append(track[-1])
    del track[track_i:]
    return body

length = 1
track = [(WIDTH//2, HEIGHT//2)]
dir = (1, 0)
food = random_pos(track)
print(food)
food_img =  [pygame.image.load(path.join(img_dir, 'f_1.png')).convert(), pygame.image.load(path.join(img_dir, 'f_2.png')).convert(),
                 pygame.image.load(path.join(img_dir, 'f_3.png')).convert(),pygame.image.load(path.join(img_dir, 'f_9.png')).convert(),
                 pygame.image.load(path.join(img_dir, 'f_5.png')).convert(),pygame.image.load(path.join(img_dir, 'f_8.png')).convert(),
                 pygame.image.load(path.join(img_dir, 'f_7.png')).convert() ]
food_eat = pygame.transform.scale(random.choice(food_img), (20,20))
food_eat.set_colorkey(WHITE)
food_rect = food_eat.get_rect(x = food[0], y = food[1])
run = True
while run:
    
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: dir = (-2, 0)
            elif event.key == pygame.K_RIGHT: dir = (2, 0)
            elif event.key == pygame.K_UP: dir = (0, -2)
            elif event.key == pygame.K_DOWN: dir = (0, 2)

    track.insert(0, track[0][:])    
    track[0] = (track[0][0] + dir[0]) % WIDTH, (track[0][1] + dir[1]) % HEIGHT

    body = create_body(track, length, 20)
    if hit(body[0], food, 20):
        food = random_pos(track)
        food_eat = pygame.transform.scale(random.choice(food_img), (20,20))
        food_eat.set_colorkey(WHITE)
        food_rect = food_eat.get_rect(x = food[0], y = food[1])
        length += 1
        am.play()
    if hit_body(body[0], body[1:], length, 20):
        run = False
    screen.blit(background, background_rect)
    score_for_snake(length -1)
    screen.blit(food_eat, food_rect)
    
    
    for i, pos in enumerate(body):
        color = (255, 0, 0) if i==0 else (0, 192, 0) if (i%2)==0 else (255, 128, 0)
        pygame.draw.circle(screen, color, pos, SIZE//2)
    
    pygame.display.flip()
pygame.quit()
