#This file contains the Packet class and its two subclasses,
#DataPacket and AckPacket.

#Constant sizes of packets in bits
DATA_PACKET_SIZE = 1024 * 8
ACK_PACKET_SIZE = 64 * 8
ROUTING_PACKET_SIZE = 64 * 8

class Packet(object):
    """Super class for DataPackets and AckPackets"""
    
    def __init__(self, packet_id, src, dest, flow_id):
        """Constructor for host class"""
        self.pack_id = packet_id
        self.src = src
        self.dest = dest
        self.flow_id = flow_id
        self.is_ack = False
        self.is_routing = False

class DataPacket(Packet):
    """Class for data packets"""
    
    def __init__(self, packet_id, src, dest, flow_id):
        """Constructor for DataPacket class"""
        super(DataPacket, self).__init__(packet_id, src, dest, flow_id)
        self.size = DATA_PACKET_SIZE

class AckPacket(Packet):
    """Class for acknowledgement packets"""
    
    def __init__(self, packet_id, src, dest, flow_id):
        """Constructor for AckPackets class"""
        super(AckPacket, self).__init__(packet_id, src, dest, flow_id)
        self.size = ACK_PACKET_SIZE
        self.is_ack = True

class RoutingPacket(Packet):
    """Class for routing packets"""
    
    def __init__(self, packet_id, src, dest, flow_id, routing_table):
        """Constructor for RoutingPacket class"""
        super(RoutingPacket, self).__init__(packet_id, src, dest, flow_id)
        self.size = ROUTING_PACKET_SIZE
        self.is_routing = True
        self.routing_table = routing_table

