import pygame, sys 
from setting import *

class Game:
    def __int__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT  ))
        self.clock = pygame.time.Clock()
    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            dt = self.clock.tick(60) / 1000
            pygame.display.update()


if __name__ == '__main__':
    game = Game()
    game.run()
    
            