import pygame
from .settings import *

class DungeonMenu:
    def __init__(self, display_surface, run_dungeon_func):
        self.display_surface = display_surface
        self.font = pygame.font.SysFont("georgia", 20, bold=True)
        self.run_dungeon = run_dungeon_func
        self.player_health = 100  # Initial HP
        self.enemy_health = 0
        self.text_lines = []
        self.input_text = ""
        self.game_over = False
        self.running = True
        self.player_inventory = []  # Initialize inventory
        self.player_stats = {"strength": 0}  # Initialize stats

    def add_text(self, text):
        self.text_lines.append(text)
        if len(self.text_lines) > 10:  # Limit to 10 lines
            self.text_lines.pop(0)

    def choose(self, options):
        """Display choices and return the selected index."""
        self.add_text("Choose an action:")
        while True:
            self.render(options=options)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    return -1
                if event.type == pygame.KEYDOWN:
                    for i in range(min(4, len(options))):
                        if event.key == getattr(pygame, f'K_{i+1}'):
                            return i
            pygame.time.wait(100)  # Small delay to prevent spam

    def fight(self, enemy_name, enemy_hp, player_action=None):
        self.add_text(f"You encounter a {enemy_name} with {enemy_hp} HP!")
        self.enemy_health = enemy_hp
        player_attack = 20
        if player_action == "strong":
            player_attack = 30
        elif player_action == "dodge":
            player_attack = 15
            self.player_health += 5  # Minor heal from dodging
        elif player_action == "special":
            player_attack = 25
            self.player_health -= 5  # Cost for special
        elif player_action == "quick":
            player_attack = 15
        elif player_action == "group":
            player_attack = 10  # Reduced for group
        elif player_action == "boss":
            player_attack = 20

        while self.enemy_health > 0 and self.player_health > 0:
            self.enemy_health -= player_attack
            self.add_text(f"You deal {player_attack} damage. {enemy_name} has {max(0, self.enemy_health)} HP left.")
            if self.enemy_health > 0:
                enemy_attack = 10
                if player_action == "group":
                    enemy_attack = 15  # Increased for group
                elif player_action == "boss":
                    enemy_attack = 20  # Increased for boss
                self.player_health -= enemy_attack
                self.add_text(f"The {enemy_name} deals {enemy_attack} damage. You have {max(0, self.player_health)} HP left.")
            pygame.time.wait(500)  # Pause for readability
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # Quit fight
                    self.add_text("You fled the fight!")
                    return
        if self.player_health <= 0:
            self.add_text("You have been defeated! Game Over.")
            self.game_over = True
        else:
            self.add_text(f"You defeated the {enemy_name}!")

    def run(self):
        if self.run_dungeon:
            self.run_dungeon(self)  # Pass self so the dungeon can use the menu
        while self.running:
            self.render()
            pygame.display.update()
            for event in pygame.event.get():
                self.handle_event(event)

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not self.game_over:
                self.running = False
            elif event.key == pygame.K_q:
                self.running = False

    def render(self, options=None):
        self.display_surface.fill((0, 0, 0))
        y_offset = 20
        for line in self.text_lines:
            text_surf = self.font.render(line, True, (255, 255, 255))
            self.display_surface.blit(text_surf, (20, y_offset))
            y_offset += 30
        if options:
            for idx, opt in enumerate(options):
                opt_surf = self.font.render(f"{idx+1}. {opt}", True, (180, 220, 255))
                self.display_surface.blit(opt_surf, (40, y_offset))
                y_offset += 28
        if not self.game_over:
            prompt = self.font.render(
                "Press ENTER to continue or Q to quit", True, (255, 255, 255)
            )
            self.display_surface.blit(prompt, (20, y_offset))
        else:
            game_over = self.font.render(
                "Game Over! Press Q to quit", True, (255, 0, 0)
            )
            self.display_surface.blit(game_over, (20, y_offset))