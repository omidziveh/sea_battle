import pygame
import sys
import math

from pygame.constants import MOUSEBUTTONUP, MOUSEMOTION
from board import Board
from ship import Ship, get_clicked
from button import Button
from photo import Photo
import motion_manager
import csv
import drag_manager
import drop_manager
import click_manager
import efects
import color
import bot


def in_range(first, last, radius=3):
    if math.sqrt((first[0] - last[0]) ** 2 + (first[1] - last[1]) ** 2) < radius:
        return True
    return False


(open('db/ships/board/bot_board.csv', 'r+')).truncate()

pygame.init()

width = 1000
height = 560

screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)
pygame.display.set_caption("sea_battle")
screen.fill(color.white)

board = Board(screen)  # initate board

ships = []

ships.append(Ship(11, screen, 'assets/images/ship11.png', 38, 38, 520, 320, board.block_size, 'H', board))
ships.append(Ship(12, screen, 'assets/images/ship11.png', 38, 38, 600, 320, board.block_size, 'H', board))
ships.append(Ship(13, screen, 'assets/images/ship11.png', 38, 38, 680, 320, board.block_size, 'H', board))
ships.append(Ship(14, screen, 'assets/images/ship11.png', 38, 38, 760, 320, board.block_size, 'H', board))
ships.append(Ship(21, screen, 'assets/images/ship21.png', 78, 38, 520, 240, board.block_size, 'H', board))
ships.append(Ship(22, screen, 'assets/images/ship21.png', 78, 38, 640, 240, board.block_size, 'H', board))
ships.append(Ship(23, screen, 'assets/images/ship21.png', 78, 38, 760, 240, board.block_size, 'H', board))
ships.append(Ship(31, screen, 'assets/images/ship31.png', 118, 38, 520, 160, board.block_size, 'H', board))
ships.append(Ship(32, screen, 'assets/images/ship31.png', 118, 38, 680, 160, board.block_size, 'H', board))
ships.append(Ship(41, screen, 'assets/images/ship41.png', 158, 38, 520, 80, board.block_size, 'H', board))

buttons = []

buttons.append(Button('rotate', screen, "assets/images/rotate.png", 79, 79, 521, 401))
buttons.append(Button('done', screen, "assets/images/finish.png", 79, 79, 641, 401))

numbers = []

numbers.append(Photo(screen, 0, 0, 440, 440, "assets/images/10.png", False))

pygame.time.Clock().tick(1000)

Button = 'Up'
motion = False
drag = False
last_down = []
last_pos = [0, 0]
drop = False


while True:
    click = False
    hover = True
    screen.fill(color.white)

    for number in numbers:
        number.deploy_photo()

    board.draw_page()
    board.draw_board()

    for button in buttons:
        button.deploy_button()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:  # exit
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:  # Button down
            last_down = event.pos
            drop = False
            Button = 'Down'

        if event.type == MOUSEMOTION:  # motion
            last_pos = event.pos
            if Button == 'Down':  # Drag
                position = event.pos
                if not in_range(position, last_down):
                    drag = True

        if event.type == MOUSEBUTTONUP:  # Button up
            position = event.pos
            drop = True

            if drag:  # Drop
                print('Drop')
                drag = False
                Button = 'Up'
            if Button == 'Down' and in_range(position, last_down):  # click in range
                Button = 'Up'
                click = True
                print('click')
            elif motion and Button == 'Down':  # drag and drop
                Button = 'Up'
                motion = False
                print('drag and drop')

    motion_manager.motion_in_board(screen, last_pos[0], last_pos[1], board)
    if click:
        click_manager.action(last_pos[0], last_pos[1], ships, buttons, board)
    if drag:
        drag_manager.drag_ship(ships, last_pos[0], last_pos[1])
    if drop:
        drop_manager.drop_ship(ships, board)
    for ship in ships:
        ship.draw()
    pygame.display.update()
