class Device(object):
    """Super class for the `Host` and `Router` classes.

    Parameters
    ----------
    net_addr : string
        A unique id for the device in the network.

    Attributes
    ----------
    network_id : string
        A unique id of the device in the network.
    links : list
        A list of links that the device is connected to.

    Methods
    -------
    add_link(link)
        Adds the specified `Link` object to `links`.
    delete_link(link)
        Remotes the specified `Link` object from `links`.
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

    def add_link(self, link):
        """Add link to list of links.
        
        Parameters
        ----------
        link : `Link`
            The link to add to the device.
        """
        self._links.append(link)

    def delete_link(self, link):
        """Remove link from list of links.
        
        Parameters
        ----------
        link : `Link`
            The link to remove from the device.
        """
        self._links.remove(link)

    def send(self, packet):
        """Virtual method for sending device packets.
        
        Parameters
        ----------
        packet : `Packet`
            Packet to send.
        """
        pass

    def __str__(self):
        """Returns a string representation of the device."""
        msg = "Device {0}, connected to links:\n"
        for link in self._links:
            msg += "  " + str(link) + "\n"
        return msg.format(self._network_id)
