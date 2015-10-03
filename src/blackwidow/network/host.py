class Host:
    """Simple class for hosts.
    
    Hosts are mainly responsible for recording their time data. 
    They don't trigger events in the simulation, but it will be
    useful to separate host data (end to end data). Flows
    will trigger host behavior.
    """
    def __init__(self, host_id, link_id):
        """Constructor for Host class.
        """
        self.host_id = host_id
        self.link_id = link_id

    def send(): 
        """Connects to a link"""

