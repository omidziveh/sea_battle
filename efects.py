import pygame

def deploy_efect(file_name, loops):
    pygame.mixer.music.load(file_name)
    pygame.mixer.music.play(loops)