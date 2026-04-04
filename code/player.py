import pygame 
from setting import *
from support import *
from my_timer import Timer

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

        #timers
        self.timers = {
            'tool use' : Timer(350, self.tool_use),
            'tool_switch' : Timer(200)
        }

        #tool use
        self.tools = ['hoe', 'axe', 'water']
        self.tool_index = 0
        self.selected_tool = self.tools[self.tool_index]

    def tool_use(self):
        #self.timers['tool use'].activate()
        print(self.selected_tool)


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

    def animate(self, dt):
        self.frame_index += 4 * dt
        if self.frame_index >= len(self.animation[self.status]):
            self.frame_index = 0
        self.image = self.animation[self.status][int(self.frame_index)]

    def input(self):
        keys = pygame.key.get_pressed()
        if not self.timers['tool use'].active:
            if keys[pygame.K_w]:
                self.direction.y = -1
                self.status = 'up'
            elif keys[pygame.K_s]:
                self.direction.y = 1
                self.status = 'down'
            else:
                self.direction.y = 0

            if keys[pygame.K_a]:
                self.direction.x = -1
                self.status = 'left'
            elif keys[pygame.K_d]:
                self.direction.x = 1
                self.status = 'right'
            else:
                self.direction.x = 0

            # tool use on key press (edge), not while holding
            if keys[pygame.K_SPACE]:
                self.timers['tool use'].activate()
                self.direction = pygame.math.Vector2()
                self.frame_index = 0

            #switch tools
            if keys[pygame.K_1] and not self.timers['tool_switch'].active:
                self.timers['tool_switch'].activate()
                self.tool_index += 1
                self.tool_index = self.tool_index if self.tool_index < len(self.tools) else 0
                self.selected_tool = self.tools[self.tool_index]
                



    def update_timers(self):
        for ti in self.timers.values():
            ti.update()

    def status_update(self):
        #movement status
        if self.direction.magnitude() == 0:
            self.status = self.status.split('_')[0] + '_idle'
        #tool use status
        if self.timers['tool use'].active:
            self.status = self.status.split('_')[0] + '_' + self.selected_tool 

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
        self.update_timers()
        self.status_update()

        self.move(dt)
        self.animate(dt)
        