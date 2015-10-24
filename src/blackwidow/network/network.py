from host import Host
from router import Router
from link import Link
from flow import Flow


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
        self.time = 0

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
        self.links[link_id] = Link(link_id, device_1, device_2, delay, rate, capacity,
                                  self)
        device_1.add_link(self.links[link_id])
        device_2.add_link(self.links[link_id])
        self.ids.append(link_id)

    def add_flow(self, flow_id, flow_src, flow_dest, data_amt, flow_start):
        device_1 = self.devices[flow_src]
        device_2 = self.devices[flow_dest]


        flow = Flow(flow_id, device_1, device_2, data_amt,
                        self, flow_start)
        self.flows[flow_id] = flow

        device_1.add_flow(flow)
        device_2.add_flow(flow)


        self.ids.append(flow_id)

    def run(self):
        while True:
            if self.time % 10 == 0:
                print "Time: {0} ms".format(self.time)
            done = True
            for id in self.links:
                # print "Attempting to send on link {0}".format(id)
                self.links[id].send()
            for id in self.flows:
                # print "Attempting to send on flow {0}".format(id)
                self.flows[id].send_packet()
                if not self.flows[id].done:
                    done = False
            self.time += 1
            if done or self.time > 2000:
                break
