""" Flow class
"""

import pdb
from blackwidow.network.packet import AckPacket, DataPacket
from event import Event

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
        self.cwnd = 1
        self.ssthresh = 10
        self.packets_sent = []
        self.packets_time_out = []
        self.packets_arrived = []
        self.acks_arrived = set()
        self.env = env
        self.flow_start = time*1000.0
        self.last_packet = 0
        self.env.add_event(Event("Start flow", self.send_packet), self.flow_start)

    def send_ack(self, packet):
        """ Creates ack based for packet.
        """
        if self.src == packet.src and self.dest == packet.dest:
            ack_packet = AckPacket(packet.pack_id, packet.dest, packet.src, self.flow_id)
            self.dest.send(ack_packet)
            print "Flow sent ack packet {0}".format(packet.pack_id)
        else:
            print "Received wrong packet."

    def send_packet(self):
        """ Send a packet.
        """
        if self.amount > 0:
            while (len(self.packets_sent) - len(self.packets_time_out) < self.cwnd):
                pack = DataPacket(self.pack_num, self.src, self.dest, self.flow_id)
                if (self.pack_num not in self.acks_arrived):
                    self.src.send(pack)
                    print "Flow sent packet {0}".format(pack.pack_id)
                self.env.add_event(Event("Timeout", self.timeout, pack_num = self.pack_num), 1000)
                # Shouldn't subtract pack.size if sent before.
                if (self.pack_num not in self.packets_sent) and (self.pack_num not in self.acks_arrived):
                    self.amount = self.amount - pack.size
                    self.packets_sent.append(self.pack_num)
                print "Flow has {0} bits left".format(self.amount)
                if self.pack_num in self.packets_time_out:
                    self.packets_time_out.remove(self.pack_num)
                self.pack_num = self.pack_num + 1
                if self.amount <= 0:
                    break
        else:
            # Just keep resending last few packets until done
            while len(self.packets_time_out) > 0:
                self.pack_num = self.packets_time_out[0]
                pack = DataPacket(self.pack_num, self.src, self.dest, self.flow_id)
                self.src.send(pack)
                self.packets_time_out.remove(self.pack_num)
                self.env.add_event(Event("Timeout", self.timeout, pack_num = self.pack_num), 1000)

    def receive(self, packet):
        """ Generate an ack or respond to bad packet.
        """
        if packet.dest == self.dest:
            print "Flow received packet {0}".format(packet.pack_id)
            if packet.pack_id not in self.acks_arrived:
                self.send_ack(packet)
        else:
            if packet.pack_id not in self.acks_arrived:
                self.respond_to_ack()
                if packet.pack_id in self.packets_sent:
                    self.packets_sent.remove(packet.pack_id)
                if packet.pack_id in self.packets_time_out:
                    self.packets_time_out.remove(packet.pack_id)
                self.acks_arrived.add(packet.pack_id)
                print "Flow received ack for packet {0}".format(packet.pack_id)

    def respond_to_ack(self):
        """ Update window size.
        """
        self.env.add_event(Event("Send", self.send_packet), 0)
        if self.cwnd < self.ssthresh:
            self.cwnd = self.cwnd + 1
        else:
            self.cwnd = self.cwnd + 1.0/self.cwnd
        print "Window size is {0}".format(self.cwnd)

    def timeout(self, pack_num):
        """ Timeout if packet still not received.
        """
        if pack_num not in self.acks_arrived:
            self.env.add_event(Event("Resend", self.send_packet), 10)
            # Go back n
            if pack_num not in self.packets_time_out:
                self.packets_time_out.append(pack_num)
            self.pack_num = pack_num
            self.ssthresh = self.cwnd/2
            self.cwnd = 1
            print "Window size is {0}".format(self.cwnd)
