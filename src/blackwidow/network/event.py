class Event:
    _last_id = 0
    def __init__(self, type, src_id, f, **kwargs):
        self._id = Event._last_id
        Event._last_id += 1

        self._type = type
        self._f = f
        self._kwargs = kwargs
        self._src_id = src_id

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        raise AttributeError("Cannot modify event id: {0}".format(self._id))

    @property
    def src_id(self):
        return self._src_id

    @src_id.setter
    def src_id(self, value):
        raise AttributeError("Cannot modify event source id: {0}".format(self._id))

    @property
    def type(self):
        return self._type

    @type.setter
    def type(self, value):
        raise AttributeError("Cannot modify event type: {0}".format(self._id))

    def run(self):
        self._f(**self._kwargs)

    def __str__(self):
        msg = "Event {0} running: {1}"
        return msg.format(self._id, self._type)
