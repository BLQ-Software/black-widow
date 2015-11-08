from device import Device

class Host(Device):
    """Simple class for hosts.

    Hosts are mainly responsible for recording their time data.
    They don't trigger events in the simulation, but it will be
    useful to separate host data (end to end data). Flows
    will trigger host behavior.
    """
    def __init__(self, host_id):
        """Constructor for Host class."""
        super(Host, self).__init__(host_id)
        self._flows = []

    def add_flow(self, flow):
        """Add receiving flow to host."""
        self._flows.append(flow)

    def send(self, packet):
        """Connects to a link."""
        self._links[0].receive(packet, self._network_id)

    def receive(self, packet):
        """Send packet to flow to process."""
        for flow in self._flows:
            if packet.flow_id == flow.flow_id:
                flow.receive(packet)
                return
