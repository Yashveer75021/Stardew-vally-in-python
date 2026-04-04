import pygame
from setting import *
from random import randint, choice
from my_timer import Timer

class Generic(pygame.sprite.Sprite):
    def __init__(self, pos, surf, group, z = LAYERS['ground']):
        super().__init__(group)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z
        self.hitbox = self.rect.copy().inflate(-self.rect.width * 0.2, -self.rect.height * 0.75)

    
class Water(Generic):
    def __init__(self, pos, frames, group):
        
        #amination setup
        self.frame = frames
        self.frame_index = 0

        super().__init__(pos = pos, 
                        surf = self.frame[self.frame_index], 
                        group = group, 
                        z = LAYERS['water'])

    def animate(self, dt):
        self.frame_index += 5 * dt
        if self.frame_index >= len(self.frame):
             self.frame_index = 0
        self.image = self.frame[int(self.frame_index)]

    def update(self, dt):
        self.animate(dt)

class Wildflower(Generic):
    def __init__(self, pos, surf, group,z = LAYERS['main']):
        super().__init__(pos, surf , group, z)
        self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)

class Tree(Generic):
    def __init__(self, pos, surf, group, z = LAYERS['main'],name = 'Small'):
        super().__init__(pos, surf, group, z)
        #self.hitbox = self.rect.copy().inflate(-20, -self.rect.height * 0.9)

        #tree attributes
        self.tree_health = 5 
        self.alive = True
        stump_path = f'graphics/stumps/{"small" if name == "small" else "large"}.png'
        self.stump_surf = pygame.image.load(stump_path).convert_alpha()
        self.inval_timer = Timer(200)


        #apple 
        self.apple_surf = pygame.image.load('graphics/fruit/apple.png').convert_alpha()
        self.apple_pos = APPLE_POS[name]
        self.apple_sprites = pygame.sprite.Group()
        self.create_fruit()

    def damage(self):
        self.tree_health -= 1

        #remove the apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            random_apple.kill()

    def create_fruit(self):
        for pos in self.apple_pos:
            if randint(0,10) < 2:
                Generic(
                    pos = (self.rect.left + pos[0], self.rect.top + pos[1]),
                    surf = self.apple_surf,
                    group = [self.apple_sprites, self.groups()[0]],
                    z = LAYERS['fruit']
                )


