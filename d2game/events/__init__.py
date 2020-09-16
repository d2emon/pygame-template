class Events:
    INIT = 'INIT'
    UPDATE = 'UPDATE'
    DRAW = 'DRAW'

    KEY = 'KEY'
    KEYDOWN = 'KEYDOWN'
    KEYUP = 'KEYUP'

    MOUSEMOTION = 'MOUSEMOTION'
    MOUSEBUTTONDOWN = 'MOUSEBUTTONDOWN'
    MOUSEBUTTONUP = 'MOUSEBUTTONUP'

    BUTTON_CLICK = 'BUTTON.CLICK'
    BUTTON_HOVER = 'BUTTON.HOVER'
    BUTTON_LEAVE = 'BUTTON.LEAVE'
    BUTTON_PRESS = 'BUTTON.PRESS'

    def __init__(self, handlers=None):
        self.handlers = handlers or {}
        self.children = []

    def emit(self, event_type, *args, **kwargs):
        for child in self.children:
            child.emit(event_type, *args, **kwargs)

        handler = self.handlers.get(event_type)
        if not handler:
            return
        handler(event_type, *args, **kwargs)

    def add(self, event_id, handler):
        self.handlers[event_id] = handler

    def remove(self, event_id):
        del self.handlers[event_id]

    def add_child(self, events):
        self.children.append(events)

    def remove_child(self, events):
        self.children.remove(events)
