import pygame
from setting import *
from player import Player
from overlay import Overlay 
from sprites import Generic, Water, Wildflower, Tree, Interaction, Particle
from pytmx.util_pygame import load_pygame
from support import *
from transition import Transition
from soil import SoilLayer
from sky import Rain, Sky
from random import randint

class Level:
    def __init__(self):
        #getting the display surface
        self.display_surface = pygame.display.get_surface()


        #sprite group setup
        self.all_sprites = CameraGroup()
        self.collision_sprites = pygame.sprite.Group()
        self.tree_sprites = pygame.sprite.Group()  
        self.intraction_sprites = pygame.sprite.Group() 

        self.soil_layer = SoilLayer(self.all_sprites, self.collision_sprites)
        self.setup()
        self.overlay = Overlay(self.player)
        self.transition = Transition(self.reset, self.player)
        
        #sky 
        self.rain = Rain(self.all_sprites)
        self.raining = randint(0,10) > 7 
        self.soil_layer.raining = self.raining  
        self.sky = Sky()

    def setup(self):
        tmx_data = load_pygame('data/map.tmx')
        #import the house
        for layer in ['HouseFloor', 'HouseFurnitureBottom']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic(
                    pos = (x * TILE_SIZE, y * TILE_SIZE),
                    surf = surf,
                    group = self.all_sprites,
                    z = LAYERS['house bottom']
                )

        for layer in ['HouseWalls', 'HouseFurnitureTop']:
            for x, y, surf in tmx_data.get_layer_by_name(layer).tiles():
                Generic(
                    pos = (x * TILE_SIZE, y * TILE_SIZE),
                    surf = surf,
                    group = self.all_sprites,
                    z = LAYERS['main']
                )

        #import the fence
        for x, y, surf in tmx_data.get_layer_by_name('Fence').tiles():
            Generic(
                pos = (x * TILE_SIZE, y * TILE_SIZE),
                surf = surf,
                group = [self.all_sprites, self.collision_sprites],
                z = LAYERS['main']
            )

        #import the water
        water_frames = import_folder('graphics/water')
        for x, y, surf in tmx_data.get_layer_by_name('Water').tiles():
            Water(
                pos = (x * TILE_SIZE, y * TILE_SIZE),
                frames = water_frames,
                group = self.all_sprites
            )
            
        #import the trees    
        for obj in tmx_data.get_layer_by_name('Trees'):
            Tree(
                pos = (obj.x, obj.y),
                surf = obj.image,
                group = [self.all_sprites, self.collision_sprites, self.tree_sprites],
                player_add = self.player_add 
            )

        #import the wildfowers
        for obj in tmx_data.get_layer_by_name('Decoration'):
            Wildflower(
                pos = (obj.x, obj.y),
                surf = obj.image,
                group = [self.all_sprites, self.collision_sprites]
            )

        #collision tiles
        for x, y, surf in tmx_data.get_layer_by_name('Collision').tiles():
            Generic(
                pos = (x * TILE_SIZE, y * TILE_SIZE),
                surf = pygame.Surface((TILE_SIZE, TILE_SIZE)),
                group =  self.collision_sprites
            )

        #Player
        for obj in tmx_data.get_layer_by_name('Player'):
            if obj.name == 'Start':
                self.player = Player(
                    pos = (obj.x, obj.y),
                    groups = self.all_sprites,
                    collision_sprites = self.collision_sprites,
                    tree_stripes = self.tree_sprites,
                    interaction_sprites = self.intraction_sprites,
                    soil_layer = self.soil_layer
                )
            if obj.name == 'Bed':
                Interaction(
                    pos = (obj.x, obj.y),
                    size = (obj.width, obj.height),
                    group = self.intraction_sprites,
                    name = 'Bed'
                ) 

        Generic(
            pos = (0,0),
            surf = pygame.image.load('graphics/world/ground.png').convert_alpha(),
            group = self.all_sprites,
            z = LAYERS['ground']
        )

    def player_add(self,item):
        self.player.item_inventory[item] += 1

    def run(self, dt):
        self.display_surface.fill('black') 
        self.all_sprites.custom_draw(self.player)
        self.all_sprites.update(dt)

        #rain 
        if self.raining:
            self.rain.update()

        #sky 
        self.sky.display(dt)

        self.overlay.display()
        if self.player.sleep:
            self.transition.fade()

        #plant colliosion
        self.plant_collosion()

    def reset(self):
        #plant
        self.soil_layer.update_plant()

        #apple on tree
        for tree in self.tree_sprites.sprites():
            for apple in tree.apple_sprites.sprites():
                apple.kill()
            if tree.alive:
                tree.create_fruit()
        
        #remove water
        self.soil_layer.remove_water() 
        self.raining = randint(0,10) > 7 
        self.soil_layer.raining = self.raining
        if self.raining:
            self.soil_layer.water_all()

        #sky 
        self.sky.start_color = self.sky.end_color.copy()
        
        
    def plant_collosion(self):
        if self.soil_layer.plant_sprites:
            for plant in self.soil_layer.plant_sprites:
                if plant.harvesteble and plant.rect.colliderect(self.player.hitbox):
                    self.player.item_inventory[plant.plant_type] += 1
                    plant.kill()
                    Particle(
                        pos = plant.rect.topleft,
                        surf = plant.image,
                        groups = self.all_sprites,
                        z = LAYERS['main']
                    )
                    self.soil_layer.soil_grid[plant.rect.centery // TILE_SIZE][plant.rect.centerx // TILE_SIZE].remove('P')
                    

class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()
        self.display_surface = pygame.display.get_surface() 
        self.offset = pygame.math.Vector2()

    def custom_draw(self, player):
        self.offset.x = player.rect.centerx - SCREEN_WIDTH / 2
        self.offset.y = player.rect.centery - SCREEN_HEIGHT / 2

        for layer in LAYERS.values():
            for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
                if sprite.z == layer:
                    offset_rect = sprite.rect.copy()
                    offset_rect.center -= self.offset
                    self.display_surface.blit(sprite.image, offset_rect)

                    #analics
                    # if sprite == player:
                    #     pygame.draw.rect(self.display_surface, 'red', offset_rect, 5)
                    #     hitbox_offset = sprite.hitbox.copy()
                    #     hitbox_offset.center = offset_rect.center 
                    #     pygame.draw.rect(self.display_surface, 'green', hitbox_offset, 5)
                    #     taget_pos = offset_rect.center + PLAYER_TOOL_OFFEST[player.status.split('_')[0]]
                    #     pygame.draw.circle(self.display_surface, 'blue', taget_pos, 5)
 