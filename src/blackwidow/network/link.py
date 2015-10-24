

class Link():

    def __init__(self, device_a, device_b, delay, rate, capacity):
        self.rate = rate
        self.delay = delay
        self.capacity = capacity

    def receive(self, packet, source_id):
        pass

    def send(self, packet):
        pass
