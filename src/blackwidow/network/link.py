import network
from collections import deque
import packet

class Link():

    def __init__(self, device_a, device_b, delay, rate, capacity):
        self.device_a = device_a
        self.device_b = device_b
        # rate is initially Mbps. rate is stored as bits per ms.
        self.rate = rate * 10 ** 9
        self.delay = delay
        self.capacity = capacity
        # Buffer to enter link
        self.release_into_link_buffer = deque()
        # Packets that are traveling through the link
        self.release_to_device_buffer = deque()

    def receive(self, packet, source_id):
        # Add packet to link buffer as soon as it is received.
        if len(release_into_link_buffer) < capacity:
            release_into_link_buffer.appendleft([packet, source_id, network.time])

    def send(self):
        # Release into link
        if (len(release_into_link_buffer) > 0):
            # Peak at head
            packet_info = release_into_link_buffer[-1]
            packet = packet_info[0]
            source_id = packet_info[1]
            start_time = packet_info[2]
            # Check if packet has been sent by router.
            if (network.time - start_time >= packet.size / self.rate):
                # Add it to queue of packets traveling through link.
                release_to_device_buffer.appendLeft([packet, source_id, network.time]);
                release_into_link_buffer.pop()
                # Update's packet time
                if (len(release_into_link_buffer) > 0):
                    release_into_link_buffer[-1][2] = network.time

        # Release to device
        if (len(release_to_device_buffer) > 0):
            packet_info = release_to_device_buffer[-1]
            packet = packet_info[0]
            source_id = packet_info[1]
            start_time = packet_info[2]
            if (network.time - start_time >= self.delay):
                if (source_id == device_a.network_id):
                    device_a.receive(packet)
                elif (source_id == device_b.network_id):
                    device_b.receive(packet)
                release_to_device_buffer.pop()
