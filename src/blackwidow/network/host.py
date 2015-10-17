from blackwidow.network.device import Device
from blackwidow.network.packet import Packet 

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
        self.host_id = host_id
        self.flows = [] 
    
    def add_flow(self, flow):
        """Add receiving flow to host."""
        self.flows.append(flow)
    
    def set_env(self, env)
        """Set pysim environment."""
        self.env = env

    def send(self, packet): 
        """Connects to a link."""
        self.links[0].receive(packet)

    def receive(self, packet):
        """Send packet to flow to process."""
        for flow in self.flows:
            if packet.flow_id == flow.flow_id:
                flow.receive(packet)
                return
            
            
                




