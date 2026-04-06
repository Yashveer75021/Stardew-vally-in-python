import pygame
from setting import * 
from support import * 
from pytmx.util_pygame import load_pygame

class SoilTiles(pygame.sprite.Sprite):
    def __init__(self,pos, surf, groups):
        super().__init__(groups)
        self.image = surf
        self.rect = self.image.get_rect(topleft = pos)
        self.z = LAYERS["soil"]

class SoilLayer():
    def __init__(self,all_sprites):
        #sprite groups 
        self.all_sprites = all_sprites
        self.soil_sprites = pygame.sprite.Group()

        #graphic
        self.soil_surf = pygame.image.load("graphics/soil/o.png")
        self.soil_surfs = import_folder_dict("graphics/soil")
        

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
                x = rect.x // TILE_SIZE
                y = rect.y // TILE_SIZE
                if "F" in self.soil_grid[y][x]:
                    self.soil_grid[y][x].append("X")
                    self.crate_soil_tiles()

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
    


