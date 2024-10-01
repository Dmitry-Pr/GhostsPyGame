import pygame as pg
import os


def load_image(name, size=None, color_key=None):
    fullname = os.path.join('data', name)
    try:
        image = pg.image.load(fullname)
    except pg.error as message:
        print('Cannot load image:', name)
        raise SystemExit(message)
    if size is not None:
        image = pg.transform.scale(image, size)
    if color_key is not None:
        if color_key == -1:
            color_key = image.get_at((0, 0))
        image.set_colorkey(color_key)
        image = image.convert()
    else:
        image = image.convert_alpha()

    return image


class Board:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.left = 5
        self.top = 5
        self.cell_size = 60

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self):
        a = self.left
        b = self.top
        c = self.cell_size
        for j in range(len(self.board)):
            for i in range(len(self.board[j])):
                pg.draw.rect(screen, (39, 204, 17), (a + i * c, b + j * c, c, c), width=1)

    def get_click(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        self.on_click(cell)

    def get_cell(self, mouse_pos):
        if mouse_pos[0] > (self.left + self.cell_size * self.width) or mouse_pos[0] < self.left:
            return None
        elif mouse_pos[1] > (self.top + self.cell_size * self.height) or mouse_pos[1] < self.top:
            return None
        else:
            x = (mouse_pos[0] - self.left) // self.cell_size
            y = (mouse_pos[1] - self.top) // self.cell_size
            return x, y

    def on_click(self, cell_coords):
        if cell_coords is None:
            return 0
        x = cell_coords[0]
        y = cell_coords[1]
        pg.draw.rect(screen, RED, (
            self.left + x * self.cell_size + 1, self.top + y * self.cell_size + 1, self.cell_size - 2,
            self.cell_size - 2))

        if x == 0:
            point1 = "1"
            text3 = font.render(point1, True, (0, 0, 0))
            screen.blit(text3, (160, 420))
            pg.display.flip()

            my_file = open("data/level.txt", "w")
            my_file.write("1")
            my_file.close()

            os.system('pp1.py')

            pg.draw.rect(screen, BLACK, (
                self.left + x * self.cell_size + 1, self.top + y * self.cell_size + 1, self.cell_size - 2,
                self.cell_size - 2))
            point1 = "1"
            text3 = font.render(point1, True, (39, 204, 17))
            screen.blit(text3, (160, 420))

        elif x == 1:
            point1 = "2"
            text3 = font.render(point1, True, (0, 0, 0))
            screen.blit(text3, (240, 420))
            pg.display.flip()

            my_file = open("data/level.txt", "w")
            my_file.write("2")
            my_file.close()

            os.system('pp1.py')

            pg.draw.rect(screen, BLACK, (
                self.left + x * self.cell_size + 1, self.top + y * self.cell_size + 1, self.cell_size - 2,
                self.cell_size - 2))
            point1 = "2"
            text3 = font.render(point1, True, (39, 204, 17))
            screen.blit(text3, (240, 420))
        elif x == 2:
            my_file = open("data/level.txt", 'w')
            my_file.write("3")
            my_file.close()

            point1 = "3"
            text3 = font.render(point1, True, (0, 0, 0))
            screen.blit(text3, (320, 420))
            pg.display.flip()

            os.system('pp1.py')

            pg.draw.rect(screen, BLACK, (
                self.left + x * self.cell_size + 1, self.top + y * self.cell_size + 1, self.cell_size - 2,
                self.cell_size - 2))
            point1 = "3"
            text3 = font.render(point1, True, (39, 204, 17))
            screen.blit(text3, (320, 420))


if __name__ == '__main__':
    pg.init()
    pg.display.set_caption('Меню')
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BlUE = (0, 0, 255)
    colors = [BLACK, RED]
    WHITE = (255, 255, 255)
    size = weight, height = 500, 500
    screen = pg.display.set_mode(size)
    board = Board(3, 1)
    board.set_view(130, 390, 80)
    running = True
    fon = pg.transform.scale(load_image('fon4.jpg'), (500, 500))
    screen.blit(fon, (0, 0))
    hello = "Добро пожаловать!"
    hello2 = "Выбирайте уровень:"

    font = pg.font.Font(None, 40)
    text1 = font.render(hello, True, (229, 111, 33), (0, 0, 0))
    screen.blit(text1, (110, 50))
    text2 = font.render(hello2, True, (255, 102, 0), (0, 0, 0))
    screen.blit(text2, (115, 250))
    point1 = "1"
    text3 = font.render(point1, True, (39, 204, 17))
    screen.blit(text3, (160, 420))

    point1 = "2"
    text3 = font.render(point1, True, (39, 204, 17))
    screen.blit(text3, (240, 420))

    point1 = "3"
    text3 = font.render(point1, True, (39, 204, 17))
    screen.blit(text3, (320, 420))

    pg.display.flip()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.MOUSEBUTTONDOWN:
                board.get_click(event.pos)

        board.render()
        pg.display.flip()
