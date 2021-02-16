import pygame

class Photo:
    def __init__(self, display, x, y, length, width, file_name, rotate):
        self.display = display
        self.x = x
        self.y = y
        self.length = length
        self.width = width
        self.file_name = file_name
        self.rotate = rotate
    def deploy_photo(self):
        image = pygame.image.load(self.file_name)
        image = pygame.transform.scale(image, (self.length, self.width))
        if self.rotate:
            image = pygame.transform.rotate(image, self.rotate)
        self.display.blit(image, (self.x, self.y))
