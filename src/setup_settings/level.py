import pygame
from .settings import *
from .sprites import Sprite
from .player import Player


class Level:
    def __init__(self, tmx_map, player_name, player_health):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.LayeredUpdates()
        self.collision_sprites = pygame.sprite.Group()
        self.camera_offset = pygame.Vector2(0, 0)
        self.camera_speed = 0.15
        self.player = None
        self.player_name = player_name
        self.player_health = player_health
        self.map_width = tmx_map.width * TILE_SIZE
        self.map_height = tmx_map.height * TILE_SIZE
        self.setup(tmx_map)
        self.create_map_borders()

    def setup(self, tmx_map):
        # Terrain tiles (layer 0)
        for x, y, surf in tmx_map.get_layer_by_name("Terrain").tiles():
            tile = Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)
            self.all_sprites.change_layer(tile, 0)

        # Player (layer 2)
        for obj in tmx_map.get_layer_by_name("Objects"):
            if getattr(obj, "name", None) == "player":
                print("Player created at", obj.x, obj.y)
                self.player = Player(
                    (obj.x, obj.y), self.all_sprites, self.collision_sprites
                )
                self.all_sprites.change_layer(self.player, 2)

        # Trees (layer 1 for base/collision, layer 3 for top)
        for obj in tmx_map.get_layer_by_name("Objects"):
            if hasattr(obj, "gid") and obj.gid is not None:
                surf = tmx_map.get_tile_image_by_gid(obj.gid)
                if surf:
                    # Draw base (for collision, e.g. bottom 30px)
                    base_height = 30
                    if surf.get_height() > base_height:
                        base_rect = pygame.Rect(
                            0,
                            surf.get_height() - base_height,
                            surf.get_width(),
                            base_height,
                        )
                        base_surf = surf.subsurface(base_rect).copy()
                        base_sprite = Sprite(
                            (obj.x, obj.y + surf.get_height() - base_height),
                            base_surf,
                            self.all_sprites,
                            self.collision_sprites,
                        )
                        self.all_sprites.change_layer(base_sprite, 1)

                        # Draw top (over player)
                        top_rect = pygame.Rect(
                            0, 0, surf.get_width(), surf.get_height() - base_height
                        )
                        if top_rect.height > 0:
                            top_surf = surf.subsurface(top_rect).copy()
                            top_sprite = Sprite((obj.x, obj.y), top_surf, self.all_sprites)
                            self.all_sprites.change_layer(top_sprite, 3)
                    else:
                        # Image is too small, use the whole image
                        base_surf = surf.copy()
                        base_sprite = Sprite(
                            (obj.x, obj.y),
                            base_surf,
                            self.all_sprites,
                            self.collision_sprites,
                        )
                        self.all_sprites.change_layer(base_sprite, 1)

                        # No top sprite needed, as the whole image is used for the base

    def create_map_borders(self):
        borders = [
            pygame.Rect(-TILE_SIZE, 0, TILE_SIZE, self.map_height),  # left
            pygame.Rect(self.map_width, 0, TILE_SIZE, self.map_height),  # right
            pygame.Rect(0, -TILE_SIZE, self.map_width, TILE_SIZE),  # top
            pygame.Rect(0, self.map_height, self.map_width, TILE_SIZE),  # bottom
        ]
        for rect in borders:
            border = pygame.sprite.Sprite(self.collision_sprites)
            border.image = pygame.Surface((rect.width, rect.height), pygame.SRCALPHA)
            border.rect = rect

    def update_camera(self):
        if self.player:
            target = pygame.Vector2(self.player.rect.center) - pygame.Vector2(
                WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
            )
            self.camera_offset += (target - self.camera_offset) * self.camera_speed

    def run(self, dt):
        self.all_sprites.update(dt)
        self.update_camera()
        self.display_surface.fill((10, 20, 60))  # dark blue
        for sprite in self.all_sprites:
            offset_rect = sprite.rect.copy()
            offset_rect.topleft -= self.camera_offset
            self.display_surface.blit(sprite.image, offset_rect)
