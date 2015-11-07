from collections import deque
from event import Event
import pdb

class Link():

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
            # pdb.set_trace()

            # If we only have one packet in the buffer, send it with no delay
            if len(self.release_into_link_buffer) == 1:
                # Begin sending the packet in the link
                # pdb.set_trace()
                self.send(float(packet.size) / float(self.rate))

        # The buffer is full
        else:
            print "Packet dropped."
            self.bw.record('{0}'.format(self.env.time), 'drop')


    def send(self, delay):
        # pdb.set_trace()
        # Wait for packet.size / self.rate time before packet is traveling
        packet_info = self.release_into_link_buffer[-1]
        packet = packet_info[0]
        source_id = packet_info[1]
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

            delay = float(next_packet.size) / float(self.rate)

            if next_source_id != source_id:
                delay += self.delay

            self.send(delay)
