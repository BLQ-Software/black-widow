from blackwidow.network.packet import Packet
from event import Event
import Queue

class Data(object):
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

class Rate_Graph(object):
    """Class to graph rates.
    """
    def __init__(self, name, bw):
        """ Constructor for Rate_Graph class
        """
        self._name = name
        self.bw = bw
        self.window_size = 100
        self.window = PriorityQueue()
        self.bits_in_window = 0

    def add_point(self, packet, time):
        """ Adds a point to the queue
        """
        self.window.put(Data(time, packet.size))
        self.bits_in_window = self.bits_in_window + packet.size

    def remove_points(self, time):
        """ Removes data before time
        """
        while ((not self.window.empty()) and 

    def peek_time(self):
        temp = self.window.get()
        temp_time = temp.time



    def graph(self):
        self.bw.record('{0}, {1}'.format(self.env.time,packet.size), '{0}.rate'.format(self.name))
