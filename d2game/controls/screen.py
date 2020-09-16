import pygame
from d2game.events import Events


class Screen(pygame.Surface):
    def __init__(self, size):
        super().__init__(size)
        self.sprites = pygame.sprite.Group()
        self.events = Events({
            Events.UPDATE: self.update,
            Events.DRAW: self.draw,
        })

    def update(self, *args, **kwargs):
        self.sprites.update()

    def draw(self, *args, **kwargs):
        self.sprites.draw(self)
