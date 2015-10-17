"""Packet classes
"""
class Packet(object):
    def __init__(self, pack_id, src, dest, size):
        self.pack_id = pack_id
        self.src = src
        self.dest = dest
        self.size = size
        self.ack = 0

    def is_ack(self):
        """ Returns 0 if not ack packet.
        """
        pass


class DataPacket(Packet):
    def __init__(self, pack_id, src, dest):
        self.pack_id = pack_id
        self.src = src
        self.dest = dest
        self.size = 1024*8

class AckPacket(Packet):
    def __init__(self, pack_id, src, dest):
        self.pack_id = pack_id
        self.src = src
        self.dest = dest
        self.size = 64*8
        self.ack = 1
