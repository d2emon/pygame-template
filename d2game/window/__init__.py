import pygame
import sys
from d2game.events import Events


class Window:
    EXIT = 0
    INITIALIZATION = 100
    PLAYING = 200
    GAME_OVER = 300
    WIN = 400

    __EVENT_MAP = {
        pygame.KEYDOWN: Events.KEYDOWN,
        pygame.KEYUP: Events.KEYUP,
    }

    def __init__(
        self,
        caption='Game',
        fps=60,
        size=(800, 600),
        mixer=None,  # (44100, 16, 2, 4096)
    ):
        # Config
        self.state = self.INITIALIZATION
        self.__is_showing = False
        self.surface = None
        self.screen = None
        self.caption = caption
        self.fps = fps
        self.size = size

        self.init_pygame(mixer)
        self.clock = pygame.time.Clock()

        # Setup events
        self.events = Events({
            pygame.QUIT: self.on_close,

            pygame.KEYUP: self.on_key_event,
            pygame.KEYDOWN: self.on_key_event,

            pygame.MOUSEBUTTONDOWN: self.on_key_event,
            pygame.MOUSEBUTTONUP: self.on_key_event,
            pygame.MOUSEMOTION: self.on_key_event,
        })

    @classmethod
    def init_pygame(cls, mixer=None):
        if mixer:
            pygame.mixer.pre_init(*mixer)
        pygame.init()
        pygame.font.init()

    def set_screen(self, screen, state=None):
        if state is not None:
            self.state = state

        self.screen = screen
        self.events.add_child(self.screen.events)

    @property
    def is_initialized(self):
        return self.state != self.INITIALIZATION

    @property
    def is_showing(self):
        return self.is_initialized and self.__is_showing

    @property
    def is_win(self):
        return self.state == self.WIN

    @property
    def is_loose(self):
        return self.state == self.GAME_OVER

    # Events
    def on_close(self, *args, **kwargs):
        self.__is_showing = False

    def on_key_event(self, event_type, *args, **kwargs):
        self.events.emit(
            self.__EVENT_MAP.get(event_type),
            *args,
            **kwargs,
            keys=pygame.key.get_pressed(),
        )
        # if pygame.K_ESCAPE in pygame.key.get_pressed():
        #     self.close()

    def on_mouse_event(self, event_type, *args, **kwargs):
        event = kwargs.get('events')
        self.events.emit(
            self.__EVENT_MAP.get(event_type),
            *args,
            **kwargs,
            pos=event.pos if event else None,
        )

    # Phases
    def show(self):
        self.surface = pygame.display.set_mode(self.size)
        pygame.display.set_caption(self.caption)
        self.events.emit(Events.INIT)
        self.__is_showing = True
        self.state = self.PLAYING

    def close(self):
        self.state = self.EXIT
        self.__is_showing = False
        pygame.quit()
        sys.exit()

    def win_game(self):
        self.state = self.WIN

    def loose_game(self):
        self.state = self.GAME_OVER

    def draw(self, *args, **kwargs):
        self.events.emit(Events.UPDATE, *args, **kwargs)
        self.events.emit(Events.DRAW, *args, **kwargs)

        if self.screen is not None:
            self.surface.blit(self.screen, (0, 0))

        pygame.display.update()
        self.clock.tick(self.fps)

    def run(self):
        self.show()
        while self.is_showing:
            for event in pygame.event.get():
                self.events.emit(event.type, event=event)

            self.draw()
        self.close()
