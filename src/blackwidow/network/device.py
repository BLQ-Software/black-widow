class Device(object):
    """Super class for hosts and routers.
    """
    def __init__(self, net_addr):
        """Constructor for device."""
        self.net_addr = net_addr
        self.links = []
        self.env = None

    def set_env(self, env):
        """Set simpy environment"""
        self.env = env

    def add_link(self, link):
        """Add link to list of links."""
        self.links.append(link)
