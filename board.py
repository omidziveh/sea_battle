import pygame
import color
import csv
from pathlib import Path


class Board:
    left = 0
    right = 0
    up = 0
    down = 0

    def __init__(self, display, pos_x=40, pos_y=40, x_count=10, y_count=10, block_size=40, color=color.black):
        self.display = display
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.y_count = y_count
        self.x_count = x_count
        self.block_size = block_size
        self.color = color
        Board.left = pos_x
        Board.right = pos_x + x_count * block_size
        Board.up = pos_y
        Board.down = pos_y + y_count * block_size


    def draw_page(self):
        display_x_count = self.display.get_width() // self.block_size
        display_y_count = self.display.get_height() // self.block_size
        for i in range(display_y_count + 1):
            pygame.draw.line(self.display,
                             (150, 150, 150),
                             (0, i * self.block_size),
                             (display_x_count * self.block_size, i * self.block_size))
        for i in range(display_x_count + 1):
            pygame.draw.line(self.display,
                             (150, 150, 150),
                             (i * self.block_size, 0),
                             (i * self.block_size, display_y_count * self.block_size))


    def draw_board(self):
        pygame.draw.rect(self.display, color.gray, (self.pos_x,
                                                          self.pos_y,
                                                          self.block_size * self.x_count,
                                                          self.block_size * self.y_count))

        for i in range(self.y_count + 1):
            pygame.draw.line(self.display,
                             self.color,
                             (self.pos_x, i * self.block_size + self.pos_y),
                             (self.pos_x + self.x_count * self.block_size, i * self.block_size + self.pos_y),
                             2)
        for i in range(self.x_count + 1):
            pygame.draw.line(self.display,
                             self.color,
                             (i * self.block_size + self.pos_x, self.pos_y),
                             (i * self.block_size + self.pos_x, self.pos_y + self.y_count * self.block_size),
                             2)

    def read_board(self, user):
        (open('db/ships/board/user_board.csv', 'r+')).truncate()
        counter = 0
        user_addres = 'db/ships/' + user
        pathlist = Path(user_addres).rglob('*.csv')
        for path in pathlist:
            x = self.pos_x - 20
            for i in range(self.x_count):
                y = self.pos_y - 20
                x += self.block_size
                for j in range(self.y_count):
                    y += self.block_size
                    # print(x, y)
                    if user == 'user':
                        file = open(path, "r")
                        ships_data = file.readlines()
                        ships_data = ships_data[2]
                        ships_data = str(ships_data).split(',')
                        if int(ships_data[5]) < x < int(ships_data[6]) and \
                                int(ships_data[7]) < y < int(ships_data[8]):
                            # print([x // self.block_size, y // self.block_size])
                            counter += 1
                            csv.writer(open('db/ships/board/user_board.csv', 'a')).writerows([
                                (x // self.block_size, y // self.block_size, path)])
                    if user == 'bot':
                        ships_data = open(path).readline().split(',')
                        # print(x // self.block_size, y // self.block_size, path)
                        if int(ships_data[0]) < x < int(ships_data[0]) + int(ships_data[2]) and \
                                int(ships_data[1]) < y < int(ships_data[1]) + int(ships_data[3]):
                            counter += 1
                            csv.writer(open('db/ships/board/bot_board.csv', 'a')).writerows([
                                (x // self.block_size, y // self.block_size, path)])
        return counter
