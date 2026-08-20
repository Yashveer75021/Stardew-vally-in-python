import pygame
from setting import * 
from support import * 
from pytmx.util_pygame import load_pygame
from random import choice

class SoilTiles(pygame.sprite.Sprite):
    def __init__(self,pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS["soil"]

class WaterTile(pygame.sprite.Sprite):
    def __init__(self,pos,surf,groups, z = LAYERS["soil water"]):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = z

class Plant(pygame.sprite.Sprite,):
    def __init__(self,plant_type, groups, soil, cheak_waterd, z = LAYERS['ground plant']):
        super().__init__(groups)
        self.plant_type = plant_type
        self.soil = soil
        self.cheak_waterd = cheak_waterd
        self.z = z
        
        #plant graphic
        self.frames = import_folder(f"graphics/fruit/{plant_type}")
        
        #plant growing
        self.age = 0
        self.max_age = len(self.frames) - 1 
        self.grow_speed = GROWTH_SPEED[plant_type]
        self.harvesteble = False 
        
        # sprite group 
        self.image = self.frames[self.age]
        self.y_offset = -16 if plant_type == 'corn' else -8
        self.rect = self.image.get_rect(midbottom = soil.rect.midbottom + pygame.math.Vector2(0,self.y_offset))

    def grow(self):
        if self.cheak_waterd(self.rect.center):
            self.age += self.grow_speed
            if int(self.age) > 0:
                self.hitbox = self.rect.copy().inflate(-26, -self.rect.height* 0.4)
                self.z = LAYERS['main']
            if self.age >= self.max_age:
                self.age = self.max_age
                self.harvesteble = True    

            
            self.image = self.frames[int(self.age)] 
            self.rect = self.image.get_rect(midbottom = self.soil.rect.midbottom + pygame.math.Vector2(0,self.y_offset))

class SoilLayer():
    def __init__(self,all_sprites, collision_sprites):
        #sprite groups 
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()
        self.water_sprites = pygame.sprite.Group()  
        self.plant_sprites = pygame.sprite.Group()
        self.collision_sprites = collision_sprites

        #graphic
        self.soil_surf = pygame.image.load("graphics/soil/o.png")
        self.soil_surfs = import_folder_dict("graphics/soil")
        self.water_surf = import_folder("graphics/soil_water")

        #sound 
        self.hoe_sound = pygame.mixer.Sound('audio/hoe.wav')
        self.hoe_sound.set_volume(0.2)

        self.crate_soil_grid()
        self.crate_hit_rects()
        
    def crate_soil_grid(self):
        ground = pygame.image.load("graphics/world/ground.png")
        h_tiles, v_tiles = ground.get_width() // TILE_SIZE, ground.get_height() // TILE_SIZE

        self.soil_grid = [[[] for col in range(h_tiles)] for row in range(v_tiles)]
        for x, y, _ in load_pygame("data/map.tmx").get_layer_by_name("Farmable").tiles():
            self.soil_grid[y][x].append("F")
    
    def crate_hit_rects(self):
        self.hit_rects = []
        for index_row, row in enumerate(self.soil_grid):
            for index_col, col in enumerate(row):
                x = index_col * TILE_SIZE
                y = index_row * TILE_SIZE
                rect = pygame.Rect(x,y,TILE_SIZE,TILE_SIZE)
                self.hit_rects.append(rect)

    def get_hit(self,point):
        for rect in self.hit_rects:
            if rect.collidepoint(point):
                self.hoe_sound.play()   
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE
                if "F" in self.soil_grid[y][x]:
                    self.soil_grid[y][x].append("X")
                    self.crate_soil_tiles()
                    if self.raining:
                        self.water_all()

    def water(self, targe_pos):
        for soil_sprite in self.soil_sprites:
            if soil_sprite.rect.collidepoint(targe_pos):
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                self.soil_grid[y][x].append("W")
                self.crate_soil_tiles()
                WaterTile(
                    pos = (x * TILE_SIZE, y * TILE_SIZE),
                    surf = choice(self.water_surf),
                    groups = [self.all_sprites, self.water_sprites],
                    z = LAYERS["soil water"]
                )   
    
    def water_all(self):
        for index_row, row in enumerate(self.soil_grid):
            for index_col, col in enumerate(row):
                if 'X' in col and 'W' not in col: 
                    self.soil_grid[index_row][index_col].append('W')
                    # self.crate_soil_tiles() 
                    WaterTile(
                        pos = (index_col * TILE_SIZE, index_row * TILE_SIZE),
                        surf = choice(self.water_surf),
                        groups = [self.all_sprites, self.water_sprites],
                        z = LAYERS['soil water']
                    )   

    def remove_water(self):
        for sprite in self.water_sprites:
            sprite.kill()
        for row in self.soil_grid:
            for cell in row:
                if 'W' in cell:
                    cell.remove('W')
 
    def cheak_waterd(self,pos):
        x = pos[0] // TILE_SIZE
        y = pos[1] // TILE_SIZE
        cell = self.soil_grid[y][x]
        if 'W' in cell:
            return True
        return False

    def plant_seed(self,target_pos, seed):
        for soil_sprite in self.soil_sprites:
            if soil_sprite.rect.collidepoint(target_pos):
                x = soil_sprite.rect.x // TILE_SIZE
                y = soil_sprite.rect.y // TILE_SIZE
                if 'P' not in self.soil_grid[y][x]:
                    self.soil_grid[y][x].append('P')
                    Plant(
                        plant_type = seed,
                        groups = [self.all_sprites, self.plant_sprites, self.collision_sprites],
                        soil = soil_sprite,
                        cheak_waterd = self.cheak_waterd,
                        z = LAYERS['ground plant']
                    )
                
    def update_plant(self):
        for plant in self.plant_sprites.sprites():
            plant.grow()

    def crate_soil_tiles(self):
        self.soil_sprites.empty()
        for index_row, row in enumerate(self.soil_grid):
            for index_col, col in enumerate(row):
                if 'X' in col:

                    #tile option
                    t = 'X' in self.soil_grid[index_row - 1][index_col]
                    b = 'X' in self.soil_grid[index_row + 1][index_col]
                    r = "X" in row[index_col + 1]
                    l = "X" in row[index_col - 1]

                    tile_type = 'o'
                    # tile to print
                    # all sides
                    if all((t,b,l,b)):
                        tile_type = 'x'

                    # horizontal tile system 
                    if r and not any((t,l,b)):
                        tile_type = 'l'
                    if l and not any((t,r,b)):
                        tile_type = "r"
                    if l and r and not any((t,b)):
                        tile_type = 'lr'

                    # vertical tile system 
                    if t and not any((r,l,b)):
                        tile_type = "b"                        
                    if b and not any((r,l,t)):
                        tile_type = "t"                        
                    if t and b and not any((r,l)):
                        tile_type = "tb"                        
                    
                    # cornes 
                    if l and b and not any((r,t)):
                        tile_type = "tr" 
                    if r and b and not any((l,t)):
                        tile_type = "tl" 
                    if l and t and not any((b,r)):
                        tile_type = "br" 
                    if r and t and not any((l,b)):
                        tile_type = "bl" 

                    # t-shape
                    if all((t,b,r)) and not l:
                        tile_type = "tbr"                
                    if all((t,b,l)) and not r:
                        tile_type = "tbl"                
                    if all((l,r,t)) and not b:
                        tile_type = "lrb"                
                    if all((l,r,b)) and not t:
                        tile_type = "lrt"                



                    SoilTiles(
                        pos = (index_col * TILE_SIZE, index_row * TILE_SIZE),
                        surf = self.soil_surfs[tile_type],
                        groups = [self.all_sprites, self.soil_sprites]
                    )
    

