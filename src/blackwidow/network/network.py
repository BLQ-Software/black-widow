from host import Host
from router import Router
from link import Link
from flow import Flow

time = 0
end_time = 1000


class Network():
    """Python representation of the network.

    Each host, router, link, and flow object is denoted by a
    unique character id, and placed in a distinct dictionary.
    The check_id function checks the unique id constraint before
    construction any new objects. This is a global id constraint
    across all objects.
    """
    def __init__(self):
        self.devices = {}
        self.links = {}
        self.flows = {}
        self.ids = []

    def check_id(self, obj_id):
        """Raise an exception if object id is not unique."""
        if obj_id in self.ids:
            raise NameError('id {0} already exists.'.format(obj_id))

    def dump(self):
        """Prints out network"""
        print self.devices
        print self.links
        print self.flows

    def add_host(self, host_id):
        """Construct host and add to dictionary of hosts."""
        self.check_id(host_id)
        self.devices[host_id] = Host(host_id)
        self.ids.append(host_id)

    def add_router(self, router_id):
        """Construct router and add to dictionary of routers"""
        self.check_id(router_id)
        self.devices[router_id] = Router(router_id)
        self.ids.append(router_id)

    def add_link(self, link_id, device_id1, device_id2, delay, rate, capacity):
        self.check_id(link_id)
        if device_id1 not in self.ids:
            raise KeyError('id {0} does not exist.'.format(device_id1))
        if device_id2 not in self.ids:
            raise KeyError('id {0} does not exist.'.format(device_id2))

        # Get devices
        device_1 = self.devices[device_id1]
        device_2 = self.devices[device_id2]

        # Create link
        self.links[link_id] = Link(device_1, device_2, delay, rate, capacity,
                                  self)

    def add_flow(self, flow_id, flow_src, flow_dest, data_amt, flow_start):
        self.devices[flow_id] = Flow(flow_id, flow_src, flow_dest, data_amt,
                                    self, flow_start)

    def run(self):
        global time, end_time
        while time < end_time:
            for id in self.flows:
                self.flows[id].send_packet()
            for id in self.links:
                self.links[id].send()
            time += 1
