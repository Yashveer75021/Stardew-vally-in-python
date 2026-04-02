import pygame 
from setting import *
from support import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        
        self.import_assets()
        self.status = 'down_idle'
        self.frame_index = 0

        #generel setup
        self.image = self.animation[self.status][self.frame_index]
        self.rect = self.image.get_rect(center = pos)

        #movement attributes
        self.direction = pygame.math.Vector2()
        self.pos = pygame.math.Vector2(self.rect.center)
        self.speed = 200

    def import_assets(self):
        self.animation = {
            'up' : [],'down' : [],'left' : [],'right' : [],
            'right_idle' : [],'left_idle' : [],'up_idle' : [],'down_idle' : [],
            'right_hoe' : [],'left_hoe' : [],'up_hoe' : [],'down_hoe' : [],
            'right_axe' : [],'left_axe' : [],'up_axe' : [],'down_axe' : [],
            'right_water' : [],'left_water' : [],'up_water' : [],'down_water' : []
        }

        for animation in self.animation.keys():
            full_path = 'graphics/character/' + animation
            self.animation[animation] =  import_folder(full_path)

    def input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_w]:
            self.direction.y = -1
        elif keys[pygame.K_s]:
            self.direction.y = 1
        else:
            self.direction.y = 0

        if keys[pygame.K_a]:
            self.direction.x = -1
        elif keys[pygame.K_d]:
            self.direction.x = 1
        else:
            self.direction.x = 0

    def move(self, dt):
        #normalize the vector so that diagonal movement isn't faster
        if self.direction.magnitude() != 0:
            self.direction = self.direction.normalize()

        #horizontal movement
        self.pos.x += self.direction.x * self.speed * dt
        self.rect.centerx = round(self.pos.x)
        
        
        #vertical movement    
        self.pos.y += self.direction.y * self.speed * dt    
        self.rect.centery = round(self.pos.y)

    def update(self, dt):
        self.input()
        self.move(dt)