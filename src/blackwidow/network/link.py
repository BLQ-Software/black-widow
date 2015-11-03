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
        if self.size + packet.size < self.capacity:
            self.release_into_link_buffer.appendleft(
                [packet, source_id])
            self.size += packet.size
            print "Current size of link {}: {}".format(self.id, self.size)
        else:
            print "Packet dropped."
            self.bw.record('{0}'.format(self.env.time), 'drop')
        if len(self.release_into_link_buffer) == 1:
            # Begin sending the packet in the link
            self.env.add_event(Event("Packet buffer in link", self.send), 0)


    def send(self):
        packet_info = self.release_into_link_buffer.pop()
        packet = packet_info[0]
        source_id = packet_info[1]

        delay = float(packet.size) / float(self.rate)
        # Wait for packet.size / self.rate time before packet is traveling
        self.env.add_event(Event("Send to link", self.release, packet_info=packet_info), delay)
        if len(self.release_into_link_buffer) > 0:
            if self.release_into_link_buffer[-1][1] != source_id:
                delay += self.delay
            # Begin sending the next packet in the link after the previous packet is finished traveling
            self.env.add_event(Event("Wait to send to link", self.send), delay)


    def release(self, packet_info):
        packet, source_id = packet_info
        if (source_id == self.device_a.network_id):
            f = self.device_b.receive
        else:
            f = self.device_a.receive
        # Release to device after self.delay time
        self.env.add_event(Event("Send to device", f, packet=packet), self.delay)
