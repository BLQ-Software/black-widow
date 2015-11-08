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
        self._pack_id = packet_id
        self._src = src
        self._dest = dest
        self._flow_id = flow_id
        self._is_ack = False
        self._is_routing = False
        self._size = 0
    def __str__(self):
        msg = ""
        if self._is_ack:
            msg += "ACK "
        msg += "Packet {0} sending from {1} to {2}"
        return msg.format(self._pack_id, self._src.network_id, self._dest.network_id)

    @property
    def pack_id(self):
        return self._pack_id

    @pack_id.setter
    def pack_id(self, value):
        raise AttributeError("Cannot modify packet id: {0}".format(self._pack_id))

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, value):
        raise AttributeError("Cannot modify packet source: {0}".format(self._src))

    @property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, value):
        raise AttributeError("Cannot modify packet id: {0}".format(self._dest))

    @property
    def flow_id(self):
        return self._flow_id

    @flow_id.setter
    def flow_id(self, value):
        raise AttributeError("Cannot modify packet flow id: {0}".format(self._dest))

    @property
    def is_ack(self):
        return self._is_ack

    @is_ack.setter
    def is_ack(self, value):
        raise AttributeError("Cannot modify packet type: {0}".format(self._pack_id))

    @property
    def is_routing(self):
        return self._is_routing

    @is_routing.setter
    def is_routing(self, value):
        raise AttributeError("Cannot modify packet type: {0}".format(self._pack_id))

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        raise AttributeError("Cannot modify packet size: {0}".format(self._pack_id))

class DataPacket(Packet):
    """Class for data packets"""

    def __init__(self, packet_id, src, dest, flow_id):
        """Constructor for DataPacket class"""
        super(DataPacket, self).__init__(packet_id, src, dest, flow_id)
        self._size = DATA_PACKET_SIZE

class AckPacket(Packet):
    """Class for acknowledgement packets"""

    def __init__(self, packet_id, src, dest, flow_id):
        """Constructor for AckPackets class"""
        super(AckPacket, self).__init__(packet_id, src, dest, flow_id)
        self._size = ACK_PACKET_SIZE
        self._is_ack = True

class RoutingPacket(Packet):
    """Class for routing packets"""

    def __init__(self, packet_id, src, dest, flow_id, routing_table):
        """Constructor for RoutingPacket class"""
        super(RoutingPacket, self).__init__(packet_id, src, dest, flow_id)
        self._size = ROUTING_PACKET_SIZE
        self._is_routing = True
        self._routing_table = routing_table
