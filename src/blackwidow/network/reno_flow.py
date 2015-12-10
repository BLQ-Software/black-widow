from blackwidow.network.packet import AckPacket, DataPacket
from event import Event
from tahoe_flow import TahoeFlow


class RenoFlow(TahoeFlow):
    """ Implements TCP Reno.
    Adds Fast Retransmit and Fast Recovery
    Flows will trigger host behavior.
    Has slow start and congestion avoidance.

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
        0 if flow isn't finished; 1 if flow is finished
        Used to avoid decrementing flow more than once.
    send_rate : Rate_Graph
        Keeps track of the rate the flow is sending at and outputs to CSV file
        in real time.
    receive_rate : Rate_Graph
        Keeps track of the rate the flow is receiving at and outputs to CSV
        file in real time.
    packets_arrived : list
        Keeps track of packets(not acks) that have not arrived. Filled with all
        possible packet numbers when the flow starts and numbers are removed as
        each packet reaches the destination
    total_num_packets : int
        Total number of packets that need to be sent
    last_pack_rec : int
        Packet number of previous next packet expected by the destination
    counter : int
        Keeps track of duplicate acknowledgements
    """
    def __init__(self, flow_id, source, destination, amount, env, time, bw):
        """ Constructor for Flow class
        """
        TahoeFlow.__init__(self, flow_id, source, destination, amount, env,
                           time, bw)
        self._ssthresh = 1000
        self._packets_arrived = []
        self._packets_arrived = range(0, (int)(self._amount/(1024*8)))
        self._total_num_pack = (int)(self._amount/(1024*8)) + 1
        self._last_pack_rec = -1
        self._counter = 0
        self._resend_time = 10

    def _send_ack(self, packet):
        """ Creates ack for packet.
        """
        if self._src == packet.src and self._dest == packet.dest:
            if len(self._packets_arrived) > 0:
                next_ack_expected = self._packets_arrived[0]
            else:
                next_ack_expected = self._total_num_pack
            ack_packet = AckPacket(packet.pack_id, packet.dest, packet.src,
                                   self._flow_id, next_ack_expected,
                                   timestamp=packet.timestamp)
            self._dest.send(ack_packet)
            print "Flow sent ack packet {0}".format(packet.pack_id)
        else:
            print "Received wrong packet."

    def receive(self, packet):
        """ Generate an ack or respond to bad packet.
        Parameters
        ----------
        packet : `Packet`
            The packet to be received.
        """
        if packet.dest == self._dest:
            print "Flow received packet {0}".format(packet.pack_id)
            if packet.pack_id in self._packets_arrived:
                self._packets_arrived.remove(packet.pack_id)
            self._send_ack(packet)
        else:
            # Check for duplicate acknowledgements
            if packet.next_expected == self._last_pack_rec:
                self._counter = self._counter + 1
            else:
                if self._counter >= 3:
                    # window deflation on non-dup ACK
                    self._cwnd = self._ssthresh
                    print ("Flow {} window size is {} -"
                           " fast retransmit".format(self._flow_id,
                                                     self._cwnd))
                    self.bw.record('{0}, {1}'.format(self.env.time,
                                                     self._cwnd),
                                   'flow_{0}.window'.format(self.flow_id))
                self._counter = 0
                self._last_pack_rec = packet.next_expected
            # Fast retransmit/Fast recovery
            if self._counter == 3:
                if self._cwnd > 4:
                    self._ssthresh = self._cwnd/float(2)
                else:
                    self._ssthresh = 2.0
                # Go back n
                self._pack_num = packet.next_expected
                # window inflation where ndup = 3
                self._cwnd = self._ssthresh + self._counter
                if packet.next_expected not in self._packets_time_out:
                    self._packets_time_out.append(packet.next_expected)
                self.env.add_event(Event("Resend",
                                         self._flow_id,
                                         self.send_packet),
                                   100)
                print ("Flow {} window size is {} -"
                       " fast retransmit".format(self._flow_id, self._cwnd))
                self.bw.record('{0}, {1}'.format(self.env.time, self._cwnd),
                               'flow_{0}.window'.format(self.flow_id))
            self._receive_ack(packet)

    def _reset_window(self):
        """ Called when a packet timeout occurs.
            Sets ssthresh to max(2, cwnd/2) and cwnd to 1.
            Resets counter
        """
        super(RenoFlow, self)._reset_window()
        self._counter = 0
