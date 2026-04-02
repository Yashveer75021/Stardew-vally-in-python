import pygame
from setting import *
from player import Player

class Level:
    def __init__(self):
        #getting the display surface
        self.display_surface = pygame.display.get_surface()

        #sprite group setup
        self.all_sprites = pygame.sprite.Group() 

        self.setup()

    def setup(self):
        self.player = Player((640, 360), self.all_sprites)

    def run(self, dt):
        self.display_surface.fill('black') 
        self.all_sprites.draw(self.display_surface)
        self.all_sprites.update(dt)