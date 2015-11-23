class Device(object):
    """Super class for hosts and routers.
    """
    def __init__(self, net_addr):
        """Constructor for device."""
        self._network_id = net_addr
        self._links = []
        self.env = None

    @property
    def network_id(self):
        return self._network_id

    @network_id.setter
    def network_id(self, value):
        raise AttributeError("Cannot modify device id: {0}".format(self._network_id))

    @property
    def links(self):
        return self._links

    def set_env(self, env):
        """Set simpy environment"""
        self.env = env

    def add_link(self, link):
        """Add link to list of links."""
        self._links.append(link)

    def delete_link(self, link):
        self._links.remove(link)

    def send(self, packet):
        pass

    def __str__(self):
        msg = "Device {0}, connected to links:\n"
        for link in self._links:
            msg += "  " + str(link) + "\n"
        return msg.format(self._network_id)
