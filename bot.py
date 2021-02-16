import pygame
import ship
import random
import board
import csv
from pathlib import Path

def safe_area(ID, block_size):
    data = list(csv.reader(open('db/ships/bot/{ship_id}.csv'.format(ship_id=ID), 'r')))[0]
    left = int(data[0]) - block_size
    right = int(data[0]) + int(data[2]) + block_size
    up = int(data[1]) - block_size
    down = int(data[1]) + int(data[3]) + block_size
    return [left, right, up, down]


def hit_box(ID):
    data = list(csv.reader(open('db/ships/bot/{ship_id}.csv'.format(ship_id=ID), 'r')))[0]
    left = int(data[0])
    right = int(data[0]) + int(data[2])
    up = int(data[1])
    down = int(data[1]) + int(data[3])
    return [left, right, up, down]

"""
def check_bot_ships_in_safe_area(ID, block_size):
    bot_ship_safe_area = safe_area(ID, block_size)
    bot_ship_hit_box = hit_box(ID)
    if (bot_ship_safe_area[0] <= bot_ship_hit_box[1] <= bot_ship_safe_area[1] or
        bot_ship_safe_area[0] <= bot_ship_hit_box[0] <= bot_ship_safe_area[1]) and \
            (bot_ship_safe_area[2] <= bot_ship_hit_box[3] <= bot_ship_safe_area[3] or
             bot_ship_safe_area[2] <= bot_ship_hit_box[2] <= bot_ship_safe_area[3]):
        return False
    return True
"""
def check_formation(ship_id , block_size):
    """
    :param block_size:
    :return: True if ok False if not ok
    """
    pathlist = Path('db/ships/bot').glob('*.csv')
    bot_safe_area = safe_area(ship_id, block_size)

    for path in pathlist:
        if str(path.name).split('.')[0] == str(ship_id):
            continue
        other_ships_data = open(path).readline().split(',')
        bot_hit_box = hit_box(other_ships_data[5])
        if (bot_safe_area[0] < bot_hit_box[1] < bot_safe_area[1] or
            bot_safe_area[0] < bot_hit_box[0] < bot_safe_area[1]) and \
                (bot_safe_area[2] < bot_hit_box[3] < bot_safe_area[3] or
                bot_safe_area[2] < bot_hit_box[2] < bot_safe_area[3]):
            return False
    return True


def ship_bots(ID, length, width, board, block_size):
    orientation_options = ["H", "V"]
    orientation = random.choice(orientation_options)
    if orientation == "H":
        x = random.randint(board.left, board.right - length + board.block_size)
        y = random.randint(board.up, board.down - width + board.block_size)
        x = x // block_size * block_size
        y = y // block_size * block_size
    if orientation == "V":
        length, width = width, length
        x = random.randint(board.left, board.right - length + board.block_size)
        y = random.randint(board.up, board.down - width + board.block_size)
        x = x // block_size * block_size
        y = y // block_size * block_size
    csv.writer(open('db/ships/bot/{ship_id}.csv'.format(ship_id=ID), 'w')).writerows([
        (x, y, length, width, orientation, ID, "1"),
        ('x', 'y', 'length', 'width', 'orientation', 'ID')])


def get_all_ships():
    """
    returns a list containing IDs for all ships on the display.
    """
    ships = []
    pathlist = Path('db/ships/bot').rglob('*.csv')
    for path in pathlist:
        ID = int(path.name.split('.')[0])
        ships.append(ID)

    return ships

def init_ships(board, block_size):
    ship_bots("41", 160, 40, board, block_size)
    ship_bots("31", 120, 40, board, block_size)
    ship_bots("32", 120, 40, board, block_size)
    ship_bots("21", 80, 40, board, block_size)
    ship_bots("22", 80, 40, board, block_size)
    ship_bots("23", 80, 40, board, block_size)
    ship_bots("11", 40, 40, board, block_size)
    ship_bots("12", 40, 40, board, block_size)
    ship_bots("13", 40, 40, board, block_size)
    ship_bots("14", 40, 40, board, block_size)

def deploy(board, block_size):
    for ship_id in get_all_ships():
        if not check_formation(ship_id, block_size):
            ship_bots(str(ship_id), int(str(ship_id)[0]) * 40, 40, board, block_size)
            deploy(board, block_size)
