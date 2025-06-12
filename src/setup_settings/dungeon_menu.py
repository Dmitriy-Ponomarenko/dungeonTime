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

    def add_text(self, text):
        self.text_lines.append(text)
        if len(self.text_lines) > 10:  # Limit to 10 lines
            self.text_lines.pop(0)

    def fight(self, enemy_name, enemy_hp):
        self.add_text(f"You encounter a {enemy_name} with {enemy_hp} HP!")
        self.enemy_health = enemy_hp
        player_attack = 20  # Fixed player attack power
        while self.enemy_health > 0 and self.player_health > 0:
            self.enemy_health -= player_attack
            self.add_text(
                f"You deal {player_attack} damage. {enemy_name} has {max(0, self.enemy_health)} HP left."
            )
            if self.enemy_health > 0:
                enemy_attack = 10  # Fixed enemy attack power
                self.player_health -= enemy_attack
                self.add_text(
                    f"The {enemy_name} deals {enemy_attack} damage. You have {max(0, self.player_health)} HP left."
                )
            pygame.time.wait(500)  # Pause for readability
            self.render()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_q
                ):  # Quit fight
                    self.add_text("You fled the fight!")
                    return
        if self.player_health <= 0:
            self.add_text("You have been defeated! Game Over.")
            self.game_over = True
        else:
            self.add_text(f"You defeated the {enemy_name}!")

    def run(self):
        self.add_text("You enter the dungeon...")
        self.add_text("Thoughts: The air feels heavy, danger lurks ahead.")
        self.add_text("Event: You find a rusty sword (+5 attack next fight).")

        # Example dungeon events (customize per dungeon file)
        self.fight("Skeleton", 50)
        if not self.game_over:
            self.add_text("Teammate: 'Good job, let’s move on!'")
            self.add_text("Thoughts: I feel stronger now.")
            self.fight("Skeleton Warrior", 70)

        if not self.game_over:
            self.add_text("You reach the dungeon exit.")
        else:
            self.add_text("You are ejected from the dungeon.")

        while self.running:
            self.render()
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and not self.game_over:
                        self.running = False
                    elif event.key == pygame.K_q:
                        self.running = False

    def handle_event(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and not self.game_over:
                self.running = False
            elif event.key == pygame.K_q:
                self.running = False

    def render(self):
        self.display_surface.fill((0, 0, 0))  # Black background for text menu
        y_offset = 20
        for line in self.text_lines:
            text_surf = self.font.render(line, True, (255, 255, 255))
            self.display_surface.blit(text_surf, (20, y_offset))
            y_offset += 30
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
