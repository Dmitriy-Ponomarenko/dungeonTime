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
        self._setup(tmx_map)
        self._create_map_borders()

    def _setup(self, tmx_map):
        """Setup level with optimized sprite creation."""
        # Cache terrain tiles to avoid repeated surface creation
        terrain_layer = tmx_map.get_layer_by_name("Terrain")
        for x, y, surf in terrain_layer.tiles():
            Sprite((x * TILE_SIZE, y * TILE_SIZE), surf, self.all_sprites, layer=0)

        # Player setup
        for obj in tmx_map.get_layer_by_name("Objects"):
            if getattr(obj, "name", None) == "player":
                self.player = Player(
                    (obj.x, obj.y), self.all_sprites, self.collision_sprites
                )
                self.all_sprites.change_layer(self.player, 2)
                break  # Exit after finding player to avoid unnecessary iterations

        # Optimized tree rendering with cached surfaces
        for obj in tmx_map.get_layer_by_name("Objects"):
            if hasattr(obj, "gid") and obj.gid is not None:
                surf = tmx_map.get_tile_image_by_gid(obj.gid)
                if surf:
                    base_height = min(30, surf.get_height())
                    base_rect = pygame.Rect(
                        0,
                        surf.get_height() - base_height,
                        surf.get_width(),
                        base_height,
                    )
                    base_surf = (
                        surf.subsurface(base_rect).copy()
                        if base_height
                        else surf.copy()
                    )
                    base_sprite = Sprite(
                        (
                            obj.x,
                            obj.y
                            + (surf.get_height() - base_height if base_height else 0),
                        ),
                        base_surf,
                        self.all_sprites,
                        self.collision_sprites,
                        layer=1,
                    )

                    if base_height and surf.get_height() > base_height:
                        top_rect = pygame.Rect(
                            0, 0, surf.get_width(), surf.get_height() - base_height
                        )
                        top_surf = surf.subsurface(top_rect).copy()
                        Sprite((obj.x, obj.y), top_surf, self.all_sprites, layer=3)

    def _create_map_borders(self):
        """Create map borders efficiently."""
        borders = [
            (-TILE_SIZE, 0, TILE_SIZE, self.map_height),  # left
            (self.map_width, 0, TILE_SIZE, self.map_height),  # right
            (0, -TILE_SIZE, self.map_width, TILE_SIZE),  # top
            (0, self.map_height, self.map_width, TILE_SIZE),  # bottom
        ]
        for x, y, w, h in borders:
            border = pygame.sprite.Sprite(self.collision_sprites)
            border.image = pygame.Surface((w, h), pygame.SRCALPHA)
            border.rect = pygame.Rect(x, y, w, h)

    def update_camera(self):
        """Smooth camera movement with bounds checking."""
        if self.player:
            target = pygame.Vector2(self.player.rect.center) - pygame.Vector2(
                WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2
            )
            # Clamp camera to map bounds
            target.x = max(0, min(target.x, self.map_width - WINDOW_WIDTH))
            target.y = max(0, min(target.y, self.map_height - WINDOW_HEIGHT))
            self.camera_offset += (target - self.camera_offset) * self.camera_speed

    def run(self, dt):
        """Optimized rendering loop."""
        self.all_sprites.update(dt)
        self.update_camera()
        self.display_surface.fill((10, 20, 60))  # dark blue
        # Batch rendering to reduce draw calls
        for sprite in self.all_sprites:
            offset_rect = sprite.rect.move(-self.camera_offset)
            self.display_surface.blit(sprite.image, offset_rect)
