import pygame
from .settings import *
from .sprites import Sprite
from .player import Player

class Level:
    def __init__(self, tmx_map):
        self.display_surface = pygame.display.get_surface()
        self.all_sprites = pygame.sprite.LayeredUpdates()  # Layered group!
        self.camera_offset = pygame.Vector2(0, 0)
        self.camera_speed = 0.15
        self.player = None
        self.setup(tmx_map)

    def setup(self, tmx_map):
        # Terrain tiles
        for x, y, surf in tmx_map.get_layer_by_name('Terrain').tiles():
            # print(f"Tile at {x},{y} created")
            tile = Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites)
            self.all_sprites.change_layer(tile, 0)
        # Player
        for obj in tmx_map.get_layer_by_name('Objects'):
            print(f"Object: {getattr(obj, 'name', None)} at {obj.x},{obj.y}")
            if getattr(obj, 'name', None) == 'player':
                print("Player created at", obj.x, obj.y)
                self.player = Player((obj.x, obj.y), self.all_sprites)
                self.all_sprites.change_layer(self.player, 1)

        # Draw tree objects (objects with a gid)
        for obj in tmx_map.get_layer_by_name('Objects'):
            if hasattr(obj, 'gid') and obj.gid is not None:
                surf = tmx_map.get_tile_image_by_gid(obj.gid)
                if surf:
                    Sprite((obj.x, obj.y), surf, self.all_sprites)
                    # Optionally, set layer for trees if you want
                    self.all_sprites.change_layer(self.all_sprites.sprites()[-1], 1)

    def update_camera(self):
        if self.player:
            target = pygame.Vector2(self.player.rect.center) - pygame.Vector2(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2)
            self.camera_offset += (target - self.camera_offset) * self.camera_speed

    def run(self, dt):
        self.all_sprites.update(dt)
        self.display_surface.fill((10, 20, 60))  # dark blue
        for sprite in self.all_sprites:
            offset_rect = sprite.rect.copy()
            offset_rect.topleft -= self.camera_offset
            self.display_surface.blit(sprite.image, offset_rect)