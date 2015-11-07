from collections import deque
from event import Event
import pdb

class Link():
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
    receive(packet)
        Receives a packet from a `Device`.
    """


    def __init__(self, id, device_a, device_b, delay, rate, capacity, env, bw):
        self.id = id
        self.device_a = device_a
        self.device_b = device_b

        # rate is initially Mbps. rate is stored as bits per ms.
        self.rate = rate * 10 ** 3
        self.delay = delay
        self.capacity = capacity * 1000 * 8

        # Buffer to enter link
        self.release_into_link_buffer = deque()

        self.env = env
        self.bw = bw
        self.size = 0

    def __str__(self):
        msg = "Link {0} connected to {1} and {2}\n"
        msg += "\t Rate: {3} mbps\n"
        msg += "\t Delay: {4} mbps\n"
        msg += "\t Capacity: {5} bits\n"
        return msg.format(self.id, self.device_a.network_id, self.device_b.network_id, self.rate, self.delay, self.capacity)

    def receive(self, packet):
        # Add packet to link buffer as soon as it is received.
        # Drop packet if the buffer is full
        message = "I am link {0}. I have received "
        if packet.is_ack:
            message += "ACK "
        message += "packet {1} at time {2}"
        print message.format(self.id, packet.pack_id, self.env.time)

        # The buffer is not yet full, so enqueue the packet
        if self.size + packet.size < self.capacity:
            self.release_into_link_buffer.appendleft(
                [packet, packet.src])
            self.size += packet.size
            print "Current size of link {}: {}".format(self.id, self.size)
            # pdb.set_trace()

            # If we only have one packet in the buffer, send it with no delay
            if len(self.release_into_link_buffer) == 1:
                # Begin sending the packet in the link
                # pdb.set_trace()
                self.send()

        # The buffer is full
        else:
            print "Packet dropped."
            self.bw.record('{0}'.format(self.env.time), 'drop')


    def send(self):
        # pdb.set_trace()
        # Wait for packet.size / self.rate time before packet is traveling
        packet_info = self.release_into_link_buffer[-1]
        packet = packet_info[0]
        source_id = packet_info[1]
        delay = float(packet.size) / float(self.rate)
        msg = "I am link {0}. I have begun sending "
        if packet.is_ack:
            msg += "ACK "
        msg += "packet {1}"
        self.env.add_event(Event(msg.format(self.id, packet.pack_id), self.release), delay)


    def release(self):
        # pdb.set_trace()
        packet, source_id = self.release_into_link_buffer.pop()
        self.size -= packet.size

        # Figure out which device to send to
        if (source_id == self.device_a.network_id):
            f = self.device_b.receive
        else:
            f = self.device_a.receive
        # Release to device after self.delay time
        msg = "I am link {0}. I have sent "
        if packet.is_ack:
            msg += "ACK "
        msg += "packet {1}"
        self.env.add_event(Event(msg.format(self.id, packet.pack_id), f, packet=packet), self.delay)
        self.bw.record('{0}, {1}'.format(self.env.time, packet.size), 'link.sent')

        if len(self.release_into_link_buffer) > 0:
            packet_info = self.release_into_link_buffer[-1]
            next_packet = packet_info[0]
            next_source_id = packet_info[1]

            if next_source_id != source_id:
                delay = self.delay
            else:
                delay = 0
            msg = "I am link {0}. I am ready to send "
            if next_packet.is_ack:
                msg += "ACK "
            msg += "packet {1}"
            self.env.add_event(Event(msg.format(self.id, next_packet.pack_id), self.send), delay)
