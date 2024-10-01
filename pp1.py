import os
import sys
import pygame
import pytmx
import random

import time

pygame.init()
pygame.display.set_caption('Игра')
pygame.key.set_repeat(200, 70)

sound1 = pygame.mixer.Sound('data/музыка.ogg')
sound2 = pygame.mixer.Sound('data/скрип.ogg')
sound3 = pygame.mixer.Sound('data/овации.ogg')
sound1.play(-1)

FPS = 25
WIDTH = 1500
HEIGHT = 680
STEP = 10
DIST = 8
FLOOR = [101, 102, 103, 104, 112, 88, 121, 122, 123, 124]
CELLING = [22, 24, 32, 125, 126, 127, 128, 129, 130, 131]
FLOOR_UP = [85, 86, 87, 97]
FLOOR_DOWN = [89, 90, 91, 98]
FINISH = [73]
WALL = [53, 93, 41, 81]
CELLING_UP = [25, 26, 27, 37]
CELLING_DOWN = [29, 30, 31, 38]
PLAYER = [215]
FASTER = [214]
SLOWER = [284]
ENEMY_DOWN = [298]
BACK = [237]
DOOR = [61]
BOX = FLOOR + CELLING + FLOOR_DOWN + CELLING_UP + WALL

running = True
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen_rect = (0, 0, 1500, 680)
screen1 = pygame.Surface((WIDTH, (HEIGHT - DIST) // 2))
screen2 = pygame.Surface((WIDTH, (HEIGHT - DIST) // 2 - 4))
clock = pygame.time.Clock()

player = None
all_sprites1 = pygame.sprite.Group()
tiles_group1 = pygame.sprite.Group()
player_group1 = pygame.sprite.Group()
box_group1 = pygame.sprite.Group()
bad_group1 = pygame.sprite.Group()
good_group1 = pygame.sprite.Group()
back_group1 = pygame.sprite.Group()
moving_up_group1 = pygame.sprite.Group()
moving_down_group1 = pygame.sprite.Group()
walls1 = pygame.sprite.Group()
finish_group1 = pygame.sprite.Group()
floor_up_group1 = pygame.sprite.Group()
celling_down_group1 = pygame.sprite.Group()
enemy_down_group1 = pygame.sprite.Group()

all_sprites2 = pygame.sprite.Group()
tiles_group2 = pygame.sprite.Group()
player_group2 = pygame.sprite.Group()
box_group2 = pygame.sprite.Group()
bad_group2 = pygame.sprite.Group()
good_group2 = pygame.sprite.Group()
back_group2 = pygame.sprite.Group()
moving_up_group2 = pygame.sprite.Group()
moving_down_group2 = pygame.sprite.Group()
walls2 = pygame.sprite.Group()
finish_group2 = pygame.sprite.Group()
floor_up_group2 = pygame.sprite.Group()
celling_down_group2 = pygame.sprite.Group()
enemy_down_group2 = pygame.sprite.Group()


def load_image(name, size=None, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pygame.image.load(fullname)
    except pygame.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if size is not None:
        image = pygame.transform.scale(image, size)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
        image = image.convert()
    else:
        image = image.convert_alpha()

    return image


def load_level(filename):
    filename = "data/" + filename
    level = pytmx.load_pygame(filename)
    return level


def generate_level1(level):
    new_player, x, y = None, None, None
    for y in range(level.height):
        for x in range(level.width):
            if get_tile_id(level, [x, y]) in BOX:
                Tile1(level.get_tile_image(x, y, 0), x, y).add(box_group1)
            elif get_tile_id(level, [x, y]) in DOOR:
                Tile1(load_image('door2.png'), x, y)
            elif get_tile_id(level, [x, y]) in FLOOR_UP:
                Tile1(level.get_tile_image(x, y, 0), x, y).add(floor_up_group1)
            elif get_tile_id(level, [x, y]) in CELLING_DOWN:
                Tile1(level.get_tile_image(x, y, 0), x, y).add(celling_down_group1)
            elif get_tile_id(level, [x, y]) in FINISH:
                Tile1(load_image("door1.png"), x, y).add(finish_group1)
            elif get_tile_id(level, [x, y]) in PLAYER:
                Tile1(load_image('tile96.png', (48, 48), -1), x, y)
                new_player = Player1(x, y)
            elif get_tile_id(level, [x, y]) == 174:
                Tile1(load_image("tile96.png"), x, y)
            elif get_tile_id(level, [x, y]) == 7:
                Tile1(load_image("tile134.png"), x, y)
            elif get_tile_id(level, [x, y]) == 8:
                Tile1(load_image("tile133.png"), x, y).add(box_group1)
            elif get_tile_id(level, [x, y]) == 9:
                Tile1(load_image("tile132.png"), x, y)
            elif get_tile_id(level, [x, y]) in FASTER:
                Tile1(load_image('fast.png', (48, 48), -1), x, y).add(good_group1)
            elif get_tile_id(level, [x, y]) in SLOWER:
                Tile1(load_image('slow.png', (48, 48)), x, y).add(bad_group1)
            elif get_tile_id(level, [x, y]) in BACK:
                Tile1(load_image('back.png', (48, 48), -1), x, y).add(back_group1)
            elif get_tile_id(level, [x, y]) in ENEMY_DOWN:
                Tile1(load_image('cage.png', (48, 48)), x, y).add(enemy_down_group1)
            elif get_tile_id(level, [x, y]) == 136:
                Tile1(level.get_tile_image(x, y, 0), x, y).add(moving_up_group1)
                wall = pygame.sprite.Sprite()
                walls1.add(wall)
                wall.image = pygame.Surface([1, HEIGHT // 2])
                wall.rect = pygame.Rect(x * 48 - 200, 0, 1, HEIGHT // 2)
            elif get_tile_id(level, [x, y]) == 23:
                Tile1(level.get_tile_image(x, y, 0), x, y).add(moving_down_group1)
                wall = pygame.sprite.Sprite()
                walls1.add(wall)
                wall.image = pygame.Surface([1, HEIGHT // 2])
                wall.rect = pygame.Rect(x * 48 - 200, 0, 1, HEIGHT // 2)
            else:
                Tile1(level.get_tile_image(x, y, 0), x, y)
    return new_player


def get_tile_id(level, pos):
    try:
        return level.tiledgidmap[level.get_tile_gid(*pos, 0)]
    except KeyError:
        return 174


def generate_level2(level):
    new_player, x, y = None, None, None
    for y in range(level.height):
        for x in range(level.width):
            if get_tile_id(level, [x, y]) in BOX:
                Tile2(level.get_tile_image(x, y, 0), x, y).add(box_group2)
            elif get_tile_id(level, [x, y]) in DOOR:
                Tile2(load_image('door2.png'), x, y)
            elif get_tile_id(level, [x, y]) in FLOOR_UP:
                Tile2(level.get_tile_image(x, y, 0), x, y).add(floor_up_group2)
            elif get_tile_id(level, [x, y]) in CELLING_DOWN:
                Tile2(level.get_tile_image(x, y, 0), x, y).add(celling_down_group2)
            elif get_tile_id(level, [x, y]) in FINISH:
                Tile2(load_image("door1.png"), x, y).add(finish_group2)
            elif get_tile_id(level, [x, y]) in PLAYER:
                Tile2(load_image('tile96.png', (48, 48), -1), x, y)
                new_player = Player2(x, y)
            elif get_tile_id(level, [x, y]) == 174:
                Tile2(load_image("tile96.png"), x, y)
            elif get_tile_id(level, [x, y]) == 7:
                Tile2(load_image("tile134.png"), x, y)
            elif get_tile_id(level, [x, y]) == 8:
                Tile2(load_image("tile133.png"), x, y).add(box_group2)
            elif get_tile_id(level, [x, y]) == 9:
                Tile2(load_image("tile132.png"), x, y)
            elif get_tile_id(level, [x, y]) in FASTER:
                Tile2(load_image('fast.png', (48, 48), -1), x, y).add(good_group2)
            elif get_tile_id(level, [x, y]) in SLOWER:
                Tile2(load_image('slow.png', (48, 48), -1), x, y).add(bad_group2)
            elif get_tile_id(level, [x, y]) in BACK:
                Tile2(load_image('back.png', (48, 48), -1), x, y).add(back_group2)
            elif get_tile_id(level, [x, y]) in ENEMY_DOWN:
                Tile2(load_image('cage.png', (48, 48)), x, y).add(enemy_down_group2)
            elif get_tile_id(level, [x, y]) == 136:
                Tile2(level.get_tile_image(x, y, 0), x, y).add(moving_up_group2)
                wall = pygame.sprite.Sprite()
                walls2.add(wall)
                wall.image = pygame.Surface([1, HEIGHT // 2])
                wall.rect = pygame.Rect(x * 48 - 200, 0, 1, HEIGHT // 2)
            elif get_tile_id(level, [x, y]) == 23:
                Tile2(level.get_tile_image(x, y, 0), x, y).add(moving_down_group2)
                wall = pygame.sprite.Sprite()
                walls2.add(wall)
                wall.image = pygame.Surface([1, HEIGHT // 2])
                wall.rect = pygame.Rect(x * 48 - 200, 0, 1, HEIGHT // 2)
            else:
                Tile2(level.get_tile_image(x, y, 0), x, y)
    return new_player


def terminate():
    pygame.quit()
    sys.exit()


player_image = load_image('ghost2.png', (54, 54))

tile_width = tile_height = 48


class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, dx, dy, won):
        if won == 1:
            self.fire = [load_image('star4.jpg')]
        else:
            self.fire = [load_image('star5.jpg')]

        for scale in (5, 10, 20):
            self.fire.append(pygame.transform.scale(self.fire[0], (scale, scale)))
        super().__init__(all_sprites)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()
        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = 0.1

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen_rect):
            self.kill()


def create_particles(position, won):
    particle_count = 20
    numbers = range(-5, 6)
    for _ in range(particle_count):
        Particle(position, random.choice(numbers), random.choice(numbers), won)


class Tile1(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(tiles_group1, all_sprites1)
        self.image = image
        self.rect = pygame.Rect(tile_width * pos_x, tile_height * pos_y, 48, 48)
        self.mask = pygame.mask.from_surface(self.image)


class Tile2(pygame.sprite.Sprite):
    def __init__(self, image, pos_x, pos_y):
        super().__init__(tiles_group2, all_sprites2)
        self.image = image
        self.rect = pygame.Rect(tile_width * pos_x, tile_height * pos_y, 48, 48)


class Player1(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group1, all_sprites1)
        self.flag = False
        self.down = False
        self.tm = 0
        self.first = False
        self.third = False
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, event=False):
        if self.first:
            self.tm += clock1.tick() / 1000
            if self.tm >= 0.2:
                self.image = load_image("ghost2.png", (52, 52))
                self.first = False
        if self.third:
            self.tm += clock1.tick() / 1000
            if self.tm >= 0.2:
                self.image = load_image("ghost2.png", (52, 52))
                self.third = False
        x1 = self.rect.x
        y1 = self.rect.y
        if not event:
            self.rect.x += STEP
            if pygame.sprite.spritecollide(self, bad_group1, False, collided=pygame.sprite.collide_mask):
                self.rect.x -= 7

            if pygame.sprite.spritecollide(self, good_group1, False, collided=pygame.sprite.collide_mask):
                self.rect.x += 10

            sprite = pygame.sprite.spritecollideany(self, back_group1, collided=pygame.sprite.collide_mask)
            if sprite:
                sprite.kill()
                self.rect.x -= 240

            sprite = pygame.sprite.spritecollideany(self, walls1)
            if sprite:
                for sp in moving_up_group1:
                    if sprite.rect.x + 199.99 <= sp.rect.x <= sprite.rect.x + 200.01:
                        move_wall1(sp, 'up', 3)
                for sp in moving_down_group1:
                    if sprite.rect.x + 199.99 <= sp.rect.x <= sprite.rect.x + 200.01:
                        move_wall1(sp, 'down', 3)
        elif event and not self.down:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.image = load_image('ghost1.png', (52, 52))
                player1.rect.y -= STEP
                self.first = True
                self.tm = 0
            if keys[pygame.K_s]:
                self.third = True
                self.tm = 0
                self.image = load_image('ghost3.png', (52, 52))
                player1.rect.y += STEP
        if self.down:
            self.rect.y += 10
            self.rect.x = x1

        if pygame.sprite.spritecollide(self, enemy_down_group1, True, collided=pygame.sprite.collide_mask):
            player2.down = True
            player2.image = load_image('ghost_in_cage.png', (52, 52))

        if pygame.sprite.spritecollide(self, box_group1, False, collided=pygame.sprite.collide_mask):
            if self.down:
                self.image = load_image("ghost2.png")
                self.down = False
            self.rect.x = x1
            self.rect.y = y1

        if pygame.sprite.spritecollide(self, floor_up_group1, False, collided=pygame.sprite.collide_mask):
            if self.down:
                self.image = load_image('ghost2.png', (52, 52))
                self.down = False
            self.rect.y -= 11

        if pygame.sprite.spritecollide(self, celling_down_group1, False, collided=pygame.sprite.collide_mask):
            self.rect.y += 11

        sprites = pygame.sprite.spritecollide(self, finish_group1, False, collided=pygame.sprite.collide_mask)
        if sprites:
            self.flag = True
            clock.tick(4)
            sprites[0].image = load_image("door2.png")


class Player2(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(player_group2, all_sprites2)
        self.flag = False
        self.down = False
        self.first = False
        self.third = False
        self.tm = 0
        self.image = player_image
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.mask = pygame.mask.from_surface(self.image)

    def update(self, event=False):
        if self.first:
            self.tm += clock1.tick() / 1000
            if self.tm >= 0.2:
                self.image = load_image("ghost2.png", (52, 52))
                self.first = False
        if self.third:
            self.tm += clock1.tick() / 1000
            if self.tm >= 0.2:
                self.image = load_image("ghost2.png", (52, 52))
                self.third = False
        x1 = self.rect.x
        y1 = self.rect.y
        if not event:
            self.rect.x += STEP
            if pygame.sprite.spritecollide(self, bad_group2, False, collided=pygame.sprite.collide_mask):
                self.rect.x -= 7

            if pygame.sprite.spritecollide(self, good_group2, False, collided=pygame.sprite.collide_mask):
                self.rect.x += 10

            sprite = pygame.sprite.spritecollideany(self, back_group2, collided=pygame.sprite.collide_mask)
            if sprite:
                sprite.kill()
                self.rect.x -= 240

            sprite = pygame.sprite.spritecollideany(self, walls2)
            if sprite:
                for sp in moving_up_group2:
                    if sprite.rect.x + 199.99 <= sp.rect.x <= sprite.rect.x + 200.01:
                        move_wall2(sp, 'up', 3)
                for sp in moving_down_group2:
                    if sprite.rect.x + 199.99 <= sp.rect.x <= sprite.rect.x + 200.01:
                        move_wall2(sp, 'down', 3)
        elif event and not self.down:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP]:
                player2.rect.y -= STEP
                self.first = True
                self.tm = 0
                self.image = load_image('ghost1.png', (52, 52))
            if keys[pygame.K_DOWN]:
                self.third = True
                self.tm = 0
                self.image = load_image('ghost3.png', (52, 52))
                player2.rect.y += STEP
        if self.down:
            self.rect.y += 10
            self.rect.x = x1

        if pygame.sprite.spritecollide(self, enemy_down_group2, True, collided=pygame.sprite.collide_mask):
            player1.down = True
            player1.image = load_image("ghost_in_cage.png", (52, 52))

        if pygame.sprite.spritecollide(self, box_group2, False, collided=pygame.sprite.collide_mask):
            if self.down:
                self.image = load_image('ghost2.png', (52, 52))
                self.down = False
            self.rect.x = x1
            self.rect.y = y1

        if pygame.sprite.spritecollide(self, floor_up_group2, False, collided=pygame.sprite.collide_mask):
            if self.down:
                self.image = load_image('ghost2.png', (52, 52))
                self.down = False
            self.rect.y -= 11

        if pygame.sprite.spritecollide(self, celling_down_group2, False, collided=pygame.sprite.collide_mask):
            self.rect.y += 11

        sprites = pygame.sprite.spritecollide(self, finish_group2, False, collided=pygame.sprite.collide_mask)
        if sprites:
            self.flag = True
            clock.tick(4)
            sprites[0].image = load_image("door2.png")


class Camera:
    def __init__(self):
        self.dx = 0

    def apply(self, obj):
        obj.rect.x += self.dx

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)


def move_wall1(wall, dir, length):
    if dir == 'up':
        for i in range(1, length + 1):
            new_wall = pygame.sprite.Sprite(box_group1, all_sprites1, tiles_group1)
            new_wall.image = load_image('tile103.png', (48, 48))
            new_wall.rect = new_wall.image.get_rect()
            new_wall.rect.x = wall.rect.x
            new_wall.rect.y = wall.rect.y - 48 * i + 1
    else:
        for i in range(1, length + 1):
            new_wall = pygame.sprite.Sprite(box_group1, all_sprites1, tiles_group1)
            new_wall.image = load_image('tile103.png', (48, 48))
            new_wall.rect = new_wall.image.get_rect()
            new_wall.rect.x = wall.rect.x
            new_wall.rect.y = wall.rect.y + 48 * i - 1


def move_wall2(wall, dir, length):
    if dir == 'up':
        for i in range(1, length + 1):
            new_wall = pygame.sprite.Sprite(box_group2, all_sprites2, tiles_group2)
            new_wall.image = load_image('tile103.png', (48, 48))
            new_wall.rect = new_wall.image.get_rect()
            new_wall.rect.x = wall.rect.x
            new_wall.rect.y = wall.rect.y - 48 * i + 1
    else:
        for i in range(1, length + 1):
            new_wall = pygame.sprite.Sprite(box_group2, all_sprites2, tiles_group2)
            new_wall.image = load_image('tile103.png', (48, 48))
            new_wall.rect = new_wall.image.get_rect()
            new_wall.rect.x = wall.rect.x
            new_wall.rect.y = wall.rect.y + 48 * i - 1


all_sprites = pygame.sprite.Group()
back_btn = pygame.sprite.Sprite(all_sprites)
back_btn.image = load_image("back_btn.png", (80, 40))
back_btn.rect = back_btn.image.get_rect()
back_btn.rect.x = back_btn.rect.y = 0
clock = pygame.time.Clock()
clock1 = pygame.time.Clock()
clock2 = pygame.time.Clock()
font = pygame.font.Font(None, 40)
running = True
file = '3'
filename = ''
if file == '1':
    filename = 'lev.tmx'
elif file == '2':
    filename = 'lev1.tmx'
elif file == '3':
    filename = 'lev2.tmx'
player1 = generate_level1(load_level(filename))
player2 = generate_level2(load_level(filename))
camera1 = Camera()
camera2 = Camera()
all_sprites1.add(walls1)
all_sprites2.add(walls2)
won = 3
image = load_image("stone_cursor.png", (30, 40))
pygame.mouse.set_visible(False)
mouse_coords = [0, 0]
paused = False
while running:
    if paused:
        screen.fill((200, 200, 200))
        all_sprites.draw(screen)
        font = pygame.font.Font(None, 50)
        text1 = font.render("Пауза", True, (89, 73, 235))
        text2 = font.render("Нажмите кнопку 'P', чтобы продолжить игру", True, (89, 73, 235))
        text1_x = WIDTH // 2 - text1.get_width() // 2
        text1_y = HEIGHT // 2 - text1.get_height() // 2 - 50
        text2_x = WIDTH // 2 - text2.get_width() // 2
        text2_y = HEIGHT // 2 - text2.get_height() // 2 + 50
        screen.blit(text1, (text1_x, text1_y))
        screen.blit(text2, (text2_x, text2_y))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_focused():
                    screen.blit(image, event.pos)
                    mouse_coords = event.pos
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.rect.collidepoint(event.pos):
                    terminate()
            if pygame.mouse.get_focused():
                screen.blit(image, mouse_coords)
            pygame.display.flip()
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                paused = False
    else:
        if player1.flag:
            running = False
            won = 1

        if player2.flag:
            running = False
            won = 2

        player1.update()
        player2.update()

        camera1.update(player1)
        camera2.update(player2)

        for sprite in all_sprites1:
            camera1.apply(sprite)

        for sprite in all_sprites2:
            camera2.apply(sprite)

        screen.fill((0, 0, 0))
        screen2.blit(load_image('tile96.png', (WIDTH, HEIGHT)), (0, 0))
        screen1.blit(load_image('tile96.png', (WIDTH, HEIGHT)), (0, 0))
        tiles_group1.draw(screen1)
        player_group1.draw(screen1)
        tiles_group2.draw(screen2)
        player_group2.draw(screen2)
        screen.blit(screen1, (0, 0))
        screen.blit(screen2, (0, (HEIGHT - DIST) // 2 + DIST))
        all_sprites.draw(screen)
        for event in pygame.event.get():
            keys = pygame.key.get_pressed()
            if keys[pygame.K_p]:
                print(0)
                paused = True
            player1.update(True)
            player2.update(True)
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEMOTION:
            if pygame.mouse.get_focused():
                screen.blit(image, event.pos)
                mouse_coords = event.pos
        if event.type == pygame.MOUSEBUTTONDOWN:
            if back_btn.rect.collidepoint(event.pos):
                terminate()
        if pygame.mouse.get_focused():
            screen.blit(image, mouse_coords)
        pygame.display.flip()

        clock.tick(FPS)

sound1.stop()
sound2.play()
time.sleep(3)
sound2.stop()
sound3.play(-1)

if won != 3:
    running = True
    a = 1
    while running:
        a += 1
        if a % 10 == 0:
            if won == 1:
                create_particles((random.randint(0, 1500), random.randint(0, 800)), 1)
            else:
                create_particles((random.randint(0, 1500), random.randint(0, 800)), 2)

        all_sprites.update()
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_btn.rect.collidepoint(event.pos):
                    terminate()
            if event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_focused():
                    screen.blit(image, event.pos)
                    mouse_coords = event.pos
        if pygame.mouse.get_focused():
            screen.blit(image, mouse_coords)
        pygame.display.flip()
        pygame.display.flip()
        clock.tick(FPS)

terminate()
