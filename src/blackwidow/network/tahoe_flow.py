from blackwidow.network.packet import AckPacket, DataPacket
from event import Event
from flow import Flow

class TahoeFlow(Flow):
    """ Implements TCP Tahoe.
    Adds Fast Retransmit
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

    """
    def __init__(self, flow_id, source, destination, amount, env, time, bw):
        """ Constructor for Flow class
        """
        Flow.__init__(self, flow_id, source, destination, amount, env, time ,bw)
        self._packets_arrived = []
        self._packets_arrived = range(0,(int)(self._amount/(1024*8))) 
        self._total_num_pack = (int)(self._amount/(1024*8)) + 1
        self._last_pack_rec = -1
        self._counter = 0

    def _send_ack(self, packet):
        """ Creates ack for packet.
        """
        if self._src == packet.src and self._dest == packet.dest:
            if len(self._packets_arrived) > 0:
                next_ack_expected = self._packets_arrived[0]
            else:
                next_ack_expected = self._total_num_pack
            ack_packet = AckPacket(packet.pack_id, packet.dest, packet.src, self._flow_id, next_ack_expected)
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
            self._receive_ack(packet)
