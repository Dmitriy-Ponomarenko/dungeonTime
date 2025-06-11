import pygame
from .settings import *

class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups):
        super().__init__(groups)
        self.animations = {}
        self.load_animations()
        self.state = 'idle'
        self.frame_index = 0
        self.animation_speed = 12  # for 120fps

        self.image = self.animations['idle'][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.time_accumulator = 0

        # Attack and cooldown logic
        self.is_attacking = False
        self.attack_start_time = 0
        self.attack_cooldown = 1000  # ms (1 second)
        self.last_attack_time = 0
        self.attack_anim_duration = 0.4  # seconds for the full attack animation
        self.attack_anim_timer = 0

        # Player attributes (unchanged)
        self.gender = "male"
        self.name = "Alaric"
        self.age = 25
        self.hair_color = "brown"
        self.hair_style = "short"
        self.eye_color = "green"
        self.height = 1.80
        self.weight = 80
        self.skin_color = "white"
        self.occupation = "warrior"
        self.body_type = "muscular"
        self.features = ["scar on right eye", "tattoo on right side neck"]
        self.clothing = {
            "torso": "black armor with red deatils",
            "legs": "black thick pants",
            "feet": "black boots with red details",
            "hands": "black leather gloves with free fingers",
            "back": "sword with dried blood and a shield"
        }

        # movement 
        self.direction = vector()
        self.speed = 200

        # Jump logic (timer-based)
        self.is_jumping = False
        self.jump_start_y = self.rect.y
        self.jump_start_time = 0
        self.jump_duration = 0.5  # seconds
        self.jump_height = 40     # pixels

        self.frozen_walk_frame = None

        # --- Flipping ---
        self.facing_left = False

    def load_animations(self):
        animation_data = {
            'idle':   ('src/data/graphics/player/player_idle.png', 5, 100, 100),
            'walk':   ('src/data/graphics/player/player_walk.png', 6, 100, 100),
            'attack': ('src/data/graphics/player/player_attack3.png', 6, 100, 100),
        }
        BORDER_WIDTH = 128
        BORDER_HEIGHT = 90

        for state, (path, frames, fw, fh) in animation_data.items():
            sheet = pygame.image.load(path).convert_alpha()
            anim_frames = []
            for i in range(frames):
                frame = sheet.subsurface(pygame.Rect(i * fw, 0, fw, fh))
                scaled_frame = pygame.transform.scale(frame, (fw * 3, fh * 3))
                final_frame = pygame.Surface((BORDER_WIDTH, BORDER_HEIGHT), pygame.SRCALPHA)
                rect = scaled_frame.get_rect(center=final_frame.get_rect().center)
                final_frame.blit(scaled_frame, rect)
                pygame.draw.rect(final_frame, (255, 0, 0), final_frame.get_rect(), 3)
                anim_frames.append(final_frame)
            self.animations[state] = anim_frames

    def handle_attack_input(self):
        now = pygame.time.get_ticks()
        mouse_pressed = pygame.mouse.get_pressed()[0]

        # If on cooldown or already attacking, can't attack
        if self.is_attacking or (now - self.last_attack_time < self.attack_cooldown):
            return

        # Start attack
        if mouse_pressed:
            self.is_attacking = True
            self.attack_start_time = now
            self.attack_anim_timer = 0
            self.frame_index = 0

    def set_state(self):
        if self.is_attacking:
            self.state = 'attack'
            return
        elif self.is_jumping:
            if self.state == 'walk' and self.frozen_walk_frame is None:
                self.frozen_walk_frame = self.frame_index
            if self.state == 'walk':
                self.state = 'walk'
            else:
                self.state = 'idle'
        elif self.direction.length_squared() > 0:
            self.state = 'walk'
            self.frozen_walk_frame = None
        else:
            self.state = 'idle'
            self.frozen_walk_frame = None

    def animate(self, dt):
        frames = self.animations[self.state]
        if self.state == 'attack' and self.is_attacking:
            self.attack_anim_timer += dt
            anim_length = self.attack_anim_duration
            frame_count = len(frames)
            progress = min(self.attack_anim_timer / anim_length, 0.999)
            self.frame_index = int(progress * frame_count)
            image = frames[self.frame_index]
            # Flip if needed
            if self.facing_left:
                image = pygame.transform.flip(image, True, False)
            self.image = image
            if self.attack_anim_timer >= anim_length:
                self.is_attacking = False
                self.last_attack_time = pygame.time.get_ticks()
                self.frame_index = 0
            return

        if self.is_jumping and self.state == 'walk' and self.frozen_walk_frame is not None:
            image = frames[self.frozen_walk_frame]
            if self.facing_left:
                image = pygame.transform.flip(image, True, False)
            self.image = image
            return
        self.time_accumulator += dt
        if self.time_accumulator > 1 / self.animation_speed:
            self.time_accumulator = 0
            self.frame_index = (self.frame_index + 1) % len(frames)
        image = frames[self.frame_index]
        if self.facing_left:
            image = pygame.transform.flip(image, True, False)
        self.image = image

    def input(self):
        if self.is_attacking:
            self.direction = vector(0, 0)
            return
        keys = pygame.key.get_pressed()
        input_vector = vector(0, 0)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            input_vector.x += 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            input_vector.x -= 1
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            input_vector.y += 1
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            input_vector.y -= 1
        # Jump
        if keys[pygame.K_SPACE]:
            self.jump()

        # --- Flipping logic ---
        if input_vector.x < 0:
            self.facing_left = True
        elif input_vector.x > 0:
            self.facing_left = False

        if input_vector.length() > 0:
            self.direction = input_vector.normalize()
        else:
            self.direction = vector(0, 0)

    def move(self, dt):
        if self.is_attacking:
            return
        move_vector = self.direction * self.speed * dt
        # Normalize diagonal speed
        if abs(self.direction.x) > 0 and abs(self.direction.y) > 0:
            move_vector *= 1.19
        self.rect.topleft += move_vector

    def jump(self):
        if self.is_attacking:
            return
        if not self.is_jumping:
            self.is_jumping = True
            self.jump_start_y = self.rect.y
            self.jump_start_time = pygame.time.get_ticks() / 1000.0  # seconds

    def update_jump(self):
        if self.is_jumping:
            now = pygame.time.get_ticks() / 1000.0  # seconds
            elapsed = now - self.jump_start_time
            if elapsed < self.jump_duration:
                # Parabolic jump: y = -4h * (t/T - 0.5)^2 + h
                t = elapsed / self.jump_duration
                offset = -4 * self.jump_height * (t - 0.5) ** 2 + self.jump_height
                self.rect.y = self.jump_start_y - offset
            else:
                self.rect.y = self.jump_start_y
                self.is_jumping = False

    def update(self, dt):
        self.input()
        self.handle_attack_input()
        self.set_state()
        self.animate(dt)
        self.move(dt)
        self.update_jump()