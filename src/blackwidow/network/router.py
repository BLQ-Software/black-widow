from device import Device
from packet import RoutingPacket

ROUTING_PKT_ID = 'Routing Packet'

class Router(Device):
    """Class for routers.

    Routers are responsible for initializing and updating their
    routing table, and sending packets based on their routing table.
    """

    def __init__(self, router_id, env, bw):
        """Constructor for Router class."""
        super(Router, self).__init__(router_id)
        self.router_id = router_id
        self.env = env
        self.bw = bw
        self.routing_table = {}

    def add_link(self, link):
        """Overrides Device.add_link() ."""
        self._links.append(link)

        network_id = link._device_a.network_id

        if (network_id == self.network_id):
            network_id = link.device_b.network_id

        self.routing_table[network_id] = {'link': link, 'distance': link.rate }

    def send(self, packet):
        """Send packet to appropriate link."""
        route = None
        if packet.dest.network_id in self.routing_table:
            route = self.routing_table[packet.dest.network_id]

        if route is not None and 'link' in route:
            route['link'].receive(packet, self.network_id)

    def receive(self, packet):
        """Process packet."""
        if packet.is_routing:
            self.update_route(packet)
            print "{} received routing packet from {}".format(self.network_id, packet.src)
        else:
            self.send(packet)

    def send_routing(self):
        """Send routing packets to all neighbors."""
        for link in self.links:
            other_device = link._device_a
            if (other_device.network_id == self.network_id):
<<<<<<< HEAD
                other_device = link.device_b
            packet = RoutingPacket(ROUTING_PKT_ID, self.network_id,
=======
                other_device = link._device_b
            packet = RoutingPacket(ROUTING_PKT_ID, self.network_id,
>>>>>>> 6c1d90e53b4f41f328f0f31afc4bf74f77b378d7
                                   other_device.network_id, None,
                                   self.routing_table)
            link.receive(packet, self.network_id)
            print "Sent routing packet from {}".format(self.network_id)


    def update_route(self, packet):
        """Update routing table."""
        # TODO: Add Dijkstra's algorithm.
        link = None
        if packet.src in self.routing_table:
            route = self.routing_table[packet.src]
            if 'link' in route:
                link = route['link']
        else:
            raise ValueError('{} not found in {} \'s routing table.'.format(
                                packet.src, self.network_id))

        for dest, route in packet.routing_table.items():
            distance = route['distance'] + link._delay
            if dest not in self.routing_table:
                self.routing_table[dest] = {'link': link, 'distance': distance}
            elif distance < self.routing_table[dest]['distance']:
                self.routing_table[dest] = {'link': link, 'distance': distance}
