import pygame
from setting import *
from support import import_folder
from sprites import Generic
from random import randint, choice

class Sky:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.full_surf = pygame.Surface((SCREEN_WIDTH,SCREEN_HEIGHT))
        self.start_color = [255,255,255]
        self.end_color = (38,101,189)
    
    def display(self,dt):
        for index, value in enumerate(self.end_color):
            if self.start_color[index] > value:
                self.start_color[index] -= 10 * dt
                self.start_color[index] = max(self.start_color[index], value)

            #color transition
        self.full_surf.fill(self.start_color)
        self.display_surface.blit(self.full_surf,(0,0), special_flags=pygame.BLEND_RGBA_MULT)
        

class Drop(Generic):
    def __init__(self,pos,surf,groups, moving, z = LAYERS["rain drops"]):
        #general setup
        super().__init__(pos,surf,groups,z)
        self.lifetime = randint(400,500)
        self.start_time = pygame.time.get_ticks()
        
        # moving part 
        self.moving = moving
        if self.moving:
            self.pos = pygame.math.Vector2(self.rect.topleft)
            self.direction = pygame.math.Vector2(-2,4)
            self.speed = randint(200,250)
    def update(self,dt):
        #movemint
        if self.moving:
            self.pos += self.direction * self.speed * dt
            self.rect.topleft = ((round(self.pos.x),round(self.pos.y)))

        #timer   
        if pygame.time.get_ticks() - self.start_time >= self.lifetime: 
            self.kill() 
 
class Rain():
    def __init__(self,all_sprites):
        self.all_sprites = all_sprites
        self.rain_drop = import_folder('graphics/rain/drops')
        self.rain_floor = import_folder('graphics/rain/floor')
        self.rain_floor_w , self.rain_floor_h = pygame.image.load('graphics/world/ground.png').get_size()


    def create_floor(self):
        Drop(
            pos = (randint(0,self.rain_floor_w),randint(0,self.rain_floor_h)),
            surf = choice(self.rain_floor),
            groups = [self.all_sprites],
            moving = False,
            z = LAYERS["rain floor"]    
        ) 

    def create_raindrop(self):
        Drop(
            pos = (randint(0,self.rain_floor_w),randint(0,self.rain_floor_h)),
            surf = choice(self.rain_drop),
            groups = [self.all_sprites],
            moving = True,
            z = LAYERS["rain drops"] 
        )
        # for tile_x in range(self.floor_w // TILE_SIZE):
        #     for tile_y in range(self.rain_floor_h // TILE_SIZE):
        #         Raindrop(pos = (tile_x * TILE_SIZE, tile_y * TILE_SIZE), surf = choice(self.rain_drop), groups = [self.all_sprites])    

    def update(self):
        self.create_floor()
        self.create_raindrop()