from blackwidow.network.packet import AckPacket, DataPacket
from blackwidow.network.rate_graph import Rate_Graph
from event import Event

# Variables for timeout calculation from
# https://tools.ietf.org/html/rfc6298
K = 4.0
alpha = 1.0/8.0
beta = 1.0/4.0
# clock granularity
G = 1.0

class Flow(object):
    """Simple class for flows.
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
        The amount of time to wait before starting to send. Specified in ms.
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
        0 if flow isn't finished; 1 if flow is finished; used to avoid decrementing flow more than once
    send_rate : Rate_Graph
        Keeps track of the rate the flow is sending at and outputs to CSV file in real time
    receive_rate : Rate_Graph
        Keeps track of the rate the flow is receiving at and outputs to CSV file in real time 
    """

    def __init__(self, flow_id, source, destination, amount, env, time, bw):
        """ Constructor for Flow class
        """
        self._flow_id = flow_id
        self._src = source
        self._dest = destination
        self._amount = amount*8*10**6
        self._pack_num = 0
        self._cwnd = 1.0
        self._ssthresh = 1000
        self._resend_time = 10
        self._min_RTT = 1000.0
        self._last_RTT = 3000.0
        self._SRTT = -1
        self._RTTVAR = 0
        self._RTO = 3000
        self._packets_sent = []
        self._packets_time_out = []
        self._acks_arrived = set()
        self.env = env
        self.bw = bw
        self._flow_start = time*1000.0
        self._last_packet = 0
        self._done = 0
        self._send_rate = Rate_Graph(self._flow_id, "flow {0} send rate".format(self.flow_id), self.env, self.bw)
        self._receive_rate = Rate_Graph(self._flow_id, "flow {0} receive rate".format(self.flow_id), self.env, self.bw)
        self.env.add_event(Event("Start flow", self._flow_id, self.send_packet), self._flow_start)

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

    @property
    def amount(self):
        return self._amount

    @amount.setter
    def amount(self, value):
        raise AttributeError("Cannot change flow amount: {0}".format(self._flow_id))

    @property
    def flow_start(self):
        return self._flow_start

    @flow_start.setter
    def flow_start(self, value):
        raise AttributeError("Cannot change flow start: {0}".format(self._flow_id))



    def __str__(self):
        msg = "Flow {0}, sending from {1} to {2}"
        return msg.format(self._flow_id, self._src.network_id, self._dest.network_id)

    def _send_ack(self, packet):
        """ Creates ack for packet.
        """
        if self._src == packet.src and self._dest == packet.dest:
            ack_packet = AckPacket(packet.pack_id, packet.dest, packet.src, self._flow_id, timestamp=packet.timestamp)
            self._dest.send(ack_packet)
            print "Flow sent ack packet {0}".format(packet.pack_id)
        else:
            print "Received wrong packet."

    def send_packet(self):
        """ Send a packet.
        """
        if self._amount > 0:
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
                if self._amount <= 0:
                    break
        else:
            # Just keep resending last few packets until done
            while len(self._packets_time_out) > 0:
                self._pack_num = self._packets_time_out[0]
                pack = DataPacket(self._pack_num, self._src, self._dest, self._flow_id, timestamp=self.env.time)
                self._src.send(pack)
                self._send_rate.add_point(pack, self.env.time)
                self._packets_time_out.remove(self._pack_num)
                self.env.add_event(Event("Timeout", self._flow_id, self._timeout, pack_num = self._pack_num), self._RTO)

    def receive(self, packet):
        """ Generate an ack or respond to bad packet.
        Parameters
        ----------
        packet : `Packet`
            The packet to be received.
        """
        # Packet arrived at destination.  Send ack.
        if packet.dest == self._dest:
            print "Flow received packet {0}".format(packet.pack_id)
            if packet.pack_id not in self._acks_arrived:
                self._send_ack(packet)
        # Ack arrived at source. Update window size.
        else:
            self._receive_ack(packet)

    def _receive_ack(self, packet):
        if packet.pack_id not in self._acks_arrived:
            self._respond_to_ack()
            self._update_RTT(packet)
            # Update lists by removing pack_id
            if packet.pack_id in self._packets_sent:
                self._packets_sent.remove(packet.pack_id)
            if packet.pack_id in self._packets_time_out:
                self._packets_time_out.remove(packet.pack_id)
            # Update which acks have arrived
            self._acks_arrived.add(packet.pack_id)
            print "Flow {} received ack for packet {}".format(self._flow_id, packet.pack_id)
            self.bw.record('{0}, {1}'.format(self.env.time,packet.size), 'flow_{0}.received'.format(self.flow_id))
            self._receive_rate.add_point(packet, self.env.time)
            # Check if done
            if len(self._packets_sent) == 0 and self._amount <= 0 and self._done == 0:
                self.env.decrement_flows()
                self._done = 1

    def _respond_to_ack(self):
        """ Update window size.
        """
        self.env.add_event(Event("Send", self._flow_id, self.send_packet), self._resend_time)
        if self._cwnd < self._ssthresh:
            self._cwnd = self._cwnd + 1.0
        else:
            self._cwnd = self._cwnd + 1.0/self._cwnd
        print "Flow {} window size is {}".format(self._flow_id, self._cwnd)
        self.bw.record('{0}, {1}'.format(self.env.time, self._cwnd), 'flow_{0}.window'.format(self.flow_id))

    def _update_RTT(self, packet):
        """ Update last RTT and min RTT and retransmission timeout.
        Parameters
        ----------
        packet : `Packet`
            The packet that was received. Need this to get the timestamp
        """
        self._last_RTT = self.env.time - packet.timestamp
        if self._SRTT == -1:
            self._SRTT = self._last_RTT
            self._RTTVAR  = self._last_RTT/2.0
        else:
            self._RTTVAR = (1.0 - beta)*self._RTTVAR + beta*abs(self._SRTT - self._last_RTT)
            self._SRTT = (1.0 - alpha)*self._SRTT + alpha*self._last_RTT
        self._RTO = min(max(self._SRTT + max(G, K*self._RTTVAR), 1000), 5000)
        print "RTO is {}".format(self._RTO)
        if self._last_RTT < self._min_RTT:
            self._min_RTT = self._last_RTT
        self.bw.record('{0}, {1}'.format(self.env.time, self._last_RTT - self._min_RTT), 'flow_{0}.packet_delay'.format(self.flow_id))

    def _timeout(self, pack_num):
        """ Generate an ack or respond to bad packet.
        Parameters
        ----------
        pack_num : `Packet`number
            The packet number of the packet to check for timeout.
        """
        if pack_num not in self._acks_arrived:
            self.env.add_event(Event("Resend", self._flow_id, self.send_packet), self._resend_time)
            # Go back n
            if pack_num not in self._packets_time_out:
                self._packets_time_out.append(pack_num)
            self._pack_num = pack_num
            self._reset_window()

    def _reset_window(self):
        """ Called when a packet timeout occurs.
            Sets ssthresh to max(2, cwnd/2) and cwnd to 1.
        """
        if self._cwnd > 4:
            self._ssthresh = self._cwnd / float(2)
        else:
            self._ssthresh = 2.0
        self._cwnd = 1.0
        print "Flow {} window size is {}".format(self._flow_id, self._cwnd)
        self.bw.record('{0}, {1}'.format(self.env.time, self._cwnd), 'flow_{0}.window'.format(self.flow_id))
