""" Flow class
"""

from blackwidow.network.host import Host
from blackwidow.network.packet import DataPacket
from blackwidow.network.packet import AckPacket

class Flow(object):
    """Simple class for flows.
    Flows will trigger host behavior.
    """
    def __init__(self, source, destination, amount):
        """ Constructor for Flow class.
        """
        self.src = source
        self.dest = destination
        self.amount = amount
        self.pack_num = 0
        self.env = 0

    def set_env(self, env):
        """ Set the environment.
        """
        self.env = env

    def send_ack(self, packet):
        """ Creates ack based for packet.
        """
        if self.src == packet.dest and self.dest == packet.src:
            ack_packet = AckPacket(packet.pack_id, packet.dest, packet.src)
        else:
            print "Received wrong packet."
        self.src.send(ack_packet)

    def send_packet(self, packet_num):
        """ Send a packet.
        """
        pack = DataPacket(packet_num, self.src, self.dest)
        self.src.send(pack)

    def receive(self, packet):
        """ Generate an ack or respond to bad packet
        """

    def timeout(self, packet_num):
        """ Timeout if packet still not received
        """

