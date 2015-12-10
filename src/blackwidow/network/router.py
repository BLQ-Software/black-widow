from device import Device
from packet import RoutingPacket
from event import Event
from blackwidow.network.rate_graph import Rate_Graph

ROUTING_PKT_ID = 'Routing Packet'


class Router(Device):
    """Class for routers.

    Routers are responsible for initializing and updating their
    routing table, and sending packets based on their routing table.

    Parameters
    ----------
    router_id : string
        A unique id for the router.


    Attributes
    ----------
    network_id : string
        A unique id of the device in the network.
    links : list
        A list of links that the router is connected to.
    routing_table : dict
        A dictionary representing the router's routing table.
    new_routing_table : dict
        A dictionary representing the router's new routing table.
    env : `Network`
        The network that the link belongs to.
    bw : `Blackwidow`
        BlackWidow simulation object containing simulation settings.
    send_rate : Rate_Graph object
        Send rate graphing object.
    receive_rate : Rate_Graph object
        Receive rate graphing object.

    Methods
    -------
    add_link(link)
        Adds a link to the router.
    send(packet)
        Sends a packet to a link.
    receive(packet)
        Receives a packet from a link.
    start_new_routing()
        Starts a new routing round.
    send_routing()
        Sends a routing packet to all neighbors.
    update_route()
        Update the new_routing_table based on routing packets.
    _distance(link)
        Gets the distance of a link.
    """
    def __init__(self, router_id, env, bw):
        """Constructor for Router class."""
        super(Router, self).__init__(router_id)
        self.env = env
        self.bw = bw
        self._routing_table = {}
        self._new_routing_table = {}
        self._send_rate = Rate_Graph(router_id,
                                     "router {0} send rate".format(router_id),
                                     self.env,
                                     self.bw)
        self._receive_rate = Rate_Graph(router_id,
                                        "router {0} receive"
                                        " rate".format(router_id),
                                        self.env,
                                        self.bw)
        self.env.add_event(Event("{} sent routing"
                                 " packet".format(self._network_id),
                                 self._network_id,
                                 self.start_new_routing),
                           0)

    def add_link(self, link):
        """Overrides Device.add_link() to add to routing table.

        Parameters
        ----------
        link : Link
            The link to add to the router.
        """
        self._links.append(link)

        network_id = link._device_a.network_id

        if (network_id == self._network_id):
            network_id = link._device_b.network_id

        self._routing_table[network_id] = {'link': link,
                                           'distance': self._distance(link)}
        self._new_routing_table[network_id] = \
            {'link': link, 'distance': self._distance(link)}

    def send(self, packet):
        """Send packet to appropriate link.

        First looks in the new routing table to see if we know how to reach
        it there. Otherwise uses the old routing table.

        Parameters
        ----------
        packet : Packet
            Packet to send through the router.
        """
        route = None
        self._send_rate.add_point(packet, self.env.time)

        if packet.dest.network_id in self._new_routing_table:
            route = self._new_routing_table[packet.dest.network_id]
        elif packet.dest.network_id in self._routing_table:
            route = self._routing_table[packet.dest.network_id]

        if route is not None and 'link' in route:
            route['link'].receive(packet, self._network_id)

    def receive(self, packet):
        """Process packet by sending it out.

        If the packet is routing, calls update_route to update the
        new_routing_table.

        Parameters
        ----------
        packet : Packet
            Received packet.
        """
        self._receive_rate.add_point(packet, self.env.time)
        if packet.is_routing:
            self.update_route(packet)
            print "{} received routing packet from {}".format(self._network_id,
                                                              packet.src)
        else:
            self.send(packet)

    def start_new_routing(self):
        """Start a new routing round.

        If there is dynamic routing, updates the routing table to the new
        routing table built up by dynamic routing and measures the distance
        for each link.
        """
        # Reset routing table if dynamic routing.
        if not self.bw.static_routing:
            self._new_routing_table = {}
            for link in self._links:
                link.measure_distance()
                network_id = link._device_a.network_id
                if (network_id == self._network_id):
                    network_id = link._device_b.network_id
                self._new_routing_table[network_id] = \
                    {'link': link, 'distance': self._distance(link)}
            self._routing_table = self._new_routing_table
            self.env.add_event(Event("{} reset its routing"
                     " table.".format(self._network_id),
                     self._network_id,
                     self.start_new_routing),
                   5000)

        self.send_routing()

    def send_routing(self):
        """Send routing packets to all neighbors."""
        for link in self._links:
            other_device = link._device_a
            if (other_device.network_id == self._network_id):
                other_device = link.device_b

            if type(other_device) is Router:
                packet = RoutingPacket(ROUTING_PKT_ID, self._network_id,
                                       other_device.network_id, None,
                                       self._new_routing_table,
                                       self.bw.routing_packet_size)
                link.receive(packet, self._network_id)
                print "Sent routing packet from {}".format(self._network_id)

    def update_route(self, packet):
        """Update routing table.

        Goes through the routing table contained in the routing packet and
        determines if it contains a better way to get to each destination.
        This uses a distributed version of the Bellman-Ford algorithm.

        Parameters
        ----------
        packet : Packet
            Routing packet to update the route.
        """
        link = None
        if packet.src in self._new_routing_table:
            route = self._new_routing_table[packet.src]
            if 'link' in route:
                link = route['link']
        else:
            raise ValueError('{} not found in {} \'s routing table.'.format(
                             packet.src, self._network_id))

        route_changed = False
        for dest, route in packet.routing_table.items():
            distance = route['distance'] + link.distance

            if dest not in self._new_routing_table:
                self._new_routing_table[dest] = {'link': link,
                                                 'distance': distance}
                route_changed = True
            elif distance < self._new_routing_table[dest]['distance']:
                self._new_routing_table[dest] = {'link': link,
                                                 'distance': distance}
                route_changed = True

        if route_changed or self.env.time < 0.5:
            self.send_routing()

    def _distance(self, link):
        """Get the distance of the link.

        Parameters
        ----------
        link : Link
            Link to get distance of.
        """
        distance = link.delay + link.get_buffer_size() / float(link.rate)

        if self.bw.static_routing:
            distance = link.delay

        return distance
