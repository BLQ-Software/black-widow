""" Flow class
"""

from blackwidow.network.packet import DataPacket
from blackwidow.network.packet import AckPacket

class Flow(object):
    """Simple class for flows.
    Flows will trigger host behavior.
    """
    def __init__(self, env, source, destination, amount):
        """ Constructor for Flow class.
        """
        self.src = source
        self.dest = destination
        self.amount = amount
        self.pack_num = 0
        self.env = env

    def make_packet(self, packet_num):
        """ Creates a packet with specified number.
        """
        pack = DataPacket(packet_num, self.src, self.dest)
        return pack

    def make_ack(self, packet):
        """ Creates ack based for packet.
        """
        if self.src == packet.dest and self.dest == packet.src:
            ack_packet = AckPacket(packet.pack_id, packet.dest, packet.src)
        else:
            print "Received wrong packet."
        return ack_packet

    def send_packet(self, packet):
        """ Send a packet.
        """

    def received_packet(self, event):
        """ Generate an ack or respond to bad packet
        """

    def timeout(self, packet_num):
        """ Timeout if packet still not received
        """

