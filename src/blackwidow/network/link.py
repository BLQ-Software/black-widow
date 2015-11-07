from collections import deque
from event import Event

class Link():

    def __init__(self, id, device_a, device_b, delay, rate, capacity, env, bw):
        self.id = id
        self.device_a = device_a
        self.device_b = device_b

        # rate is initially Mbps. rate is stored as bits per ms.
        self.rate = rate * 10 ** 9
        self.delay = delay
        self.capacity = capacity * 1000 * 8

        # Buffer to enter link
        self.release_into_link_buffer = deque()

        self.env = env
        self.bw = bw
        self.size = 0

    def receive(self, packet, source_id):
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
                [packet, source_id])
            self.size += packet.size
            print "Current size of link {}: {}".format(self.id, self.size)

        # The buffer is full
        else:
            print "Packet dropped."
            self.bw.record('{0}'.format(self.env.time), 'drop')

        # If we only have one packet in the buffer, send it with no delay
        if len(self.release_into_link_buffer) == 1:
            # Begin sending the packet in the link
            self.send()


    def send(self):
        packet_info = self.release_into_link_buffer.pop()
        packet = packet_info[0]
        source_id = packet_info[1]

        delay = float(packet.size) / float(self.rate)
        # Wait for packet.size / self.rate time before packet is traveling
        msg = "I am link {0}. I have begun sending "
        if packet.is_ack:
            msg += "ACK "
        msg += "packet {1}"
        self.env.add_event(Event(msg.format(self.id, packet.pack_id), self.release, packet_info=packet_info), delay)
        if len(self.release_into_link_buffer) > 0:
            # Wait for propagation delay time before sending the next packet if
            # the current packet and the next packet are not sending to the same
            # destination.
            if self.release_into_link_buffer[-1][1] != source_id:
                delay += self.delay
            # Begin sending the next packet in the link after the previous packet is finished traveling
            msg = "I am link {0}. I am ready to send the next packet"
            self.env.add_event(Event(msg.format(self.id), self.send), delay)


    def release(self, packet_info):
        packet, source_id = packet_info
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
