import pygame
import color
import sys
import random
from photo import Photo
from board import Board


class Attack:
    history_of_but_attacks = []
    history_of_user_attacks = []

    def __init__(self, page_length, page_width, user_ships):
        self.page_length = page_length
        self.page_width = page_width
        self.user_ships = user_ships

    def draw_ships(self):
        for ship in self.user_ships:
            ship.draw()

    def draw_area(self, mode, screen, x, y, board, rect_color, image_path=None):
        if mode == "image":
            image = pygame.image.load(image_path)
            pygame.transform.scale(image, (40 - 2, 40 - 2))
            screen.blit(image, (x + 2, y + 2))
        elif mode == "rect":
            pygame.draw.rect(screen,
                             rect_color,
                             (x + 2, y + 2, 40 - 2, 40 - 2))

    def attack_bot(self, board):
        """
        :param screen:
        :param board:
        :return a list of attacks:
        """

        global line
        found = False

        bot_attacks = []
        x = random.randint(40, 439)
        y = random.randint(40, 439)
        x = x // 40
        y = y // 40

        data = (open('db/ships/board/user_board.csv', 'r').readlines())
        lines = []
        for line in data:
            if line != "\n":
                lines.append(line)
        for line in lines:
            line = (line.split(','))

            if x == int(line[0]) and y == int(line[1]):
                bot_attacks.append([x * 40, y * 40, "crash", line[2]])
                found = True
        if not found:
            bot_attacks.append([x * 40, y * 40, "none", line[2]])

        return bot_attacks

    def attack_user(self, x, y, board):
        global line, user_attacks
        found = False

        if board.left < x < board.right and \
                board.up < y < board.down:

            x, y = x // 40 - 13, y // 40
            user_attacks = []

            data = (open('db/ships/board/bot_board.csv', 'r').readlines())
            lines = []
            for line in data:
                if line != "\n":
                    lines.append(line)
            for line in lines:
                line = (line.split(','))

                if x == int(line[0]) and y == int(line[1]):
                    user_attacks.append([x * 40 + 520, y * 40, "crash", line[2]])
                    found = True
            if not found:
                user_attacks.append([x * 40 + 520, y * 40, "none", line[2]])
        return user_attacks

    def second_chance(self, file):
        data = file[len(file) - 1]
        if data[0][2] == 'crash':
            return True
        return False

    def draw_events(self, attacks, screen, board):
        for event in attacks:
            event = event[0]
            if event[2] == "crash":
                self.draw_area("rect", screen, event[0], event[1], board, color.red)
            if event[2] == "none":
                self.draw_area("rect", screen, event[0], event[1], board, color.blue)

    def deploy_page(self, board):
        attack_bot_file = []
        attack_user_file = []
        bot_turn = False
        user_turn = True

        global ev, red_arrow_deploy
        numbers = []
        screen = pygame.display.set_mode((self.page_length, self.page_width))
        screen.fill(color.white)

        numbers.append(Photo(screen, 0, 0, 440, 440, 'assets/images/10.png', False))
        numbers.append(Photo(screen, 520, 0, 440, 440, 'assets/images/10.png', False))

        left_board = (Board(screen, 40, 40, 10, 10, 40, color.black))
        right_board = (Board(screen, 560, 40, 10, 10, 40, color.black))

        green_arrow = (Photo(screen, 442, 241, 78, 79, 'assets/images/green_arrow.png', False))
        red_arrow = (Photo(screen, 442, 241, 78, 79, 'assets/images/red_arrow.png', False))

        while True:
            screen.fill(color.white)

            for number in numbers:
                number.deploy_photo()

            left_board.draw_page()
            right_board.draw_board()
            left_board.draw_board()

            if user_turn:
                red_arrow_deploy = False
            if bot_turn:
                red_arrow_deploy = True
                attack_bot_file.append(self.attack_bot(screen))
                bot_turn = False
                user_turn = True
                if self.second_chance(attack_bot_file):
                    bot_turn = True
                    user_turn = False

            if red_arrow_deploy:
                red_arrow.deploy_photo()
            else:
                green_arrow.deploy_photo()

            self.draw_events(attack_bot_file, screen, left_board)
            self.draw_events(attack_user_file, screen, right_board)

            self.draw_ships()

            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    sys.exit()
                if ev.type == pygame.MOUSEBUTTONDOWN and \
                        right_board.left < ev.pos[0] < right_board.right and \
                        right_board.up < ev.pos[1] < right_board.down:
                    attack_user_file.append(self.attack_user(ev.pos[0], ev.pos[1], right_board))
                    if self.second_chance(attack_user_file):
                        user_turn = True
                        bot_turn = False
                    else:
                        bot_turn, user_turn = user_turn, bot_turn
            pygame.display.update()
