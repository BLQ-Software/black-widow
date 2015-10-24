from host import Host
from router import Router
from flow import Flow

global time = 0.0
global end_time = 1000

class Network():
    """Python representation of the network.

    Each host, router, link, and flow object is denoted by a
    unique character id, and placed in a distinct dictionary.
    The check_id function checks the unique id constraint before
    construction any new objects. This is a global id constraint
    across all objects.
    """
    def __init__(self):
        self.hosts = {}
        self.routers = {}
        self.links = {}
        self.flows = {}
        self.ids = []

    def check_id(self, obj_id):
        """Raise an exception if object id is not unique."""
        if obj_id in self.ids:
            raise NameError('id {0} already exists.'.format(obj_id))

    def dump(self):
        """Prints out network"""
        print self.hosts
        print self.routers
        print self.links
        print self.flows

    def add_host(self, host_id):
        """Construct host and add to dictionary of hosts."""
        self.check_id(host_id)
        self.hosts[host_id] = Host(host_id)
        self.ids.append(host_id)

    def add_router(self, router_id):
        """Construct router and add to dictionary of routers"""
        self.check_id(router_id)
        self.routers[router_id] = Router(router_id)
        self.ids.append(router_id)

    def add_link(self, link_id, device_id1, device_id2, delay, rate, capacity):
        self.check_id(link_id)
        if device_id1 not in self.ids:
            raise KeyError('id {0} does not exist.'.format(device_id1))
        if device_id2 not in self.ids:
            raise KeyError('id {0} does not exist.'.format(device_id2))

        # Get devices
        if device_id1 in self.hosts:
            device_1 = self.hosts[device_id1]
        else:
            device_1 = self.routers[device_id1]

        if device_id2 in self.hosts:
            device_2 = self.hosts[device_id2]
        else:
            device_2 = self.routers[device_id2]

        # Create link
        self.links[link_id] = Link(device_1, device_2, delay, rate, capacity)

    def add_flow(self, flow):
        pass

    def run(self):
        global time, end_time
        while time < end_time:
            for id in self.flows:
                self.flows[id].send_packet()
            for id in self.links:
                self.links[id].send()
            time += 1
