from collections import deque


class Link():

    def __init__(self, id, device_a, device_b, delay, rate, capacity, env):
        self.id = id
        self.device_a = device_a
        self.device_b = device_b

        # rate is initially Mbps. rate is stored as bits per ms.
        self.rate = rate * 10 ** 9
        self.delay = delay
        self.capacity = capacity * 1000 * 8

        # Buffer to enter link
        self.release_into_link_buffer = deque()

        # Packets that are traveling through the link
        self.release_to_device_buffer = deque()

        self.env = env
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
                [packet, source_id, self.env.time])
            self.size += packet.size
        else:
            print "Packet dropped."

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
            if (self.env.time - start_time >= packet.size / self.rate):
                # Add it to queue of packets traveling through link.
                # Update the current packet time to the send time
                self.release_to_device_buffer.appendleft(
                    [packet, source_id, self.env.time])
                message = "I am link {0}. I have released "
                if (packet.is_ack):
                    message += "ACK "
                message += "packet {1} to my link at time {2}"
                print message.format(self.id, packet.pack_id, self.env.time)
                # Remove current packet from bufer
                self.release_into_link_buffer.pop()
                self.size -= packet.size
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
            if (self.env.time - start_time >= self.delay):
                # Figure out which device to send to and send
                message = "I am link {0}. I have released "
                if (packet.is_ack):
                    message += "ACK "
                message += "packet {1} to {2} at time {3}"
                if (source_id == self.device_a.network_id):
                    self.device_b.receive(packet)
                    print message.format(self.id, packet.pack_id, self.device_b.network_id, self.env.time)
                elif (source_id == self.device_b.network_id):
                    self.device_a.receive(packet)
                    print message.format(self.id, packet.pack_id, self.device_a.network_id, self.env.time)
                # Remove currenst packet from buffer
                self.release_to_device_buffer.pop()
