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
        self.release_into_link_buffer = deque()
        self.release_to_device_buffer = deque()

    def receive(self, packet, source_id):
        if len(release_into_link_buffer) < capacity:
            release_into_link_buffer.appendleft([packet, source_id, network.time])

    def send(self, packet):
        # Release into link
        if (len(release_into_link_buffer) > 0):
            packet_info = release_into_link_buffer[-1]
            packet = packet_info[0]
            source_id = packet_info[1]
            start_time = packet_info[2]
            if (network.time - start_time >= packet.size / self.rate):
                release_to_device_buffer.appendLeft([packet, source_id, network.time]);
                release_into_link_buffer.pop()
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
