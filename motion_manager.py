import pygame
import color
import board


def hover(display, x, y, image_path, block_size):
    x_count = x // 40
    y_count = y // 40
    image = pygame.image.load(image_path)
    image = pygame.transform.scale(image, (36, 36))
    # display.blit(image, (x_count*40 + 3, y_count*40 + 3))
    pygame.draw.rect(display, color.blue, (x_count * block_size + 1, y_count * block_size + 1, block_size, block_size))


def motion_in_board(display, x, y, board):
    if board.left < x < board.right and board.up < y < board.down:
        x_vertical = ((x // board.block_size) * board.block_size) + 2
        y_vertical = board.up + 2
        y_horizontal = ((y // board.block_size) * board.block_size) + 2
        x_horizontal = board.left + 2
        pygame.draw.rect(display,
                         color.black_red,
                         (x_vertical, y_vertical, board.block_size - 2, (board.block_size * board.y_count) - 2))
        pygame.draw.rect(display,
                         color.black_red,
                         (x_horizontal, y_horizontal, (board.block_size * board.x_count) - 2, board.block_size - 2))