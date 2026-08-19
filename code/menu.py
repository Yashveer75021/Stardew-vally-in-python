import pygame
from setting import * 
from my_timer import Timer

class Menu:
    def __init__(self, player, toggle_menu):
        #genral setup
        self.player = player
        self.toggle_menu = toggle_menu
        self.display_surface = pygame.display.get_surface()
        self.font = pygame.font.Font('font/LycheeSoda.ttf', 30)

        #options
        self.width = 400
        self.space = 10 
        self.padding = 8

        #menu options
        self.menu_options = list(self.player.item_inventory.keys()) + list(self.player.seed_inventory.keys()) 
        self.setup()

        #movement 
        self.index = 0 
        self.timers = Timer(200)


    def show_money(self):
        text_surf = self.font.render(f'$Money : {self.player.money}', False, 'black')
        text_rect = text_surf.get_rect(midbottom = (SCREEN_WIDTH / 2 ,  SCREEN_HEIGHT - 20))
        pygame.draw.rect(self.display_surface, 'white', text_rect.inflate(20, 20), 0, 4)
        self.display_surface.blit(text_surf, text_rect)

    def setup(self):
               
        #text surface
        self.text_surfs = []
        self.total_height = 0
        for option in self.menu_options:
            if option in self.player.item_inventory:
                text = f'{option} : {self.player.item_inventory[option]}'
            elif option in self.player.seed_inventory:
                text = f'{option} : {self.player.seed_inventory[option]}'
            text_surf = self.font.render(text, False, 'black')
            self.text_surfs.append(text_surf) 
            self.total_height += text_surf.get_height() + (self.padding * 2)
  
        self.total_height += (len(self.text_surfs) - 1) * self.space
        self.menu_top = SCREEN_HEIGHT / 2 - self.total_height / 2
        self.main_rect = pygame.Rect(self.display_surface.get_size()[0] - self.width, self.menu_top - self.padding, self.width, self.total_height)


        self.buy_text = self.font.render('Buy', False, 'black')
        self.sell_text = self.font.render('Sell', False, 'black')

    def input(self):
        keys = pygame.key.get_pressed()
        self.timers.update()
        if keys[pygame.K_ESCAPE]:
            self.toggle_menu()
        if not self.timers.active:
            if keys[pygame.K_UP] and self.index > 0:
                self.index -= 1
                self.timers.activate()
            if keys[pygame.K_DOWN] and self.index < len(self.text_surfs) - 1:
                self.index += 1
                self.timers.activate()
            if keys[pygame.K_SPACE]:
                self.timers.activate()

                #get item 
                current_item = self.menu_options[self.index]

                #sell]

                #buy


    def show_entry(self, text_surf, amount, top, selected):
        #background
        bg_rect = pygame.Rect(self.main_rect.left, top, self.width, text_surf.get_height() + (self.padding * 2))
        pygame.draw.rect(self.display_surface, 'white', bg_rect, 0, 4)
        
        #text 
        text_rect = text_surf.get_rect(midleft = (self.main_rect.left + self.padding, bg_rect.centery))
        self.display_surface.blit(text_surf, text_rect)

        #amount
        amount_surf = self.font.render(str(amount), False, 'black')
        amount_rect = amount_surf.get_rect(midright = (self.main_rect.right - self.padding, bg_rect.centery))
        self.display_surface.blit(amount_surf, amount_rect)

        #selected
        if selected:
            pygame.draw.rect(self.display_surface, 'black', bg_rect, 4, 4)
            if self.menu_options[self.index] in self.player.item_inventory:
                action_text = self.sell_text
            else:
                action_text = self.buy_text
            action_rect = action_text.get_rect(midright = (self.main_rect.right - 150, bg_rect.centery))
            self.display_surface.blit(action_text, action_rect)


    def update(self):
        self.input()
        self.show_money()
        for index, text_surf in enumerate(self.text_surfs):
            top = self.menu_top + index * (text_surf.get_height() + (self.padding * 2) + self.space)
            amount_list = list(self.player.item_inventory.values()) + list(self.player.seed_inventory.values())
            amount = amount_list[index]
            self.show_entry(text_surf, amount, top, self.index == index)