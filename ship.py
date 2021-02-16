import pygame
import csv
import math
import board
import color
import random
from pathlib import Path


def size(a, b):
    return math.sqrt((a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2)


class Ship:
    pos_x = 0
    pos_y = 0
    x_first = 0
    y_first = 0

    def __init__(self, ID, display, image_path, length, width, ix, iy, block_size, orientation, board):
        self.ID = ID
        csv.writer(open('db/ships/user/{ship_id}.csv'.format(ship_id=ID), 'w')).writerows(
            [('x', 'y', 'length', 'width', 'movement', 'left', 'right', 'up', 'down', 'clicked'),
             (ix, iy, length, width, 0, ix, ix + length, iy, iy + width, 0)])
        self.image_path = image_path
        self.display = display
        self.length = length
        self.width = width
        self.image = pygame.transform.scale(pygame.image.load(image_path), (width, length))
        self.block_size = block_size
        self.x_first = ix
        self.y_first = iy
        Ship.pos_x = ix
        Ship.pos_y = iy
        self.image = pygame.transform.rotate(self.image, 90)
        self.orientation = orientation
        self.board = board

    def draw(self):
        Ship.pos_x, Ship.pos_y = self.current_location()
        self.display.blit(self.image, (Ship.pos_x, Ship.pos_y))
        fit = self.find_fit(Ship.pos_x, Ship.pos_y, self.block_size)
        self.set_new_location(fit[0] + 2, fit[1] + 2)
        self.update_hitbox()

    def find_fit(self, x, y, block_size):
        up_left = [x // block_size * block_size, y // block_size * block_size]
        up_right = [up_left[0] + block_size, up_left[1]]
        down_left = [up_left[0], up_left[1] + block_size]
        down_right = [up_left[0] + block_size, up_left[1] + block_size]
        difs = {'ul': size([x, y], up_left),
                'ur': size([x, y], up_right),
                'dl': size([x, y], down_left),
                'dr': size([x, y], down_right)}
        min_dist = block_size + 1
        dir = None
        for key, value in difs.items():
            if min_dist > value:
                min_dist = value
                dir = key

        if dir == 'ul':
            return up_left
        if dir == 'ur':
            return up_right
        if dir == 'dl':
            return down_left
        if dir == 'dr':
            return down_right

    def current_location(self):
        """
        :return: tuple(x, y)
        """
        data = list(csv.reader(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'r')))[::2]
        return int(data[1][0]), int(data[1][1])

    def set_new_location(self, x, y):
        data = list(csv.reader(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'r')))[::2]
        data[1][0] = x
        data[1][1] = y
        csv.writer(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'w')).writerows(data)

    def get_movement_status(self):
        data = list(csv.reader(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'r')))[::2]
        if data[1][4] == 1:
            return True
        return False

    def set_moving_status(self, status):
        data = list(csv.reader(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'r')))[::2]
        if status:
            data[1][4] = '1'
        if not status:
            data[1][4] = '0'
        csv.writer(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'w')).writerows(data)

    def get_clicked_status(self):
        data = list(csv.reader(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'r')))[::2]
        if data[1][9] == 1:
            return True
        return False

    def set_clicked_status(self, status):
        data = list(csv.reader(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'r')))[::2]
        if status:
            data[1][9] = '1'
        if not status:
            data[1][9] = '0'
        csv.writer(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'w')).writerows(data)

    def update_hitbox(self):
        data = list(csv.reader(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'r')))[::2]
        data[1][5] = int(data[1][0])
        data[1][6] = int(data[1][0]) + int(data[1][2])
        data[1][7] = int(data[1][1])
        data[1][8] = int(data[1][1]) + int(data[1][3])
        csv.writer(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'w')).writerows(data)

    def check_hit(self, x, y):
        data = list(csv.reader(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'r')))[::2][1]
        hitbox = {
            'left': int(data[0]),
            'right': int(data[0]) + int(data[2]),
            'up': int(data[1]),
            'down': int(data[1]) + int(data[3])}

        if hitbox['left'] <= x <= hitbox['right'] and hitbox['up'] <= y <= hitbox['down']:
            return True
        return False

    def get_hitbox(self):
        """
        :return: [left, right, up, down]
        """
        data = list(csv.reader(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'r')))[::2][1]
        return [int(data[5]), int(data[6]), int(data[7]), int(data[8])]

    def get_safe_area(self):
        data = list(csv.reader(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'r')))[::2][1]
        left = int(data[5]) - self.block_size
        right = int(data[6]) + self.block_size
        up = int(data[7]) - self.block_size
        down = int(data[8]) + self.block_size
        return [left, right, up, down]

    def check_ships_in_safe_area(self, ships):
        safe_area = self.get_safe_area()
        for ship in ships:
            if ship != self:
                hit_box = ship.get_hitbox()
                if (safe_area[0] <= hit_box[1] <= safe_area[1] or safe_area[0] <= hit_box[0] <= safe_area[1]) and \
                        (safe_area[2] <= hit_box[3] <= safe_area[3] or safe_area[2] <= hit_box[2] <= safe_area[3]):
                    return False
        return True

    def check_safe_area(self, x, y):
        data = list(csv.reader(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'r')))[::2][1]
        left = int(data[5]) - self.block_size
        right = int(data[6]) + self.block_size
        up = int(data[7]) - self.block_size
        down = int(data[8]) + self.block_size

        if left <= x <= right and up <= y <= down:
            return True
        return False

    def move(self, x, y):
        if self.orientation == "H":
            self.set_new_location(x - self.length // 2, y - self.width // 2)
        elif self.orientation == "V":
            self.set_new_location(x - self.width // 2, y - self.length // 2)
        self.update_hitbox()

    def check_in_board(self):
        ship_hitbox = self.get_hitbox()
        if ship_hitbox[0] >= board.Board.left and ship_hitbox[1] <= board.Board.right and \
                ship_hitbox[2] >= board.Board.up and ship_hitbox[3] <= board.Board.down:
            return True
        return False

    def rotate(self, ships, dir):
        if dir == self.orientation:
            pass
        elif self.orientation == "H":
            data = list(csv.reader(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'r')))[::2]
            data[1][2], data[1][3] = data[1][3], data[1][2]
            data[1][5] = int(data[1][0])
            data[1][6] = int(data[1][0]) + int(data[1][2])
            data[1][7] = int(data[1][1])
            data[1][8] = int(data[1][1]) + int(data[1][3])
            new_hitbox = [data[1][5], data[1][6], data[1][7], data[1][8]]
            if new_hitbox[0] < board.Board.left or new_hitbox[1] > board.Board.right or \
                    new_hitbox[2] < board.Board.up or new_hitbox[3] > board.Board.down:
                return 0
            self.orientation = "V"
            self.image = pygame.transform.rotate(self.image, 270)
            csv.writer(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'w')).writerows(data)

            if not self.check_ships_in_safe_area(ships):
                self.rotate(ships, 'H')
                for i in range(5000):
                    pygame.draw.rect(self.display, color.red, (int(data[1][0]),
                                                               int(data[1][1]),
                                                               int(data[1][2]),
                                                               int(data[1][3])))

                print("draw")

        elif self.orientation == "V":
            data = list(csv.reader(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'r')))[::2]
            data[1][2], data[1][3] = data[1][3], data[1][2]
            data[1][5] = int(data[1][0])
            data[1][6] = int(data[1][0]) + int(data[1][2])
            data[1][7] = int(data[1][1])
            data[1][8] = int(data[1][1]) + int(data[1][3])
            new_hitbox = [data[1][5], data[1][6], data[1][7], data[1][8]]
            if new_hitbox[0] < board.Board.left or new_hitbox[1] > board.Board.right or \
                    new_hitbox[2] < board.Board.up or new_hitbox[3] > board.Board.down:
                return 0
            self.orientation = "H"
            self.image = pygame.transform.rotate(self.image, 90)
            csv.writer(open('db/ships/user/{ship_id}.csv'.format(ship_id=self.ID), 'w')).writerows(data)

            if not self.check_ships_in_safe_area(ships):
                self.rotate(ships, 'V')
                for i in range(5000):
                    pygame.draw.rect(self.display, color.red, (int(data[1][0]),
                                                               int(data[1][1]),
                                                               int(data[1][2]),
                                                               int(data[1][3])))



def get_all_ships():
    """
    returns a list containing IDs for all ships on the display.
    """
    ships = []
    pathlist = Path('db/ships/user').rglob('*.csv')
    for path in pathlist:
        ID = int(path.name.split('.')[0])
        ships.append(ID)

    return ships


def get_moving_ship():
    for ship_id in get_all_ships():
        data = list(csv.reader(open('db/ships/user/{ship_id}.csv'.format(ship_id=ship_id), 'r')))[::2]
        if data[1][4] == '1':
            return ship_id
    return None


def get_clicked():
    for ship_id in get_all_ships():
        data = list(csv.reader(open('db/ships/user/{ship_id}.csv'.format(ship_id=ship_id), 'r')))[::2]
        if data[1][9] == '1':
            return ship_id
    return None
