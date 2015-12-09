

class Event:
    """Event object to run.

    This object contains a function to run with any arguments. This is used by
    other objects to run specific functions at some time.

    Parameters
    ----------
    type : string
        A message specifying the type of the event.
    src_id : string
        The id of the source object creating the event.
    f : func
        The function to run.
    kwargs : dict
        Keyword arguments to provide to `f`.

    Attributes
    ----------
    id : string
        The event id.
    src_id : string
        The id of the object that created the link.
    type : string
        The type of the event.

    Methods
    -------
    run()
        Runs the event.

    Notes
    -----
    The event is initialized with a id. The `Event` class keeps a static id
    that is updated for each event to create a unique id.
    """

    # Static id to create unique ids for each event.
    _last_id = 0
    def __init__(self, type, src_id, f, **kwargs):
        # Assign the event an id
        self._id = Event._last_id
        # Update the static id to use a new id for the next event.
        Event._last_id += 1

        # Initialize event attributes
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
        """Runs the event.

        Calls the function `f` with keyword arguments `kwargs`.
        """
        self._f(**self._kwargs)

    def __str__(self):
        """Returns a string representation of the event."""
        msg = "Event {0} running: {1}"
        return msg.format(self._id, self._type)
