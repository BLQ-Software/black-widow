


class Event:
    def __init__(self, type, f, **kwargs):
        self.type = type
        self.f = f
        self.kwargs = kwargs

    def run(self):
        self.f(**self.kwargs)


