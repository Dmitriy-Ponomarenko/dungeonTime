import pygame
import sys
from os.path import join
from setup_settings.level import Level
from setup_settings.settings import *
from pytmx.util_pygame import load_pygame

class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption('dungeonTime')
        self.clock = pygame.time.Clock()

        self.tmx_maps = {0: load_pygame(join('src', 'data', 'levels', 'simple_terrain_map.tmx'))}

        self.current_stage = Level(self.tmx_maps[0])

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            dt = self.clock.tick(60) / 1000.0
            self.current_stage.run(dt)

            pygame.display.update()

if __name__ == "__main__":
    game = Game()
    game.run()