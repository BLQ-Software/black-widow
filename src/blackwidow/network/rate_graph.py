from blackwidow.network.packet import Packet
from event import Event
from Queue import PriorityQueue

class Data(object):
    """ Class to represent an amount of data and the time it was sent.
        It is used as a priority queue object with time as the priority.
    """
    def __init__(self, time, size):
        self._time = time
        self._size = size

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        raise AttributeError("Cannot change time")

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        raise AttributeError("Cannot change size")

    def __cmp__(self, other):
    """ Method to compare with other objects in the priority queue.
    """
        return cmp(self._time, other.time)

class Rate_Graph(object):
    """ Class to graph rates.
    """
    def __init__(self, object_id, name, env, bw):
        """ Constructor for Rate_Graph class
        """
        self.name = name
        self.env = env
        self.bw = bw
        self.object_id = object_id
        self.window_size = 1000
        self.window = PriorityQueue()
        self.bits_in_window = 0
        # Interval between points
        self.interval = 10
        self.env.add_event(Event("Graph rate", self.object_id, self.graph), self.window_size)

    def add_point(self, packet, time):
        """ Adds a point to the queue
        """
        self.window.put(Data(time, packet.size))
        self.bits_in_window = self.bits_in_window + packet.size

    def remove_points(self, time):
        """ Removes data before time
        """
        while ((not self.window.empty()) and self.peek_time() < time):
            first = self.window.get()
            self.bits_in_window = self.bits_in_window - first.size

    def peek_time(self):
        """ Return the time of the first object in the queue
        """
        temp = self.window.get()
        self.window.put(temp)
        return temp.time


    def graph(self):
        """ Graphs current rate
        """
        self.remove_points(self.env.time-self.window_size)
        current_rate = float(self.bits_in_window)/float(self.window_size)
        self.bw.record('{0}, {1}'.format(self.env.time, current_rate), '{0}'.format(self.name))
        self.env.add_event(Event("Graph rate", self.object_id, self.graph), self.interval)
