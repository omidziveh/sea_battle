import pygame
import color


def deploy_page():
    screen = pygame.display.set_mode((1000, 560))
    pygame.display.set_caption("sea_battle")
    screen.fill(color.white)

    image = pygame.image.load('assets/images/loading.png')
    image = pygame.transform.scale(image, (240, 150))
    screen.blit(image, (960 // 2 - 120, 560 // 2 - 75))
    pygame.display.update()
