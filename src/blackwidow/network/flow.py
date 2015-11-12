from blackwidow.network.packet import AckPacket, DataPacket
from event import Event

class Flow(object):
    """Simple class for flows.
    Flows will trigger host behavior.

    Parameters
    ----------
    flow_id : string
        A unique id for the flow.
    source : `Device`
        The source for the flow.
    destination : `Device`
        The destination for the flow.
    amount : int
        The amount of data to send in MB.
    env : `Network`
        The network that the flow belongs to.
    time : float
        The amount of time to wait before starting to send in ms.

    """
    def __init__(self, flow_id, source, destination, amount, env, time):
        """ Constructor for Flow class
        """
        self._flow_id = flow_id
        self._src = source
        self._dest = destination
        self._amount = amount*8*10**6
        self._pack_num = 0
        self._cwnd = 1
        self._ssthresh = 10
        self._packets_sent = []
        self._packets_time_out = []
        self._packets_arrived = []
        self._acks_arrived = set()
        self.env = env
        self._flow_start = time*1000.0
        self._last_packet = 0
        self.env.add_event(Event("Start flow", self.send_packet), self._flow_start)

    @property
    def flow_id(self):
        return self._flow_id

    @flow_id.setter
    def flow_id(self, value):
        raise AttributeError("Cannot change flow id: {0}".format(self._flow_id))

    @property
    def src(self):
        return self._src

    @src.setter
    def src(self, value):
        raise AttributeError("Cannot change flow source: {0}".format(self._flow_id))

    @property
    def dest(self):
        return self._dest

    @dest.setter
    def dest(self, value):
        raise AttributeError("Cannot change flow destination: {0}".format(self._flow_id))



    def __str__(self):
        msg = "Flow {0}, sending from {1} to {2}"
        return msg.format(self._flow_id, self._src.network_id, self._dest.network_id)

    def _send_ack(self, packet):
        """ Creates ack based for packet.
        """
        if self._src == packet.src and self._dest == packet.dest:
            ack_packet = AckPacket(packet.pack_id, packet.dest, packet.src, self._flow_id)
            self._dest.send(ack_packet)
            print "Flow sent ack packet {0}".format(packet.pack_id)
        else:
            print "Received wrong packet."

    def send_packet(self):
        """ Send a packet.
        """
        if self._amount > 0:
            while (len(self._packets_sent) - len(self._packets_time_out) < self._cwnd):
                pack = DataPacket(self._pack_num, self._src, self._dest, self._flow_id)
                if (self._pack_num not in self._acks_arrived):
                    self._src.send(pack)
                    print "Flow sent packet {0}".format(pack.pack_id)
                self.env.add_event(Event("Timeout", self._timeout, pack_num = self._pack_num), 1000)
                # Shouldn't subtract pack.size if sent before.
                if (self._pack_num not in self._packets_sent) and (self._pack_num not in self._acks_arrived):
                    self._amount = self._amount - pack.size
                    self._packets_sent.append(self._pack_num)
                print "Flow has {0} bits left".format(self._amount)
                if self._pack_num in self._packets_time_out:
                    self._packets_time_out.remove(self._pack_num)
                self._pack_num = self._pack_num + 1
                if self._amount <= 0:
                    break
        else:
            # Just keep resending last few packets until done
            while len(self._packets_time_out) > 0:
                self._pack_num = self._packets_time_out[0]
                pack = DataPacket(self._pack_num, self._src, self._dest, self._flow_id)
                self._src.send(pack)
                self._packets_time_out.remove(self._pack_num)
                self.env.add_event(Event("Timeout", self._timeout, pack_num = self._pack_num), 1000)

    def receive(self, packet):
        """ Generate an ack or respond to bad packet.

        Parameters
        ----------
        packet : `Packet`
            The packet to be received.

        """
        if packet.dest == self._dest:
            print "Flow received packet {0}".format(packet.pack_id)
            if packet.pack_id not in self._acks_arrived:
                self._send_ack(packet)
        else:
            if packet.pack_id not in self._acks_arrived:
                self._respond_to_ack()
                if packet.pack_id in self._packets_sent:
                    self._packets_sent.remove(packet.pack_id)
                if packet.pack_id in self._packets_time_out:
                    self._packets_time_out.remove(packet.pack_id)
                self._acks_arrived.add(packet.pack_id)
                print "Flow {} received ack for packet {}".format(self._flow_id, packet.pack_id)
                if len(self._packets_sent) + len(self._acks_arrived) == 0:
                    self.env.decrement_flows()

    def _respond_to_ack(self):
        """ Update window size.
        """
        self.env.add_event(Event("Send", self.send_packet), 0)
        if self._cwnd < self._ssthresh:
            self._cwnd = self._cwnd + 1
        else:
            self._cwnd = self._cwnd + 1.0/self._cwnd
        print "Flow {} window size is {}".format(self._flow_id, self._cwnd)

    def _timeout(self, pack_num):
        """ Generate an ack or respond to bad packet.

        Parameters
        ----------
        pack_num : `Packet`number
            The packet number of the packet to check for timeout.

        """
        if pack_num not in self._acks_arrived:
            self.env.add_event(Event("Resend", self.send_packet), 10)
            # Go back n
            if pack_num not in self._packets_time_out:
                self._packets_time_out.append(pack_num)
            self._pack_num = pack_num
            self._ssthresh = self._cwnd/2
            self._cwnd = 1
            print "Flow {} window size is {}".format(self._flow_id, self._cwnd)
