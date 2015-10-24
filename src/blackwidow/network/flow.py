""" Flow class
"""

import pdb
from blackwidow.network.packet import AckPacket, DataPacket

class Flow(object):
    """Simple class for flows.
    Flows will trigger host behavior.
    """
    def __init__(self, flow_id, source, destination, amount, env, time):
        """ Constructor for Flow class
        """
        self.flow_id = flow_id
        self.src = source
        self.dest = destination
        self.amount = amount*8*10**6
        self.pack_num = 0
        self.cwnd = 10
        self.ssthresh = 10
        self.packets_sent = []
        self.env = env
        self.flow_start = time*1000.0
        self.done = False

    def send_ack(self, packet):
        """ Creates ack based for packet.
        """
        if self.src == packet.src and self.dest == packet.dest:
            ack_packet = AckPacket(packet.pack_id, packet.dest, packet.src, self.flow_id)
            self.dest.send(ack_packet)
            print "Ack packet {0} sent".format(self.pack_num)
        else:
            print "Received wrong packet."

    def send_packet(self):
        """ Send a packet.
        """
        if self.env.time > self.flow_start and self.amount > 0 and self.env.time%100 == 0:
            pack = DataPacket(self.pack_num, self.src, self.dest, self.flow_id)
            self.packets_sent.append(self.pack_num)
            self.src.send(pack)
            self.pack_num = self.pack_num + 1
            print "Packet {0} sent".format(self.pack_num)
            print "{0} bits left".format(self.amount)
            self.amount = self.amount - pack.size
        else:
            print "Waiting"

    def receive(self, packet):
        """ Generate an ack or respond to bad packet.
        """
        print "indeed, flow called"
        if packet.dest == self.dest:
            print "Packet {0} received".format(self.pack_num)
            self.send_ack(packet)
        else:
            pdb.set_trace()
            self.respond_to_ack()
            self.packets_sent.remove(packet.pack_id)
            print "Ack received for packet {0}".format(self.pack_num)
            if self.amount < 0 and len(self.packets_sent) == 0:
                done = True

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
