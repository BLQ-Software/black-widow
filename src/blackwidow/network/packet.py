# This file contains the Packet class and its two subclasses,
# DataPacket and AckPacket.

# Constant sizes of packets in bits
DATA_PACKET_SIZE = 1024 * 8
ACK_PACKET_SIZE = 64 * 8 * 0


class Packet(object):
    """Super class for DataPackets and AckPackets

    Parameters
    ----------
    packet_id : int
        A unique id for the packet within a flow
    src : Device
        The device a packet originated from
    dest : Device
        The destination of the packet
    flow_id : string
        The flow_id of the flow this packet is in
    timestamp : float, optional
        The default value is 0 when this parameter is not used. This is used
        to track when the packet or the packet this is associated with if it
        is an ack was sent.  This parameter is used to calculate round trip
        time in flow.

    Attributes
    ----------
    pack_id : int
        The packet id or the id of the packet an ack is associated with.
    src : Device
        The device a packet originated from
    dest : Device
        The destination of the packet
    flow_id : string
        The flow_id of the flow this packet is in
    timestamp : float, optional
        The default value is 0 when this parameter is not used. This is used
        to track when the packet or the packet this is associated with if it
        is an ack was sent.  This parameter is used to calculate round trip
        time in flow.
    is_ack : boolean
        True if ack packet; False otherwise.
    is_routing : boolean
        True if routing packet; False otherwise.
    size : int
        Size in bits of packet.
    """

    def __init__(self, packet_id, src, dest, flow_id, timestamp=0):
        """ Constructor for host class
        """
        self._pack_id = packet_id
        self._src = src
        self._dest = dest
        self._flow_id = flow_id
        self._is_ack = False
        self._is_routing = False
        self._size = 0
        self._timestamp = timestamp

    def __str__(self):
        """ Returns a string of which packet is being sent and where.
            Called by link.
        """
        msg = ""
        if self._is_ack:
            msg += "ACK "
        msg += "Packet {0} sending from {1} to {2}"
        return msg.format(self._pack_id, self._src.network_id,
                          self._dest.network_id)

    @property
    def timestamp(self):
        return self._timestamp

    @timestamp.setter
    def timestamp(self, value):
        raise AttributeError("Cannot modify"
                             " timestamp: {0}".format(self._pack_id))

    @property
    def pack_id(self):
        return self._pack_id

    @pack_id.setter
    def pack_id(self, value):
        raise AttributeError("Cannot modify packet"
                             " id: {0}".format(self._pack_id))

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, value):
        raise AttributeError("Cannot modify packet"
                             " source: {0}".format(self._src))

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
        raise AttributeError("Cannot modify packet"
                             " flow id: {0}".format(self._dest))

    @property
    def is_ack(self):
        return self._is_ack

    @is_ack.setter
    def is_ack(self, value):
        raise AttributeError("Cannot modify packet"
                             " type: {0}".format(self._pack_id))

    @property
    def is_routing(self):
        return self._is_routing

    @is_routing.setter
    def is_routing(self, value):
        raise AttributeError("Cannot modify packet"
                             " type: {0}".format(self._pack_id))

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, value):
        raise AttributeError("Cannot modify packet"
                             " size: {0}".format(self._pack_id))


class DataPacket(Packet):
    """Class for data packets

    Parameters
    ----------
    packet_id : int
        A unique id for the packet within a flow
    src : Device
        The device a packet originated from
    dest : Device
        The destination of the packet
    flow_id : string
        The flow_id of the flow this packet is in
    timestamp : float, optional
        The default value is 0 when this parameter is not used. This is used
        to track when the packet or the packet this is associated with if it
        is an ack was sent.  This parameter is used to calculate round trip
        time in flow.

    Attributes
    ----------
    pack_id : int
        The packet id or the id of the packet an ack is associated with.
    src : Device
        The device a packet originated from
    dest : Device
        The destination of the packet
    flow_id : string
        The flow_id of the flow this packet is in
    timestamp : float, optional
        The default value is 0 when this parameter is not used. This is used
        to track when the packet or the packet this is associated with if it
        is an ack was sent.  This parameter is used to calculate round trip
        time in flow.
    is_ack : boolean
        True if ack packet; False otherwise.
    is_routing : boolean
        True if routing packet; False otherwise.
    size : int
        Size in bits of packet.
    """

    def __init__(self, packet_id, src, dest, flow_id, timestamp=0):
        """Constructor for DataPacket class"""
        super(DataPacket, self).__init__(packet_id, src, dest, flow_id,
                                         timestamp)
        self._size = DATA_PACKET_SIZE


class AckPacket(Packet):
    """Class for acknowledgement packets

    Parameters
    ----------
    packet_id : int
        A unique id for the packet within a flow
    src : Device
        The device a packet originated from
    dest : Device
        The destination of the packet
    flow_id : string
        The flow_id of the flow this packet is in
    next_expected_id : int
        The next packet that the destination expects from the source.
    timestamp : float, optional
        The default value is 0 when this parameter is not used. This is used
        to track when the packet or the packet this is associated with if it
        is an ack was sent.  This parameter is used to calculate round trip
        time in flow.

    Attributes
    ----------
    pack_id : int
        The packet id or the id of the packet an ack is associated with.
    src : Device
        The device a packet originated from
    dest : Device
        The destination of the packet
    flow_id : string
        The flow_id of the flow this packet is in
    timestamp : float, optional
        The default value is 0 when this parameter is not used. This is used
        to track when the packet or the packet this is associated with if it
        is an ack was sent.  This parameter is used to calculate round trip
        time in flow.
    is_ack : boolean
        True if ack packet; False otherwise.
    is_routing : boolean
        True if routing packet; False otherwise.
    size : int
        Size in bits of packet.
    next_expected_id : int
        The next packet that the destination expects from the source.
    """

    @property
    def next_expected(self):
        return self._next_expected

    @next_expected.setter
    def next_expected(self, value):
        raise AttributeError("Cannot modify ack"
                             " data: {0}".format(self._pack_id))

    def __init__(self, packet_id, src, dest, flow_id, next_expected_id=0,
                 timestamp=0):
        """Constructor for AckPackets class"""
        super(AckPacket, self).__init__(packet_id, src, dest, flow_id,
                                        timestamp)
        self._size = ACK_PACKET_SIZE
        self._is_ack = True
        self._next_expected = next_expected_id


class RoutingPacket(Packet):
    """Class for routing packets

    Parameters
    ----------
    packet_id : int
        A unique id for the packet within a flow
    src : Device
        The device a packet originated from
    dest : Device
        The destination of the packet
    flow_id : string
        The flow_id of the flow this packet is in
    routing_table : dictionary
        Routing table to be updated

    Attributes
    ----------
    pack_id : int
        The packet id or the id of the packet an ack is associated with.
    src : Device
        The device a packet originated from
    dest : Device
        The destination of the packet
    flow_id : string
        The flow_id of the flow this packet is in
    timestamp : float, optional
        The default value is 0 when this parameter is not used. This is used
        to track when the packet or the packet this is associated with if it
        is an ack was sent.  This parameter is used to calculate round trip
        time in flow.
    is_ack : boolean
        True if ack packet; False otherwise.
    is_routing : boolean
        True if routing packet; False otherwise.
    size : int
        Size in bits of packet.
    routing_table : dictionary
        Routing table to be updated
    """

    def __init__(self, packet_id, src, dest, flow_id, routing_table, size):
        """Constructor for RoutingPacket class"""
        super(RoutingPacket, self).__init__(packet_id, src, dest, flow_id)
        self._size = size
        self._is_routing = True
        self._routing_table = routing_table

    @property
    def routing_table(self):
        return self._routing_table

    @routing_table.setter
    def routing_table(self, value):
        raise AttributeError("Cannot modify"
                             " routing table: {0}".format(self._pack_id))
