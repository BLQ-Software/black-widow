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
    bw : Blackwidow
        The printer to print data to

    Attributes
    ----------
    flow_id : string
        The flow id.
    src : `Device`
        The source for the flow.
    dest : `Device`
        The destination for the flow.
    amount : int
        The amount of data left to send in MB.
    env : `Network`
        The network that the flow belongs to.
    flow_start : float
        The amount of time to wait before starting to send. Specified in ms.
    pack_num : int
        The next pack_num to check to send.
    cwnd : float
        Congestion window size.
    ssthresh : float
        Slow start threshold
    resend_time : float
        ms before packets are sent after an ack receival
    min_RTT : float
        Minimum round trip time observed for this flow
    last_RTT : float
        Last round trip time observed for this flow
    SRTT : float
        Weighted average of round trip times biased towards recent RTT
    RTTVAR : float
        Variance of round trip times
    RTO : float
        Retransmission timeout in ms
    packets_sent : list
        List of packets that have been sent but haven't had their ack received
    packets_time_out : list
        List of packets that have exceeded timeout and need to be resent
    acks_arrived : set
        Set of ack packets that have been received
    done : int
        0 if flow isn't finished; 1 if flow is finished.
        Used to avoid decrementing flow more than once.
    send_rate : Rate_Graph
        Keeps track of the rate the flow is sending at and outputs to CSV file
        in real time.
    receive_rate : Rate_Graph
        Keeps track of the rate the flow is receiving at and outputs to CSV
        file in real time.
    alpha : float
        alpha in FAST TCP algorithm; alpha = 20 because link rates are between
        10 Mbps and 1 Gbps.
    gamma : float
        gamma in FAST TCP algorithm; smoothing factor for window size
    total_num_pack : int
        total number of packets that need to be sent
    """
    def __init__(self, flow_id, source, destination, amount, env, time, bw):
        """ Constructor for Flow class
        """
        Flow.__init__(self, flow_id, source, destination, amount, env, time,
                      bw)
        self._alpha = 20.0
        self._gamma = 0.8
        self.env.add_event(Event("Start window calc", self._flow_id,
                                 self._update_window),
                           self._flow_start-1)
        self._total_num_pack = (int)(self._amount/(1024*8)) + 1
        self._cwnd = self._alpha
        self._resend_time = 1

    def send_packet(self):
        """ Send a packet. The difference between FastFlow's send_packet and
            Flow's send_packet is the ending behavior. FastFlow just keeps
            resending packets it hasn't received yet until it is done after it
            has sent all the packets once.
        """
        if self._amount > 0 or (len(self._packets_sent) > 0):
            # Send packets up to the window size.
            while (len(self._packets_sent) - len(self._packets_time_out) <
                   self._cwnd):
                pack = DataPacket(self._pack_num, self._src, self._dest,
                                  self._flow_id, timestamp=self.env.time)
                if (self._pack_num not in self._acks_arrived):
                    self._src.send(pack)
                    print "Flow sent packet {0}".format(pack.pack_id)
                    self.bw.record('{0}, {1}'.format(self.env.time, pack.size),
                                   'flow_{0}.sent'.format(self.flow_id))
                    self._send_rate.add_point(pack, self.env.time)
                    self.env.add_event(Event("Timeout",
                                             self._flow_id,
                                             self._timeout,
                                             pack_num=self._pack_num),
                                       self._RTO)
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

                    print ("Flow {} already finished. Received timeout"
                           " at {}.".format(self.flow_id, self.env.time))
                    return

    def _update_window(self):
        """ Send a packet.
        """
        self._cwnd = min((((self._min_RTT / self._last_RTT) *
                          self._cwnd + self._alpha) * self._gamma +
                          (1.0-self._gamma) * self._cwnd), 2 * self._cwnd)
        print "Flow {} window size is {}".format(self._flow_id, self._cwnd)
        self.bw.record('{0}, {1}'.format(self.env.time, self._cwnd),
                       'flow_{0}.window'.format(self.flow_id))
        self.env.add_event(Event("Start window calc",
                                 self._flow_id,
                                 self._update_window),
                           20)

    def _respond_to_ack(self):
        """ Overwrites parent Flow class' method because it shouldn't change
            window size.
        """
        self.env.add_event(Event("Send", self._flow_id, self.send_packet),
                           self._resend_time)

    def _reset_window(self):
        """ This is called when a packet timeout occurs by the parent Flow
            class.
            Does nothing since FAST TCP automatically updates every 20 ms.
        """
        pass
