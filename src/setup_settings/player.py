import pygame
from .settings import *


class Player(pygame.sprite.Sprite):
    def __init__(self, pos, groups, collision_sprites=None):
        super().__init__(groups)
        self.animations = {}
        self._load_animations()
        self.state = "idle"
        self.frame_index = 0
        self.animation_speed = 12
        self.image = self.animations["idle"][self.frame_index]
        self.rect = self.image.get_rect(topleft=pos)
        self.time_accumulator = 0

        # Collider
        collider_width = self.rect.width // 2
        collider_height = self.rect.height // 3
        collider_x = self.rect.centerx - collider_width // 2
        collider_y = self.rect.bottom - collider_height - 10
        self.collider = pygame.Rect(
            collider_x, collider_y, collider_width, collider_height
        )

        # Attack logic
        self.is_attacking = False
        self.attack_start_time = 0
        self.attack_cooldown = 1000
        self.last_attack_time = 0
        self.attack_anim_duration = 0.4
        self.attack_anim_timer = 0

        # Player attributes
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
            "torso": "black armor with red details",
            "legs": "black thick pants",
            "feet": "black boots with red details",
            "hands": "black leather gloves with free fingers",
            "back": "sword with dried blood and a shield",
        }

        # Movement
        self.direction = pygame.Vector2()
        self.speed = 200
        self.is_jumping = False
        self.jump_start_y = self.rect.y
        self.jump_start_time = 0
        self.jump_duration = 0.5
        self.jump_height = 40
        self.frozen_walk_frame = None
        self.facing_left = False
        self.collision_sprites = collision_sprites

    def _load_animations(self):
        """Load and cache animations efficiently."""
        animation_data = {
            "idle": ("src/data/graphics/player/player_idle.png", 5, 100, 100),
            "walk": ("src/data/graphics/player/player_walk.png", 6, 100, 100),
            "attack": ("src/data/graphics/player/player_attack3.png", 6, 100, 100),
        }
        BORDER_WIDTH, BORDER_HEIGHT = 128, 96
        for state, (path, frames, fw, fh) in animation_data.items():
            try:
                sheet = pygame.image.load(path).convert_alpha()
                anim_frames = []
                for i in range(frames):
                    frame = sheet.subsurface(pygame.Rect(i * fw, 0, fw, fh))
                    scaled_frame = pygame.transform.scale(frame, (fw * 3, fh * 3))
                    final_frame = pygame.Surface(
                        (BORDER_WIDTH, BORDER_HEIGHT), pygame.SRCALPHA
                    )
                    rect = scaled_frame.get_rect(center=final_frame.get_rect().center)
                    final_frame.blit(scaled_frame, rect)
                    anim_frames.append(final_frame)
                self.animations[state] = anim_frames
            except pygame.error as e:
                print(f"Error loading animation {state}: {e}")
                self.animations[state] = [
                    pygame.Surface((BORDER_WIDTH, BORDER_HEIGHT), pygame.SRCALPHA)
                ]

    def handle_attack_input(self):
        """Handle attack input with optimized timing."""
        now = pygame.time.get_ticks()
        if self.is_attacking or (now - self.last_attack_time < self.attack_cooldown):
            return
        if pygame.mouse.get_pressed()[0]:
            self.is_attacking = True
            self.attack_start_time = now
            self.attack_anim_timer = 0
            self.frame_index = 0

    def set_state(self):
        """Determine player state efficiently."""
        prev_state = getattr(self, "prev_state", None)
        if self.is_attacking:
            self.state = "attack"
        elif self.is_jumping:
            if self.state == "walk" and self.frozen_walk_frame is None:
                self.frozen_walk_frame = self.frame_index
            self.state = "walk" if self.state == "walk" else "idle"
        elif self.direction.length_squared() > 0:
            self.state = "walk"
            self.frozen_walk_frame = None
        else:
            self.state = "idle"
            self.frozen_walk_frame = None
        if self.state != prev_state:
            self.frame_index = 0
        self.prev_state = self.state

    def animate(self, dt):
        """Optimized animation with frame caching."""
        frames = self.animations.get(self.state, self.animations["idle"])
        if self.frame_index >= len(frames):
            self.frame_index = 0
        if self.state == "attack" and self.is_attacking:
            self.attack_anim_timer += dt
            progress = min(self.attack_anim_timer / self.attack_anim_duration, 0.999)
            self.frame_index = int(progress * len(frames))
            image = frames[self.frame_index]
            self.image = (
                pygame.transform.flip(image, True, False) if self.facing_left else image
            )
            if self.attack_anim_timer >= self.attack_anim_duration:
                self.is_attacking = False
                self.last_attack_time = pygame.time.get_ticks()
                self.frame_index = 0
            return
        if (
            self.is_jumping
            and self.state == "walk"
            and self.frozen_walk_frame is not None
        ):
            image = frames[self.frozen_walk_frame]
            self.image = (
                pygame.transform.flip(image, True, False) if self.facing_left else image
            )
            return
        self.time_accumulator += dt
        if self.time_accumulator > 1 / self.animation_speed:
            self.time_accumulator = 0
            self.frame_index = (self.frame_index + 1) % len(frames)
        image = frames[self.frame_index]
        self.image = (
            pygame.transform.flip(image, True, False) if self.facing_left else image
        )

    def input(self):
        """Handle input efficiently."""
        keys = pygame.key.get_pressed()
        input_vector = pygame.Vector2(0, 0)
        if not self.is_jumping:
            if keys[pygame.K_DOWN] or keys[pygame.K_s]:
                input_vector.y += 1
            if keys[pygame.K_UP] or keys[pygame.K_w]:
                input_vector.y -= 1
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            input_vector.x -= 1
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            input_vector.x += 1
        if keys[pygame.K_SPACE]:
            self.jump()
        self.facing_left = (
            input_vector.x < 0 if input_vector.x != 0 else self.facing_left
        )
        self.direction = (
            input_vector.normalize() if input_vector.length() > 0 else pygame.Vector2()
        )

    def move(self, dt):
        """Optimized movement with collision detection."""
        if self.is_attacking:
            return
        move_vector = self.direction * self.speed * dt
        if abs(self.direction.x) > 0 and abs(self.direction.y) > 0:
            move_vector *= 1.19
        self.collider.x += move_vector.x
        if self.collision_sprites:
            for sprite in self.collision_sprites:
                if self.collider.colliderect(sprite.rect):
                    if move_vector.x > 0:
                        self.collider.right = sprite.rect.left
                    elif move_vector.x < 0:
                        self.collider.left = sprite.rect.right
        self.collider.y += move_vector.y
        if self.collision_sprites:
            for sprite in self.collision_sprites:
                if self.collider.colliderect(sprite.rect):
                    if move_vector.y > 0:
                        self.collider.bottom = sprite.rect.top
                    elif move_vector.y < 0:
                        self.collider.top = sprite.rect.bottom
        self.rect.centerx = self.collider.centerx
        self.rect.bottom = self.collider.bottom + 10

    def jump(self):
        """Handle jump logic."""
        if self.is_attacking or self.is_jumping:
            return
        self.is_jumping = True
        self.jump_start_y = self.rect.y
        self.jump_start_time = pygame.time.get_ticks() / 1000.0

    def update_jump(self):
        """Update jump mechanics."""
        if self.is_jumping:
            now = pygame.time.get_ticks() / 1000.0
            elapsed = now - self.jump_start_time
            if elapsed < self.jump_duration:
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
