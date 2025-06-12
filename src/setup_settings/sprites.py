import pygame


class Sprite(pygame.sprite.Sprite):
    def __init__(self, position, surface, *groups, layer=None):
        super().__init__(*groups)
        self.image = surface
        self.rect = self.image.get_rect(topleft=position)
        if layer is not None and hasattr(groups[0], "change_layer"):
            groups[0].change_layer(self, layer)
