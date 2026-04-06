import pygame
from setting import *

class Transition:
    def __init__(self, reset, player):
        
        #set up 
        self.display = pygame.display.get_surface()
        self.player = player
        self.reset = reset
        
        #overly setting
        self.image = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT)) 
        self.color = 255
        self.speed = -2

    def fade(self):
        self.color += self.speed
        if self.color < 0:
            self.speed *= -1
            self.color = 0
            self.reset()
        if self.color > 255:
            self.color = 255
            self.player.sleep = False
            self.speed = -2
        self.image.fill((self.color,self.color,self.color))
        self.display.blit(self.image,(0,0), special_flags = pygame.BLEND_RGBA_MULT)