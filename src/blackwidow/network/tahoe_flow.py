from blackwidow.network.packet import AckPacket, DataPacket
from event import Event
from flow import Flow


class TahoeFlow(Flow):
    """ Implements TCP Tahoe.
    Flows will trigger host behavior.
    Slow start and congestion avoidance already implemented in Flow.
    Just sets parameters for TCP Tahoe

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
    """
    def __init__(self, flow_id, source, destination, amount, env, time, bw):
        """ Constructor for Flow class
        """
        Flow.__init__(self, flow_id, source, destination, amount, env, time,
                      bw)
        self._ssthresh = 9999
        self._resend_time = 100
