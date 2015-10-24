""" Flow class
"""

# from blackwidow.network.host import Host
from blackwidow.network.packet import DataPacket
from blackwidow.network.packet import AckPacket

class Flow(object):
    """Simple class for flows.
    Flows will trigger host behavior.
    """
    def __init__(self, source, destination, amount):
        """ Constructor for Flow class
        """
        self.src = source
        self.dest = destination
        self.amount = amount
        self.pack_num = 0
        self.cwnd = 1
        self.ssthresh = 10
        self.packets_sent = []

    def send_ack(self, packet):
        """ Creates ack based for packet.
        """
        if self.src == packet.dest and self.dest == packet.src:
            ack_packet = AckPacket(packet.pack_id, packet.dest, packet.src)
        else:
            print "Received wrong packet."
        self.dest.send(ack_packet)

    def send_packet(self):
        """ Send a packet.
        """
        pack = DataPacket(self.pack_num, self.src, self.dest)
        self.packets_sent.append(self.pack_num)
        self.src.send(pack)
        self.pack_num = self.pack_num + 1

    def receive(self, packet):
        """ Generate an ack or respond to bad packet.
        """
        if packet.dest == self.dest:
            self.send_ack(packet)
        else:
            self.respond_to_ack()
            self.packets_sent.remove(packet.pack_id)


    def respond_to_ack(self):
        """ Update window size.
        """
        if self.cwnd < self.ssthresh:
            self.cwnd = self.cwnd + 1
        else:
            self.cwnd = self.cwnd + 1/self.cwnd

    def timeout(self):
        """ Timeout if packet still not received.
        """
        self.ssthresh = self.cwnd/2
        self.cwnd = 1
