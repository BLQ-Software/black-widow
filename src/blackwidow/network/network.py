from host import Host
from router import Router
from link import Link
from flow import Flow
from tahoe_flow import TahoeFlow
from reno_flow import RenoFlow
from Queue import PriorityQueue
import networkx as nx
import matplotlib.pyplot as plt

# Constants
# Time to update router info, in ms.
ROUTER_UPDATE_PERIOD = 100

plt.ion()


class Network():
    """Python representation of the network.

    Each host, router, link, and flow object is denoted by a
    unique character id, and placed in a distinct dictionary.
    The check_id function checks the unique id constraint before
    construction any new objects. This is a global id constraint
    across all objects.
    """
    def __init__(self, bw):
        self.devices = {}
        self.routers = {}
        self.links = {}
        self.flows = {}
        self.ids = []
        self._time = 0
        self.bw = bw
        self._events = PriorityQueue()
        self.num_flows_active = 0
        self.g = nx.MultiDiGraph()
        self.edge_labels = {}
        self.router_labels = []
        self.host_labels = []
        self.initial_events = {}

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        raise AttributeError("Cannot modify network time")

    def check_id(self, obj_id):
        """Raise an exception if object id is not unique."""
        if obj_id in self.ids:
            raise ValueError('id {0} already exists.'.format(obj_id))

    def dump(self, output=False):
        """Prints out network"""
        if output:
            print "Devices:\n"
            for device_id in self.devices:
                print self.devices[device_id]
            print "Flows:\n"
            for flow_id in self.flows:
                print self.flows[flow_id]
        return nx.to_pydot(self.g)

    def add_host(self, host_id):
        """Construct host and add to dictionary of hosts."""
        self.check_id(host_id)
        self.devices[host_id] = Host(host_id)
        self.ids.append(host_id)
        self.g.add_node(host_id, shape="square")
        self.host_labels.append(host_id)

    def add_router(self, router_id, bw):
        """Construct router and add to dictionary of routers"""
        self.check_id(router_id)
        self.devices[router_id] = Router(router_id, self, bw)
        self.routers[router_id] = self.devices[router_id]
        self.ids.append(router_id)
        self.g.add_node(router_id)
        self.router_labels.append(router_id)

    def delete_device(self, device_id):
        device = self.devices[device_id]
        for link in device.links[:]:
            self.delete_link(link.id)
        try:
            for flow in devices.flows[:]:
                self.delete_flow(flow.flow_id)
        except:
            pass

        self.g.remove_node(device_id)
        self.ids.remove(device_id)
        del self.devices[device_id]

    def add_link(self, link_id, device_id1, device_id2,
                 delay, rate, capacity, bw):
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
                                  self, bw)
        device_1.add_link(self.links[link_id])
        device_2.add_link(self.links[link_id])
        self.ids.append(link_id)

        self.g.add_edge(device_id1, device_id2, label=link_id, dir="none", len=str(delay))
        self.edge_labels[(device_id1, device_id2)] = link_id

    def delete_link(self, link_id):
        link = self.links[link_id]
        link.device_a.delete_link(link)
        link.device_b.delete_link(link)

        try:
            self.g.remove_edge(link.device_a.network_id, link.device_b.network_id)
        except:
            self.g.remove_edge(link.device_b.network_id, link.device_a.network_id)

        self.ids.remove(link_id)
        del self.links[link_id]


    def add_flow(self, flow_id, flow_src, flow_dest, data_amt, flow_start, bw):

        self.check_id(flow_id)
        device_1 = self.devices[flow_src]
        device_2 = self.devices[flow_dest]

        self.num_flows_active += 1

        # Determine TCP alg from bw.tcp_alg
        if self.bw.tcp_alg == 'Reno':
            flow = RenoFlow(flow_id, device_1, device_2, data_amt,
                        self, flow_start, bw)
        elif self.bw.tcp_alg == 'Tahoe':
            flow = TahoeFlow(flow_id, device_1, device_2, data_amt,
                        self, flow_start, bw)
        else:
            raise Exception("Unknown TCP algorithm.")


        self.flows[flow_id] = flow

        device_1.add_flow(flow)
        device_2.add_flow(flow)
        self.g.add_edge(flow_src, flow_dest, label=flow_id)

        self.ids.append(flow_id)

    def delete_flow(self, flow_id):
        flow = self.flows[flow_id]
        flow.src.delete_flow(flow)
        flow.dest.delete_flow(flow)

        self.g.remove_edge(flow.src.network_id, flow.dest.network_id)
        self.ids.remove(flow_id)
        del self.initial_events[flow_id]
        del self.flows[flow_id]
        self.num_flows_active -= 1

    def decrement_flows(self):
        self.num_flows_active -= 1

    def empty(self):
        self._events = PriorityQueue()
        self.initial_events = []

    def add_event(self, event, delay, initial=False):
        """
        Function to add an event to the queue

        This function adds an event to the queue to be run after delay time.

        Parameters
        ----------
        event : `Event`
            The event to be run.
        delay : float
            The amount of time in ms to wait before running the event.

        """
        if initial:
            self.initial_events[event.src_id] = (self._time + delay, event)
        else:
            self._events.put((self._time + delay, event))

    def run(self):

        for i in self.initial_events:
            self._events.put((self.initial_events[i][0], self.initial_events[i][1]))
        # Keep running while we have events to run. The first events will be
        # enqueued by the flows when they are initialized.
        while not self._events.empty() and self.num_flows_active != 0:
            (time, current_event) = self._events.get()
            print "{0} at time {1} with {2} flows active".format(str(current_event), time, self.num_flows_active)
            self._time = time
            current_event.run()

        # Return end time.
        return self._time
