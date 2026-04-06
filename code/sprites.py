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

class Interaction(Generic):
    def __init__(self, pos, size, group, name ):
        surf = pygame.Surface(size)
        surf.fill('red')
        super().__init__(pos, surf, group)
        self.name = name
    
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

class Particle(Generic):
    def __init__(self, pos, surf, group, z, duration = 200):
        super().__init__(pos, surf, group, z)
        self.duration = duration
        self.start_timer = pygame.time.get_ticks()

        #white surface for the white particles
        mask_surf = pygame.mask.from_surface(self.image)
        white_surf = mask_surf.to_surface()
        white_surf.set_colorkey((0,0,0))
        self.image = white_surf    
    
    def update(self, dt):
        current_time = pygame.time.get_ticks()
        if current_time - self.start_timer >= self.duration:
            self.kill()

class Tree(Generic):
    def __init__(self, pos, surf, group, z = LAYERS['main'],name = 'Small', player_add = None):
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

        self.player_add = player_add

    def damage(self):
        self.tree_health -= 1

        #remove the apple
        if len(self.apple_sprites.sprites()) > 0:
            random_apple = choice(self.apple_sprites.sprites())
            Particle(
                pos = random_apple.rect.topleft,
                surf = random_apple.image,
                group = self.groups()[0],
                z = LAYERS['fruit'])
    
            if self.player_add:
                self.player_add('apple')
            random_apple.kill()
        

    def cheak_death(self):
        if self.tree_health <= 0:
            Particle(
                pos = self.rect.topleft,
                surf = self.image,
                group = self.groups()[0],
                z = LAYERS['fruit'],
                duration = 200
            )
            self.image = self.stump_surf
            self.rect = self.image.get_rect(midbottom = self.rect.midbottom)
            self.hitbox = self.rect.copy().inflate(-10, -self.rect.height * 0.6)
            self.alive = False
            if self.player_add:
                self.player_add('wood')

    def update(self, dt):
        if self.alive:
            self.cheak_death()
        
    def create_fruit(self):
        for pos in self.apple_pos:
            if randint(0,10) < 2:
                Generic(
                    pos = (self.rect.left + pos[0], self.rect.top + pos[1]),
                    surf = self.apple_surf,
                    group = [self.apple_sprites, self.groups()[0]],
                    z = LAYERS['fruit']
                )


