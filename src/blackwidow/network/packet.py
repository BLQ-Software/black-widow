#This file contains the Packet class and its two subclasses,
#DataPacket and AckPacket.

#Constant sizes of packets in bits
DATA_PACKET_SIZE = 1024 * 8
ACK_PACKET_SIZE = 64 * 8

class Packet(object):
    """Super class for DataPackets and AckPackets"""
    
    def __init__(self, packet_id, src, dest, size):
        """Constructor for host class"""
        self.pack_id = pack_id
        self.src = src
        self.dest = dest   

class DataPacket(Packet):
    """Class for data packets"""
    
    def __init__(self, size, ack):
        """Constructor for DataPacket class"""
        super(Packet, self).__init__()
        self.size = DATA_PACKET_SIZE
        self.is_ack = False

class AckPacket(Packet):
    """Class for acknowledgement packets"""
    
    def __init__(self, pack_id, src, dest):
        """Constructor for AckPackets class"""
        self.size = ACK_PACKET_SIZE
        self.is_ack = True
