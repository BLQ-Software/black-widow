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
        self.cwnd = 100
        self.ssthresh = 10
        self.packets_sent = []
        self.packets_arrived = set()
        self.env = env
        self.flow_start = time*1000.0
        self.done = False
        self.last_packet = 0

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
        if self.env.time % 1 != 0:
            return
        if self.env.time > self.flow_start and self.amount > 0:
            if (len(self.packets_sent) > self.cwnd):
                self.pack_num = self.packets_sent[0]
            pack = DataPacket(self.pack_num, self.src, self.dest, self.flow_id)
            if (self.pack_num not in self.packets_arrived):
                self.src.send(pack)
                print "Packet {0} sent".format(self.pack_num)
            self.pack_num = self.pack_num + 1
            print "{0} bits left".format(self.amount)
            # Shouldn't subtract pack.size if sent before.
            if (self.pack_num not in self.packets_sent) and (self.pack_num not in self.packets_arrived):
                self.amount = self.amount - pack.size
            if (self.pack_num not in self.packets_sent) and (self.pack_num not in self.packets_arrived):
                self.packets_sent.append(self.pack_num)
        else:
            if self.amount > 0:
                print "Waiting"
            else:
                if (len(self.packets_sent) == 0):
                    self.done = True
                else:
                    self.pack_num = self.packets_sent[0]
                    pack = DataPacket(self.pack_num, self.src, self.dest, self.flow_id)
                    self.src.send(pack)

    def receive(self, packet):
        """ Generate an ack or respond to bad packet.
        """
        if packet.dest == self.dest:
            print "Packet {0} received".format(self.pack_num)
            self.send_ack(packet)
        else:
            #pdb.set_trace()
            self.respond_to_ack()
            if packet.pack_id in self.packets_sent:
                self.packets_sent.remove(packet.pack_id)
            self.packets_arrived.add(packet.pack_id)
            print "Ack received for packet {0}".format(packet.pack_id)
            if self.amount < 0:# and len(self.packets_sent) == 0:
                done = True

    def respond_to_ack(self):
        """ Update window size.
        """
        pass
        if self.cwnd < self.ssthresh:
            self.cwnd = self.cwnd + 1
        else:
            self.cwnd = self.cwnd + 1/self.cwnd

    def timeout(self):
        """ Timeout if packet still not received.
        """
        self.ssthresh = self.cwnd/2
        self.cwnd = 1
