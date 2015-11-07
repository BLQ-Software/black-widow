


class Event:
    id = 0
    def __init__(self, type, f, **kwargs):
        self.id = Event.id
        Event.id += 1
        self.type = type
        self.f = f
        self.kwargs = kwargs

    def run(self):
        self.f(**self.kwargs)

    def __str__(self):
        msg = "Event {0} running: {1}"
        return msg.format(self.id, self.type)
