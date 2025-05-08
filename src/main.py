# dungeon_game/src/main.py

import pygame
from characters.character import Character
from characters.enemy import Enemy
# from quests.quests import Quest
from maps.layout import MapLayout

class DungeonGame:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Dungeon Time")
        self.clock = pygame.time.Clock()
        self.running = True
        self.player = Character("Hero", 100)
        self.enemy = Enemy("Goblin", 50, 10)
        self.quest = Quest("Find the Treasure", "Locate the hidden treasure in the dungeon.")
        self.map_layout = MapLayout()

    def main_loop(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def update(self):
        pass

    def draw(self):
        self.screen.fill((0, 0, 0)) 
        self.map_layout.display(self.screen) 
        pygame.display.flip()

if __name__ == "__main__":
    game = DungeonGame()
    game.main_loop()
    pygame.quit()