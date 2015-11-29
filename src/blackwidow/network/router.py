from device import Device
from packet import RoutingPacket
from event import Event
from blackwidow.network.rate_graph import Rate_Graph

ROUTING_PKT_ID = 'Routing Packet'

class Router(Device):
    """Class for routers.

    Routers are responsible for initializing and updating their
    routing table, and sending packets based on their routing table.
    """


    def __init__(self, router_id, env, bw):
        """Constructor for Router class."""
        super(Router, self).__init__(router_id)
        self.env = env
        self.bw = bw
        self._routing_table = {}
        self._send_rate = Rate_Graph(router_id, "router {0} send rate".format(router_id), self.env, self.bw)
        self._receive_rate = Rate_Graph(router_id, "router {0} receive rate".format(router_id), self.env, self.bw)
        self.env.add_event(Event('{} sent routing packet'.format(self._network_id),
                                 self._network_id, self.start_new_routing), 0)


    def add_link(self, link):
        """Overrides Device.add_link() ."""
        self._links.append(link)

        network_id = link._device_a.network_id

        if (network_id == self._network_id):
            network_id = link._device_b.network_id

        self._routing_table[network_id] = {'link': link, 'distance': self._distance(link)}

    def send(self, packet):
        """Send packet to appropriate link."""
        route = None
        self._send_rate.add_point(packet, self.env.time)
        if packet.dest.network_id in self._routing_table:
            route = self._routing_table[packet.dest.network_id]

        if route is not None and 'link' in route:
            route['link'].receive(packet, self._network_id)

    def receive(self, packet):
        """Process packet."""
        self._receive_rate.add_point(packet, self.env.time)
        if packet.is_routing:
            self.update_route(packet)
            print "{} received routing packet from {}".format(self._network_id, packet.src)
        else:
            self.send(packet)

    def start_new_routing(self):
        """Start a new routing round."""
        # Reset routing table if dynamic routing.
        if not self.bw.static_routing:
            self._routing_table = {}
            for link in self._links:
                link.measure_distance()
                network_id = link._device_a.network_id
                if (network_id == self._network_id):
                    network_id = link._device_b.network_id
                self._routing_table[network_id] = {'link': link, 'distance': self._distance(link)}

            self.env.add_event(Event('{} reset its routing table.'.format(self._network_id),
                               self._network_id, self.start_new_routing), 5000)


        self.send_routing()



    def send_routing(self):
        """Send routing packets to all neighbors."""
        for link in self._links:
            other_device = link._device_a
            if (other_device.network_id == self._network_id):

                other_device = link.device_b
            packet = RoutingPacket(ROUTING_PKT_ID, self._network_id,
                                   other_device.network_id, None,
                                   self._routing_table, self.bw.routing_packet_size)
            link.receive(packet, self._network_id)
            print "Sent routing packet from {}".format(self._network_id)


    def update_route(self, packet):
        """Update routing table."""
        link = None
        if packet.src in self._routing_table:
            route = self._routing_table[packet.src]
            if 'link' in route:
                link = route['link']
        else:
            raise ValueError('{} not found in {} \'s routing table.'.format(
                                packet.src, self._network_id))

        route_changed = False
        for dest, route in packet.routing_table.items():
            distance = route['distance'] + link.distance
            if dest not in self._routing_table:
                self._routing_table[dest] = {'link': link, 'distance': distance}
                route_changed = True
            elif distance < self._routing_table[dest]['distance']:
                self._routing_table[dest] = {'link': link, 'distance': distance}
                route_changed = True

        if route_changed:
            self.send_routing()

    def _distance(self, link):
        """Get the distance from the link."""
        distance = link.delay + link.get_buffer_size() / float(link.rate)

        if self.bw.static_routing:
            distance = link.delay

        return distance
