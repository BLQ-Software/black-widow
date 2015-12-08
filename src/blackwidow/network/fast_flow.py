from blackwidow.network.packet import AckPacket, DataPacket
from event import Event
from flow import Flow

class FastFlow(Flow):
    """ Implements FAST TCP.
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
    def __init__(self, flow_id, source, destination, amount, env, time, bw):
        """ Constructor for Flow class
        """
        Flow.__init__(self, flow_id, source, destination, amount, env, time ,bw)
        self._alpha = 20.0
        self.env.add_event(Event("Start window calc", self._flow_id, self._update_window), self._flow_start-1)
        self._total_num_pack = (int)(self._amount/(1024*8)) + 1
        self._cwnd = self._alpha

    def send_packet(self):
        """ Send a packet.
        """
        if self._amount > 0 or (len(self._packets_sent) > 0):
           # Send packets up to the window size.
            while (len(self._packets_sent) - len(self._packets_time_out) < self._cwnd):
                pack = DataPacket(self._pack_num, self._src, self._dest, self._flow_id, timestamp=self.env.time)
                if (self._pack_num not in self._acks_arrived):
                    self._src.send(pack)
                    print "Flow sent packet {0}".format(pack.pack_id)
                    self.bw.record('{0}, {1}'.format(self.env.time,pack.size), 'flow_{0}.sent'.format(self.flow_id))
                    self._send_rate.add_point(pack, self.env.time)
                    self.env.add_event(Event("Timeout", self._flow_id, self._timeout, pack_num = self._pack_num), self._RTO)
                    # Shouldn't subtract pack.size if sent before.
                    if (self._pack_num not in self._packets_sent):
                        self._amount = self._amount - pack.size
                        self._packets_sent.append(self._pack_num)
                print "Flow has {0} bits left".format(self._amount)
                if self._pack_num in self._packets_time_out:
                    self._packets_time_out.remove(self._pack_num)
                self._pack_num = self._pack_num + 1
                # Ending behavior
                if self._pack_num == self._total_num_pack:
                    self._pack_num = self._packets_sent[0]
                    self._cwnd = self._alpha
                    return

    def _update_window(self):
        self._cwnd = (self._min_RTT/self._last_RTT)*self._cwnd + self._alpha
        print "Flow {} window size is {}".format(self._flow_id, self._cwnd)
        self.bw.record('{0}, {1}'.format(self.env.time, self._cwnd), 'flow_{0}.window'.format(self.flow_id))
        self.env.add_event(Event("Start window calc", self._flow_id, self._update_window), 20)

    def _respond_to_ack(self):
        self.env.add_event(Event("Send", self._flow_id, self.send_packet),self._resend_time)

    def _reset_window(self):
        pass
