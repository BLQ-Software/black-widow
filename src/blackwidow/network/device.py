class Device(object):
    """Super class for hosts and routers.
    """
    def __init__(self, net_addr):
        """Constructor for device."""
        self.network_id = net_addr
        self.links = []
        self.env = None

    def set_env(self, env):
        """Set simpy environment"""
        self.env = env

    def add_link(self, link):
        """Add link to list of links."""
        self.links.append(link)

    def send(self, packet):
        pass

    def __str__(self):
        msg = "Device {0}, connected to links:\n"
        for link in self.links:
            msg += "  " + str(link) + "\n"
        return msg.format(self.network_id)
