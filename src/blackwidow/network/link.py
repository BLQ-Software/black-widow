from collections import deque
from event import Event

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
                [packet, source_id])
            self._size += packet.size
            print "Current size of link {}: {}".format(self._id, self._size)

            # If we only have one packet in the buffer, send it with no delay
            if len(self._release_into_link_buffer) == 1:
                # Begin sending the packet in the link
                self._send()

        # The buffer is full
        else:
            print "Packet dropped."
            self.bw.record('{0}'.format(self.env.time), 'drop')


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
        self.env.add_event(Event(msg.format(self._id, packet.pack_id), self._release), delay)


    def _release(self):
        packet, source_id = self._release_into_link_buffer.pop()
        self._size -= packet.size

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
        self.env.add_event(Event(msg.format(self._id, packet.pack_id), f, packet=packet), self._delay)
        self.bw.record('{0}, {1}'.format(self.env.time, packet.size), 'link.sent')

        if len(self._release_into_link_buffer) > 0:
            packet_info = self._release_into_link_buffer[-1]
            next_packet = packet_info[0]
            next_source_id = packet_info[1]

            if next_source_id != source_id:
                delay = self._delay
            else:
                delay = 0
            msg = "I am link {0}. I am ready to send "
            if next_packet.is_ack:
                msg += "ACK "
            msg += "packet {1}"
            self.env.add_event(Event(msg.format(self._id, next_packet.pack_id), self._send), delay)
