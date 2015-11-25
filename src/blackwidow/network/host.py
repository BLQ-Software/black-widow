from device import Device

class Host(Device):
    """Simple class for hosts.

    Hosts are mainly responsible for recording their time data.
    They don't trigger events in the simulation, but it will be
    useful to separate host data (end to end data). Flows
    will trigger host behavior.

    Parameters
    ----------
    host_id : string
        A unique id for the host.

    """
    def __init__(self, host_id):
        """Constructor for Host class."""
        super(Host, self).__init__(host_id)
        self._flows = []

    @property
    def flows(self):
        return self._flows

    def add_flow(self, flow):
        """Add receiving flow to host.

        Parameters
        ----------
        flow : `Flow`
            The flow to add to the host.

        """
        self._flows.append(flow)

    def delete_flow(self, flow):
        self._flows.remove(flow)

    def send(self, packet):
        """Connects to a link.

        Parameters
        ----------
        packet : `Packet`
            The packet to send.

        """
        if len(self._links) > 0:
            self._links[0].receive(packet, self._network_id)
        else:
            raise Exception("Host {0} does not have any links".format(self.network_id))

    def receive(self, packet):
        """Send packet to flow to process.

        Parameters
        ----------
        packet : `Packet`
            The packet to be received.

        """

        for flow in self._flows:
            if packet.flow_id == flow.flow_id:
                flow.receive(packet)
                return
