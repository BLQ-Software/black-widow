"""Packet classes
"""
class Packet:
    def __init__(self, pack_id, src, dest, size):
        self.pack_id = pack_id
        self.src = src
        self.dest = dest
        self.size = size


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
