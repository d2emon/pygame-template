import pygame
import time
from d2game.font import Font


class TextObject:
    def __init__(self, pos, text, font=None):
        self.pos = pos
        self.text_func = text
        self.__font = font or Font()
        self.color = self.__font.color
        self.font = pygame.font.SysFont(self.__font.name, self.__font.size)
        self.bounds = None

    def update(self):
        pass

    def draw(self, surface, center=False):
        text_surface = self.get_surface(self.text_func())
        text_rect = text_surface.get_rect()

        if center:
            pos = (self.pos[0] - text_rect.width // 2, self.pos[1])
        else:
            pos = self.pos

        surface.blit(text_surface, pos)

    def get_surface(self, text):
        return self.font.render(text, False, self.color)

    @classmethod
    def show_message(
        cls,
        surface,
        text,
        font=None,
        center=False,
        duration=5,
    ):
        surface.update()
        surface.draw()

        message = TextObject(
            surface.get_rect().center,
            lambda: text,
            font or Font(
                name='Arial',
                size=20,
                color=(255, 255, 255),
            ),
        )
        message.draw(surface, center)

        pygame.display.update()
        time.sleep(duration)
