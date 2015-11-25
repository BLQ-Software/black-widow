from blackwidow.network.packet import AckPacket, DataPacket
from event import Event
from flow import Flow

class TahoeFlow(Flow):
    """ Implements TCP Tahoe.
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
        self._ms_before_timeout = 1000
        self._ssthresh = 100
        self._packets_arrived = []
        self._packets_arrived = range(0,(int)(self._amount/(1024*8)))
        self._total_num_pack = (int)(self._amount/(1024*8)) + 1
        self._last_pack_rec = -1
        self._counter = 0
