from collections import deque


class Link():

    def __init__(self, device_a, device_b, delay, rate, capacity, env):
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
        self.env = env

    def receive(self, packet, source_id):
        # Add packet to link buffer as soon as it is received.
        # Drop packet if the buffer is full
        if len(self.release_into_link_buffer) < capacity:
            self.release_into_link_buffer.appendleft(
                [packet, source_id, self.env.time])

    def send(self):
        # Release into link
        if (len(self.release_into_link_buffer) > 0):
            # Peek at head
            packet_info = self.release_into_link_buffer[-1]
            # Copy packet info fields.
            packet = packet_info[0]
            source_id = packet_info[1]
            start_time = packet_info[2]
            # Check if packet has been sent by router.
            if (network.time - start_time >= packet.size / self.rate):
                # Add it to queue of packets traveling through link.
                # Update the current packet time to the send time
                self.release_to_device_buffer.appendLeft(
                    [packet, source_id, self.env.time])
                # Remove current packet from bufer
                self.release_into_link_buffer.pop()
                # Update next packet time arrival time at front of queue
                if (len(self.release_into_link_buffer) > 0):
                    self.release_into_link_buffer[-1][2] = self.env.time

        # Release to device
        if (len(self.release_to_device_buffer) > 0):
            packet_info = self.release_to_device_buffer[-1]
            # Copy packet info fields.
            packet = packet_info[0]
            source_id = packet_info[1]
            start_time = packet_info[2]
            # Check if packet has arrived at end of link.
            if (network.time - start_time >= self.delay):
                # Figure out which device to send to and send
                if (source_id == device_a.network_id):
                    self.device_a.receive(packet)
                elif (source_id == device_b.network_id):
                    self.device_b.receive(packet)
                # Remove currenet packet from buffer
                self.release_to_device_buffer.pop()
