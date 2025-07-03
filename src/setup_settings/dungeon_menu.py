import pygame
from .settings import *

class DungeonMenu:
    def __init__(self, display_surface, run_dungeon_func):
        self.display_surface = display_surface
        self.font = pygame.font.SysFont("georgia", 20, bold=True)
        self.run_dungeon = run_dungeon_func
        self.player_health = 100  # Initial HP
        self.enemy_health = 0
        self.text_lines = []  # Queue of text lines to display
        self.displayed_lines = []  # Currently visible lines
        self.current_text = ""  # Text being typed
        self.char_index = 0  # Current character index for typing
        self.current_line_index = 0  # Index of the line being processed
        self.typing_speed = 0.05  # Seconds per character
        self.line_delay = 0.5  # Seconds between lines
        self.typing_timer = 0
        self.line_timer = 0
        self.waiting_for_input = False
        self.input_text = ""
        self.game_over = False
        self.running = True
        self.player_inventory = []  # Initialize inventory
        self.player_stats = {"strength": 0}  # Initialize stats

    def add_text(self, text):
        """Add a text line to the queue."""
        self.text_lines.append(text)
        if len(self.text_lines) > 10:  # Limit to 10 lines
            self.text_lines.pop(0)

    def choose(self, options):
        """Display choices and return the selected index."""
        self.add_text("Choose an action:")
        self.waiting_for_input = True
        while self.waiting_for_input and self.running:
            self.update_text_animation(0.016)  # Update animation (~60 FPS)
            self.render(options=options)
            pygame.display.update()
            for event in pygame.event.get():
                if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                    self.running = False
                    return -1
                if event.type == pygame.KEYDOWN and self.is_text_fully_displayed():
                    for i in range(min(4, len(options))):
                        if event.key == getattr(pygame, f'K_{i+1}'):
                            self.waiting_for_input = False
                            return i
            pygame.time.wait(16)  # ~60 FPS
        return -1

    def fight(self, enemy_name, enemy_hp, player_action=None):
        """Handle combat with text and quit option."""
        self.add_text(f"You encounter a {enemy_name} with {enemy_hp} HP!")
        self.enemy_health = enemy_hp
        player_attack = 20
        if player_action == "strong":
            player_attack = 30
        elif player_action == "dodge":
            player_attack = 15
            self.player_health += 5
        elif player_action == "special":
            player_attack = 25
            self.player_health -= 5
        elif player_action == "quick":
            player_attack = 15
        elif player_action == "group":
            player_attack = 10
        elif player_action == "boss":
            player_attack = 20

        while self.enemy_health > 0 and self.player_health > 0 and self.running:
            self.enemy_health -= player_attack
            self.add_text(f"You deal {player_attack} damage. {enemy_name} has {max(0, self.enemy_health)} HP left.")
            if self.enemy_health > 0:
                enemy_attack = 10
                if player_action == "group":
                    enemy_attack = 15
                elif player_action == "boss":
                    enemy_attack = 20
                self.player_health -= enemy_attack
                self.add_text(f"The {enemy_name} deals {enemy_attack} damage. You have {max(0, self.player_health)} HP left.")
            while not self.is_text_fully_displayed() and self.running:
                self.update_text_animation(0.016)
                self.render()
                pygame.display.update()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
                        self.running = False
                        return
                pygame.time.wait(16)
            if self.running:
                pygame.time.wait(500)  # Pause for readability
        if self.player_health <= 0:
            self.add_text("You have been defeated! Game Over.")
            self.game_over = True
        else:
            self.add_text(f"You defeated the {enemy_name}!")

    def is_text_fully_displayed(self):
        """Check if all text lines are fully displayed."""
        return (self.current_line_index >= len(self.text_lines) and 
                self.char_index >= len(self.current_text))

    def update_text_animation(self, dt):
        """Update the typing animation."""
        if self.current_line_index >= len(self.text_lines):
            return

        # Start a new line if current text is empty
        if not self.current_text:
            self.current_text = self.text_lines[self.current_line_index]
            self.char_index = 0
            self.typing_timer = 0
            self.line_timer = 0
            self.displayed_lines.append("")

        # Type out characters
        self.typing_timer += dt
        if self.typing_timer >= self.typing_speed and self.char_index < len(self.current_text):
            self.displayed_lines[-1] = self.current_text[:self.char_index + 1]
            self.char_index += 1
            self.typing_timer = 0

        # Move to next line after delay
        if self.char_index >= len(self.current_text):
            self.line_timer += dt
            if self.line_timer >= self.line_delay:
                self.current_line_index += 1
                self.current_text = ""
                if self.current_line_index < len(self.text_lines):
                    self.displayed_lines.append("")
                if len(self.displayed_lines) > 10:
                    self.displayed_lines.pop(0)

    def run(self):
        """Run the dungeon with animated text."""
        if self.run_dungeon:
            self.run_dungeon(self)
        while self.running:
            self.update_text_animation(0.016)
            self.render()
            pygame.display.update()
            for event in pygame.event.get():
                self.handle_event(event)
            pygame.time.wait(16)

    def handle_event(self, event):
        """Handle input events."""
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_q):
            self.running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN and not self.game_over and self.is_text_fully_displayed():
            self.running = False

    def render(self, options=None):
        """Render the dungeon menu with animated text."""
        self.display_surface.fill((0, 0, 0))
        y_offset = 20
        for line in self.displayed_lines:
            text_surf = self.font.render(line, True, (255, 255, 255))
            self.display_surface.blit(text_surf, (20, y_offset))
            y_offset += 30
        if options and self.is_text_fully_displayed():
            for idx, opt in enumerate(options):
                opt_surf = self.font.render(f"{idx+1}. {opt}", True, (180, 220, 255))
                self.display_surface.blit(opt_surf, (40, y_offset))
                y_offset += 28
        if not self.game_over and self.is_text_fully_displayed():
            prompt = self.font.render(
                "Press ENTER to continue or Q to quit", True, (255, 255, 255)
            )
            self.display_surface.blit(prompt, (20, y_offset))
        elif self.game_over:
            game_over = self.font.render(
                "Game Over! Press Q to quit", True, (255, 0, 0)
            )
            self.display_surface.blit(game_over, (20, y_offset))