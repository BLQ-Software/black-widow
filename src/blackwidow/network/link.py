from blackwidow.network.rate_graph import Rate_Graph
from collections import deque
from event import Event

HALF_DUPLEX = False

class Link(object):
    """Simulates a link connected to two Devices in the network.

    Represents a physical link in the network. In addition to simple send and
    receive, this class also handles the packet buffer for sending packets.

    Parameters
    ----------
    id : string
        A unique id for the link.
    device_a : `Device`
        A `Device` to which the link is connected.
    device_b : `Device`
        A `Device` to which the link is connected.
    delay : float
        The propagation delay to send packets across the link. Specified in ms.
    rate : float
        The rate at which the link can send a packet. Specified in Mbps.
    capacity : int
        The capacity of the link buffer. Specified in KB.
    env : `Network`
        The network that the link belongs to.
    bw : `Blackwidow`
        The printer to print data to.

    Methods
    -------
    receive(packet, source_id)
        Receives a packet from a `Device`.
    """


    def __init__(self, id, device_a, device_b, delay, rate, capacity, env, bw):
        self._id = id
        self._device_a = device_a
        self._device_b = device_b

        # rate is initially Mbps. rate is stored as bits per ms.
        self._rate = rate * 10 ** 3
        self._delay = delay
        self._capacity = capacity * 1000 * 8

        # Buffer to enter link
        self._release_into_link_buffer = deque()

        self.env = env
        self.bw = bw
        self._size = 0
        self._distance = delay
        self._send_rate = Rate_Graph(self._id, "link {0} send rate".format(self._id), self.env, self.bw)

    def __str__(self):
        msg = "Link {0} connected to {1} and {2}\n"
        msg += "\t Rate: {3} mbps\n"
        msg += "\t Delay: {4} mbps\n"
        msg += "\t Capacity: {5} bits\n"
        return msg.format(self._id, self._device_a.network_id, self._device_b.network_id, self._rate, self._delay, self._capacity)

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        raise AttributeError("Cannot modify link id: {0}".format(self._id))

    @property
    def device_a(self):
        return self._device_a

    @device_a.setter
    def device_a(self, value):
        raise AttributeError("Cannot modify link device: {0}".format(self._id))

    @property
    def device_b(self):
        return self._device_b

    @device_b.setter
    def device_b(self, value):
        raise AttributeError("Cannot modify link device: {0}".format(self._id))

    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, value):
        raise AttributeError("Cannot modify link delay: {0}".format(self._id))

    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        raise AttributeError("Cannot modify link rate: {0}".format(self._id))

    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        raise AttributeError("Cannot modify link capacity: {0}".format(self._id))

    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        raise AttributeError("Cannot modify link distance: {0}".format(self._id))

    def receive(self, packet, source_id):
        # Add packet to link buffer as soon as it is received.
        # Drop packet if the buffer is full
        message = "I am link {0}. I have received "
        if packet.is_ack:
            message += "ACK "
        message += "packet {1} at time {2}"
        print message.format(self._id, packet.pack_id, self.env.time)

        # The buffer is not yet full, so enqueue the packet
        if self._size + packet.size < self._capacity:
            self._release_into_link_buffer.appendleft(
                [packet, source_id, self.env.time])
            self._size += packet.size
            self.bw.record('{0}, {1}'.format(self.env.time, self._size), 'link_{0}.buffer'.format(self._id))
            print "Current size of link {}: {}".format(self._id, self._size)

            # If we only have one packet in the buffer, send it with no delay
            if len(self._release_into_link_buffer) == 1:
                # Begin sending the packet in the link
                self._send()

        # The buffer is full
        else:
            print "Packet dropped."
            self.bw.record('{0}'.format(self.env.time), 'link_{0}.drop'.format(self._id))


    def _send(self):
        # Wait for packet.size / self._rate time before packet is traveling
        packet_info = self._release_into_link_buffer[-1]
        packet = packet_info[0]
        source_id = packet_info[1]
        delay = float(packet.size) / float(self._rate)
        msg = "I am link {0}. I have begun sending "
        if packet.is_ack:
            msg += "ACK "
        msg += "packet {1}"
        self.env.add_event(Event(msg.format(self._id, packet.pack_id), self._id, self._release), delay)


    def _release(self):
        packet, source_id, time = self._release_into_link_buffer.pop()
        self._send_rate.add_point(packet, self.env.time)
        self._size -= packet.size
        self.bw.record('{0}, {1}'.format(self.env.time, self._size), 'link_{0}.buffer'.format(self._id))

        # Figure out which device to send to
        if (source_id == self._device_a.network_id):
            f = self._device_b.receive
        else:
            f = self._device_a.receive
        # Release to device after self._delay time
        msg = "I am link {0}. I have sent "
        if packet.is_ack:
            msg += "ACK "
        msg += "packet {1}"
        
        # Ignore routing packet propagation so updates happen instantly.
        if packet.is_routing:
            delay = 0
        else:
            delay = self._delay

        self.env.add_event(Event(msg.format(self._id, packet.pack_id), self._id, f, packet=packet), delay)
        self.bw.record('{0}, {1}'.format(self.env.time, packet.size), 'link_{0}.sent'.format(self._id))
        if not packet.is_ack and not packet.is_routing:

            self.bw.record('{0}, {1}'.format(self.env.time, float(packet.size) / (self.env.time - time) / 1000.0), 'link_{0}.rate'.format(self._id))

        if len(self._release_into_link_buffer) > 0:
            packet_info = self._release_into_link_buffer[-1]
            next_packet = packet_info[0]
            next_source_id = packet_info[1]

            if next_source_id != source_id and HALF_DUPLEX:
                delay = self._delay
            else:
                delay = 0
            msg = "I am link {0}. I am ready to send "
            if next_packet.is_ack:
                msg += "ACK "
            msg += "packet {1}"
            self.env.add_event(Event(msg.format(self._id, next_packet.pack_id), self._id, self._send), delay)

    def get_buffer_size(self):
        """Returns the buffer size in bits."""
        total_size = 0
        for packet, source_id, time in self._release_into_link_buffer:
            total_size += packet.size
        return total_size

    def measure_distance(self):
        """Measure the link distance."""
        if self.bw.static_routing:
            self._distance = self.delay
        else:
            self._distance = self.delay + self.get_buffer_size() / float(self.rate)
