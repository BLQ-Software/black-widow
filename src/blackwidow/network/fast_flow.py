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
        self._alpha = 10.0

    def _update_window(self):
        self._cwnd = (self._min_RTT/self._last_RTT)*self.cwnd + self._alpha

    def _respond_to_ack(self):
        self.env.add_event(Event("Send", self.send_packet),self._resend_time)

    def _reset_window(self):
        pass
