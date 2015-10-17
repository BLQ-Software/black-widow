from blackwidow.network.device import Device

class Router(Device):
    """Class for routers.

    Routers are responsible for initializing and updating their 
    routing table, and sending packets based on their routing table.
    """

    def __init__(self, router_id):
        """Constructor for Router class."""
        super(Host, self).__init__(router_id)
        self.router_id = router_id
        self.routing_table = {}

    def add_link(self, link):
        """Overrides Device.add_link() ."""
        self.links.append(link)
        device_id = link.endpoint(self.router_id)
        routing_table[device_id] = link

    def send(self, packet):
        """Send packet to appropriate link."""
        link = routing_table[packet.dest]
        link.send(packet)
    
    def receive(self, packet):
        """Process packet."""
        if packet.is_routing:
            update_route(packet)
        else:
            self.send(packet)

    def update_route(self, packet):
        """Update routing table."""
        # TODO: Add Dijkstra's algorithm.
        pass
