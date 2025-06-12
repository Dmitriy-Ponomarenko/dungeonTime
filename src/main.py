import pygame
import sys
from os.path import join
from setup_settings.level import Level
from setup_settings.settings import *
from pytmx.util_pygame import load_pygame
from setup_settings.menu import StartMenu, LanguageMenu, NameMenu
import glob


class Game:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("dungeonTime")
        self.clock = pygame.time.Clock()
        self.state = "start_menu"
        self.language = "en"
        self.player_name = ""
        self.player_health = 100

        self.start_menu = StartMenu(
            self.display_surface,
            start_callback=self.open_language_menu,
            exit_callback=self.exit_game,
        )
        self.language_menu = LanguageMenu(
            self.display_surface,
            start_callback=self.open_name_menu,
            back_callback=self.open_start_menu,
        )
        self.name_menu = NameMenu(
            self.display_surface,
            start_callback=self.start_game,
            back_callback=self.open_language_menu,
        )
        self.tmx_maps = None
        self.current_stage = None

        self.loading_frames = [
            pygame.image.load(f).convert_alpha()
            for f in sorted(glob.glob("src/data/loading/loading_*.png"))
        ]
        if not self.loading_frames:
            surf = pygame.Surface((64, 64), pygame.SRCALPHA)
            pygame.draw.circle(surf, (180, 140, 80), (32, 32), 28)
            pygame.draw.circle(surf, (60, 40, 20), (32, 32), 24)
            self.loading_frames = [surf]

    def open_language_menu(self):
        self.state = "language_menu"

    def open_start_menu(self):
        self.state = "start_menu"

    def open_name_menu(self, language):
        self.language = language
        self.state = "name_menu"

    def start_game(self, name):
        self.player_name = name if name else "Hero"
        self.tmx_maps = {0: load_pygame(join("src", "data", "levels", "main_map1.tmx"))}
        self.current_stage = Level(
            self.tmx_maps[0], self.player_name, self.player_health
        )
        self.state = "game"

    def exit_game(self):
        pygame.quit()
        sys.exit()

    def draw_hud(self):
        hud_surf = pygame.Surface((320, 80), pygame.SRCALPHA)
        pygame.draw.rect(
            hud_surf, (60, 40, 20, 220), hud_surf.get_rect(), border_radius=16
        )
        pygame.draw.rect(
            hud_surf, (180, 140, 80, 255), hud_surf.get_rect(), 4, border_radius=16
        )
        font = pygame.font.SysFont("georgia", 24, bold=True)
        name_surf = font.render(f"Name: {self.player_name}", True, (255, 230, 180))
        health_surf = font.render(f"Health: {self.player_health}", True, (255, 80, 80))
        hud_surf.blit(name_surf, (16, 10))
        hud_surf.blit(health_surf, (16, 44))
        self.display_surface.blit(hud_surf, (16, 16))

    def draw_menu_box(self, menu_rect):
        s2 = pygame.Surface(menu_rect.size, pygame.SRCALPHA)
        pygame.draw.rect(s2, (180, 140, 80, 255), s2.get_rect(), border_radius=24)
        inner_rect = s2.get_rect().inflate(-12, -12)
        pygame.draw.rect(s2, (60, 40, 20, 230), inner_rect, border_radius=18)
        self.display_surface.blit(s2, menu_rect.topleft)

    def run(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_game()
                if self.state == "start_menu":
                    self.start_menu.handle_event(event)
                elif self.state == "language_menu":
                    self.language_menu.handle_event(event)
                elif self.state == "name_menu":
                    self.name_menu.handle_event(event)
                elif self.state == "game":
                    pass

            dt = self.clock.tick(120) / 1000.0

            if self.state == "start_menu":
                self.start_menu.draw()
            elif self.state == "language_menu":
                self.language_menu.draw()
            elif self.state == "name_menu":
                self.name_menu.draw()
            elif self.state == "game":
                self.current_stage.run(dt)
                self.draw_hud()

            pygame.display.update()


if __name__ == "__main__":
    game = Game()
    game.run()
