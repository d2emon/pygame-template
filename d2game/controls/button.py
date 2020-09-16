import pygame
from d2game.events import Events
from .text_object import TextObject


class Button(pygame.sprite.Sprite):
    NORMAL = 0
    HOVER = 1
    PRESSED = 2

    def __init__(
        self,
        rect,
        text,
        on_click=lambda *args, **kwargs: None,
        padding=5,
        font=None,
    ):
        super().__init__()
        self.image = pygame.Surface((rect.width, rect.height))
        self.rect = rect
        self.text = TextObject(
            pos=(padding, padding),
            text=lambda: text,
            font=font,
        )
        self.on_click = on_click

        self.state = self.NORMAL
        self.events = Events({
            Events.MOUSEMOTION: self.on_mouse_move,
            Events.MOUSEBUTTONDOWN: self.on_mouse_down,
            Events.MOUSEBUTTONUP: self.on_mouse_up,
            Events.BUTTON_CLICK: self.on_click,
            Events.BUTTON_HOVER: self.on_hover,
            Events.BUTTON_LEAVE: self.on_leave,
            Events.BUTTON_PRESS: self.on_press,
        })

    def draw(self, state):
        if state == self.NORMAL:
            self.image.fill((255, 255, 255))
        elif state == self.HOVER:
            self.image.fill((0, 255, 255))
        elif state == self.PRESSED:
            self.image.fill((0, 0, 255))

    def update(self, *args):
        self.draw(self.state)
        self.text.draw(self.image)

    # Events

    def on_mouse_move(self, *args, **kwargs):
        pos = kwargs.get('pos', (0, 0))
        if not self.rect.collidepoint(pos):
            return self.events.emit(Events.BUTTON_LEAVE, *args, **kwargs)

        if self.state == self.PRESSED:
            return

        self.events.emit(Events.BUTTON_HOVER, *args, **kwargs)

    def on_mouse_down(self, *args, **kwargs):
        pos = kwargs.get('pos', (0, 0))
        if not self.rect.collidepoint(pos):
            return

        self.events.emit(Events.BUTTON_PRESS, *args, **kwargs)

    def on_mouse_up(self, *args, **kwargs):
        if self.state != self.PRESSED:
            return

        self.events.emit(Events.BUTTON_HOVER, *args, **kwargs)
        self.events.emit(Events.BUTTON_CLICK, *args, **kwargs)

    def on_hover(self, *args, **kwargs):
        self.state = self.HOVER

    def on_leave(self, *args, **kwargs):
        self.state = self.NORMAL

    def on_press(self, *args, **kwargs):
        self.state = self.PRESSED
