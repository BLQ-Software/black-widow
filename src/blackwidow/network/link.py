from blackwidow.network.rate_graph import Rate_Graph
from collections import deque
from event import Event

# Setting to use HALF_DUPLEX for sending packets
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

    Attributes
    ----------
    id : string
        The link id.
    device_a : `Device`
        One of the `Device` objects to which the link is connected.
    device_b : `Device`
        One of the `Device` objects to which the link is connected.
    delay : float
        The progapation delay in ms.
    rate : float
        The rate at which the link can send a packet in bits per ms.
    capacity : int
        The capacity of the link buffer in bits.
    distance : float
        The distance of the link. Used for dynamic routing.

    Methods
    -------
    receive(packet, source_id)
        Receives a packet from a `Device`.
    measure_distance()
        Measures the link distance.
    """

    def __init__(self, id, device_a, device_b, delay, rate, capacity, env, bw):
        self._id = id
        self._device_a = device_a
        self._device_b = device_b

        # rate is initially Mbps. rate is stored as bits per ms.
        self._rate = rate * 10 ** 3
        self._delay = delay
        # capacity is initially KB. capacity is stored as bits.
        self._capacity = capacity * 1000 * 8

        # Buffer to enter link
        self._release_into_link_buffer = deque()

        # Environment variables
        self.env = env
        self.bw = bw

        # Buffer size. Initialize to 0 since there are no packets.
        self._size = 0
        self._distance = delay
        self._send_rate = Rate_Graph(self._id, "link {0} send rate".format(self._id), self.env, self.bw)

    def __str__(self):
        """Returns a string representation of the link."""
        msg = "Link {0} connected to {1} and {2}\n"
        msg += "\t Rate: {3} mbps\n"
        msg += "\t Delay: {4} mbps\n"
        msg += "\t Capacity: {5} bits\n"
        return msg.format(self._id, self._device_a.network_id,
                          self._device_b.network_id, self._rate, self._delay,
                          self._capacity)

    # Properties for attributes

    # Link id
    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        raise AttributeError("Cannot modify link id: {0}".format(self._id))

    # Link devices
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

    # Propagation delay
    @property
    def delay(self):
        return self._delay

    @delay.setter
    def delay(self, value):
        raise AttributeError("Cannot modify link delay: {0}".format(self._id))

    # Link rate
    @property
    def rate(self):
        return self._rate

    @rate.setter
    def rate(self, value):
        raise AttributeError("Cannot modify link rate: {0}".format(self._id))

    # Link capacity
    @property
    def capacity(self):
        return self._capacity

    @capacity.setter
    def capacity(self, value):
        raise AttributeError("Cannot modify link"
                             "capacity: {0}".format(self._id))

    # Distance of link
    @property
    def distance(self):
        return self._distance

    @distance.setter
    def distance(self, value):
        raise AttributeError("Cannot modify link"
                             "distance: {0}".format(self._id))

    def receive(self, packet, source_id):
        """Receives a packet from a `Device`.

        This function takes as parameter a `Packet` and a device id. Packets
        are either enqueued in the link buffer if the link buffer is not full
        or are dropped.

        Parameters
        ----------
        packet : `Packet`
            The packet received by the link.
        source_id : string
            The id of the `Device` object sending the packet.

        """
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
            self.bw.record('{0}, {1}'.format(self.env.time, self._size),
                           'link_{0}.buffer'.format(self._id))
            print "Current size of link {}: {}".format(self._id, self._size)

            # If we only have one packet in the buffer, send it with no delay
            if len(self._release_into_link_buffer) == 1:
                # Begin sending the packet in the link
                self._send()

        # The buffer is full
        else:
            print "Packet dropped."
            self.bw.record('{0}'.format(self.env.time),
                           'link_{0}.drop'.format(self._id))

    def _send(self):
        """Sends the first packet in the buffer across the link.

        Notes
        -----
        The packet begins to transmit across the link after size / rate time,
        where size is the packet size and rate is the rate of the link. This
        function then calls _release to send the packet to the receiving
        `Device`.
        """
        # Get the first packet in the buffer. We do not dequeue until it has
        # fully been sent.
        packet_info = self._release_into_link_buffer[-1]
        # packet_info is a tuple of packet, source_id
        packet = packet_info[0]
        source_id = packet_info[1]
        # Calculate the delay time needed to begin sending the packet.
        delay = float(packet.size) / float(self._rate)

        # Create the event message
        msg = "I am link {0}. I have begun sending "
        if packet.is_ack:
            msg += "ACK "
        msg += "packet {1}"
        # Call _release after delay time to begin sending the packet.
        self.env.add_event(Event(msg.format(self._id, packet.pack_id),
                                 self._id,
                                 self._release),
                           delay)

    def _release(self):
        """Releases the packet being sent to the receiving `Device` after the
        packet has traversed the link.

        Notes
        -----
        This function dequeues the first packet in the buffer and begins
        sending it across the link. The packet is sent to its destination after
        delay time, where delay is the propagation delay of the link.
        Routing packets and acknowledgement packets are sent instantaneously to
        their destination without considering the propagation delay. This
        simplifies the network simulation.
        """
        # Dequeue the first packet in the buffer
        packet, source_id, time = self._release_into_link_buffer.pop()

        self._send_rate.add_point(packet, self.env.time)

        # Update the buffer size
        self._size -= packet.size

        # Record the buffer size
        self.bw.record('{0}, {1}'.format(self.env.time, self._size),
                       'link_{0}.buffer'.format(self._id))

        # Figure out which device to send to
        if (source_id == self._device_a.network_id):
            f = self._device_b.receive
        else:
            f = self._device_a.receive

        # Create the event message
        msg = "I am link {0}. I have sent "
        if packet.is_ack:
            msg += "ACK "
        msg += "packet {1}"

        # Ignore routing packet propagation so updates happen instantly.
        if packet.is_routing or packet.is_ack:
            delay = 0
        else:
            delay = self._delay

        # Release to device after self._delay time
        self.env.add_event(Event(msg.format(self._id, packet.pack_id),
                                 self._id,
                                 f,
                                 packet=packet),
                           delay)

        # Record link sent
        self.bw.record('{0}, {1}'.format(self.env.time, packet.size),
                       'link_{0}.sent'.format(self._id))

        # Record the link rate for packets that are not acknowledgements or
        # routing packets

        if not packet.is_ack and not packet.is_routing:

            self.bw.record('{0}, {1}'.format(self.env.time,
                                             float(packet.size) /
                                             (self.env.time - time) / 1000.0),
                           'link_{0}.rate'.format(self._id))

        # Process the next packet in the buffer
        if len(self._release_into_link_buffer) > 0:
            # Get the next packet in the buffer
            packet_info = self._release_into_link_buffer[-1]
            next_packet = packet_info[0]
            next_source_id = packet_info[1]

            # If the next packet's destination is not the same as the current
            # packet's destination and we are running in HALF_DUPLEX mode, wait
            # until the current packet has left the link before sending the
            # next packet.
            if next_source_id != source_id and HALF_DUPLEX:
                delay = self._delay
            else:
                delay = 0

            # Create the event message
            msg = "I am link {0}. I am ready to send "
            if next_packet.is_ack:
                msg += "ACK "
            msg += "packet {1}"

            # Begin sending the next packet after delay time
            self.env.add_event(Event(msg.format(self._id, next_packet.pack_id),
                                     self._id,
                                     self._send),
                               delay)

    def get_buffer_size(self):
        """Returns the buffer size in bits."""
        total_size = 0
        for packet, source_id, time in self._release_into_link_buffer:
            total_size += packet.size
        return total_size

    def measure_distance(self):
        """Measure the link distance.

        Sets the distance attribute of the link.

        """
        if self.bw.static_routing:
            self._distance = self.delay
        else:
            self._distance = (self.delay +
                              self.get_buffer_size() / float(self.rate))
