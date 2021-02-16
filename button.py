import pygame
import color

class Button:
    def __init__(self, name, display, file_name, length, width, pos_x, pos_y, rotate = 0):
        self.name = name
        self.display = display
        self.file_name = file_name
        self.width = width
        self.length = length
        self.rotate = rotate
        self.pos_x = pos_x
        self.pos_y = pos_y

    def deploy_button(self):
        image = pygame.image.load(self.file_name)
        image = pygame.transform.scale(image, (self.width, self.length))
        if self.rotate:
            image = pygame.transform.rotate(image, self.rotate)
        pygame.draw.rect(self.display, color.white, (self.pos_x, self.pos_y, self.width, self.length))
        self.display.blit(image, (self.pos_x, self.pos_y))

    def get_hitbox(self):
        hitbox = {
            'left': self.pos_x,
            'right': self.pos_x + self.length,
            'up': self.pos_y,
            'down': self.pos_y + self.width}
        return hitbox

    def check_hit(self, x, y):
        hitbox = self.get_hitbox()
        if hitbox['left'] <= x <= hitbox['right'] and hitbox['up'] <= y <= hitbox['down']:
            return True
        return False