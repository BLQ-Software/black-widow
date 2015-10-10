from device import Device

class Host(Device):
    """Simple class for hosts.
    
    Hosts are mainly responsible for recording their time data. 
    They don't trigger events in the simulation, but it will be
    useful to separate host data (end to end data). Flows
    will trigger host behavior.
    """
    def __init__(self, host_id):
        """Constructor for Host class.
        """
        super(Host, self).__init__(host_id)
        self.host_id = host_id

    def send(): 
        """Connects to a link"""

