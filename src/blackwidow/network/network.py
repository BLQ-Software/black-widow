from host import Host
from router import Router
from link import Link
from flow import Flow
from tahoe_flow import TahoeFlow
from reno_flow import RenoFlow
from fast_flow import FastFlow
from Queue import PriorityQueue
import networkx as nx
import matplotlib.pyplot as plt

# Constants
# Time to update router info, in ms.
ROUTER_UPDATE_PERIOD = 100


class Network():
    """Python representation of the network.

    Each host, router, link, and flow object is denoted by a
    unique character id, and placed in a distinct dictionary.
    The check_id function checks the unique id constraint before
    construction any new objects. This is a global id constraint
    across all objects.

    Parameters
    ----------
    bw : `Blackwidow`
        The simulation object containing settings and data recording.

    Attributes
    ----------
    time : float
        The currenet simulation time.
    """
    def __init__(self, bw):
        self.devices = {}
        self.hosts = {}
        self.routers = {}
        self.links = {}
        self.flows = {}
        self.ids = []
        self._time = 0
        self.bw = bw
        self._events = PriorityQueue()
        self.num_flows_active = 0
        self.g = nx.MultiDiGraph()
        self.deleted = []

    @property
    def time(self):
        return self._time

    @time.setter
    def time(self, value):
        raise AttributeError("Cannot modify network time")

    def check_id(self, obj_id):
        """Check if the id is not already used.

        This function checks if the id is not already used. This function
        raises an exception if object id is not unique.

        Parameters
        ----------
        obj_id : string
            The id to check.
        """
        if obj_id in self.ids:
            raise ValueError('id {0} already exists.'.format(obj_id))

    def dump(self, output=False):
        """Prints out network and returns networkx graph

        Prints the devices, links, and flows associated with the network, and
        returns a pydot object with the network graph.

        Parameters
        ----------
        output : boolean, optional
            Specifies whether to print the network information (the default is
            False).

        Returns
        -------
        pydot
            pydot object containing the network graph
        """

        # Print network information if output is True
        if output:
            print "Devices:\n"
            for device_id in self.devices:
                print self.devices[device_id]
            print "Links:\n"
            for link_id in self.links:
                print self.links[link_id]
            print "Flows:\n"
            for flow_id in self.flows:
                print self.flows[flow_id]

        # Convert the graph to a pydot object and return
        return nx.to_pydot(self.g)

    def add_host(self, host_id):
        """Construct host and add to dictionary of hosts.

        Parameters
        ----------
        host_id : string
            A unique id for the host.
        """

        # Check if the id is not already used
        self.check_id(host_id)

        # Create a Host object
        self.devices[host_id] = Host(host_id)

        # Update dictionaries
        self.hosts[host_id] = self.devices[host_id]
        self.ids.append(host_id)

        # Update the graph
        self.g.add_node(host_id, shape="square")

    def add_router(self, router_id):
        """Construct router and add to dictionary of routers.

        Parameters
        ----------
        router_id : string
            A unique id for the router.
        """

        # Check if the id is not already used
        self.check_id(router_id)

        # Create a Router
        self.devices[router_id] = Router(router_id, self, self.bw)

        # Update dictionaries
        self.routers[router_id] = self.devices[router_id]
        self.ids.append(router_id)

        # Update the graph
        self.g.add_node(router_id)

    def delete_device(self, device_id):
        """Deletes a device in the network.

        Parameters
        ----------
        device_id : string
            The id of the `Device` to delete.
        """

        # Get device
        device = self.devices[device_id]

        # Delete all links connected to device
        for link in device.links[:]:
            self.delete_link(link.id)

        # Delete all flows from device
        try:
            for flow in device.flows[:]:

                self.delete_flow(flow.flow_id)
        except:
            pass

        # Update graph
        self.g.remove_node(device_id)

        # Update dictionaries
        self.ids.remove(device_id)
        if device_id in self.hosts:
            del self.hosts[device_id]
        if device_id in self.routers:
            del self.routers[device_id]
        self.deleted.append(device_id)
        del self.devices[device_id]

    def add_link(self, link_id, device_id1, device_id2,
                 delay, rate, capacity):
        """Adds a link to the network.

        Parameters
        ----------
        link_id : string
            A unique id for the link.

        device_id1 : string
            The id of one of the `Device` objects to connect to the link.
        device_id2 : string
            The id of one of the `Device` objects to connect to the link.
        delay : float
            The propagation delay of the link in ms.
        rate : float
            The rate at which the link can send a packet in Mbps.
        capacity : int
            The capacity of the link buffer in KB.
        """

        # Check if the id is not already used
        self.check_id(link_id)

        # Make sure both device ids correspond to existing `Device` objects
        if device_id1 not in self.ids:
            raise KeyError('id {0} does not exist.'.format(device_id1))
        if device_id2 not in self.ids:
            raise KeyError('id {0} does not exist.'.format(device_id2))

        # Get devices
        device_1 = self.devices[device_id1]
        device_2 = self.devices[device_id2]

        # Create link
        self.links[link_id] = Link(link_id, device_1, device_2, delay, rate,
                                   capacity, self, self.bw)

        # Update devices with link
        device_1.add_link(self.links[link_id])
        device_2.add_link(self.links[link_id])

        # Update dictionaries
        self.ids.append(link_id)

        # Update graph
        self.g.add_edge(device_id1, device_id2, label=link_id, dir="none",
                        len=str(delay))

    def delete_link(self, link_id):
        """Deletes a link from the network.

        Parameters
        ----------
        link_id : string
            The id of the link to delete.
        """

        # Get the link
        link = self.links[link_id]

        # Delete the link from the connected devices
        link.device_a.delete_link(link)
        link.device_b.delete_link(link)

        # Remove the edge from the graph. Since the grap is a digraph, we try
        # to remove the edge in both directions.
        try:
            self.g.remove_edge(link.device_a.network_id,
                               link.device_b.network_id)
        except:
            self.g.remove_edge(link.device_b.network_id,
                               link.device_a.network_id)

        # Update dictionaries
        self.ids.remove(link_id)
        self.deleted.append(link_id)
        del self.links[link_id]

    def add_flow(self, flow_id, flow_src, flow_dest, data_amt, flow_start):
        """Adds a flow to the network.

        Parameters
        ----------
        flow_id : string
            A unique id for the flow.
        flow_src : string
            The id for the source `Device` for the flow.
        flow_dest : string
            The id for the destination `Device` for the flow.
        data_amt : float
            The amount of data for the flow to send in MB.
        flow_start : float
            The amount of time to wait before starting the flow in ms.
        """

        # Check if the id is not already used
        self.check_id(flow_id)

        # Get the source and destination devices
        device_1 = self.devices[flow_src]
        device_2 = self.devices[flow_dest]

        # Increment the number of flow active
        self.num_flows_active += 1

        # Determine TCP alg from bw.tcp_alg
        if self.bw.tcp_alg == 'Reno':
            flow = RenoFlow(flow_id, device_1, device_2, data_amt,
                            self, flow_start, self.bw)
        elif self.bw.tcp_alg == 'Tahoe':
            flow = TahoeFlow(flow_id, device_1, device_2, data_amt,
                             self, flow_start, self.bw)
        elif self.bw.tcp_alg == 'Fast':
            flow = FastFlow(flow_id, device_1, device_2, data_amt,
                            self, flow_start, self.bw)
        else:
            raise Exception("Unknown TCP algorithm.")

        # Update dictionaries
        self.flows[flow_id] = flow
        self.ids.append(flow_id)

        # Update devices with flow
        device_1.add_flow(flow)
        device_2.add_flow(flow)

        # Update graph
        self.g.add_edge(flow_src, flow_dest, label=flow_id)

    def delete_flow(self, flow_id):
        """Delete a flow from the network.

        Parameters
        ----------
        flow_id : string
            The id of the flow to delete.
        """

        # Get the flow
        flow = self.flows[flow_id]

        # Delete the flow from the source and destination devices
        flow.src.delete_flow(flow)
        flow.dest.delete_flow(flow)

        # Update the graph
        self.g.remove_edge(flow.src.network_id, flow.dest.network_id)

        # Update dictionaries
        del self.flows[flow_id]
        self.ids.remove(flow_id)
        self.deleted.append(flow_id)

        # Decrement the number of active flows
        self.num_flows_active -= 1

    def decrement_flows(self):
        """Decrements the number of active flows."""
        self.num_flows_active -= 1

    def empty(self):
        """Empties the event queue."""
        self._events = PriorityQueue()

    def add_event(self, event, delay):
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
        # Add the event to the queue with key equal to the time to run the
        # event.
        self._events.put((self._time + delay, event))

    def to_json(self):
        """Returns a JSON representation of the network."""

        data = {}
        hosts = []
        for host_id in self.hosts:
            hosts.append(host_id)
        data["Hosts"] = hosts

        routers = []
        for router_id in self.routers:
            routers.append(router_id)
        data["Routers"] = routers

        links = []
        for link_id in self.links:
            link_data = {}
            link_data["network_id"] = link_id
            link_data["devices"] = [self.links[link_id].device_a.network_id,
                                    self.links[link_id].device_b.network_id]
            link_data["rate"] = self.links[link_id].rate / (10 ** 3)
            link_data["delay"] = self.links[link_id].delay
            link_data["buffer"] = self.links[link_id].capacity / 1000 / 8
            links.append(link_data)
        data["Links"] = links

        flows = []
        for flow_id in self.flows:
            flow_data = {}
            flow_data["network_id"] = flow_id
            flow_data["src"] = self.flows[flow_id].src.network_id
            flow_data["dest"] = self.flows[flow_id].dest.network_id
            flow_data["amount"] = self.flows[flow_id].amount / 8 / (10 ** 6)
            flow_data["start"] = self.flows[flow_id].flow_start / 1000
            flows.append(flow_data)
        data["Flows"] = flows

        return data

    def run(self):
        """Runs the network.

        Dequeues events from the queue and runs them in order until the queue
        is empty or there are 0 flows active.

        Returns
        -------
        time : int
            The amount of time taken for the network to run.
        """

        # Keep running while we have events to run and there are active flows.
        # The first events will be enqueued by the flows when they are
        # initialized.
        while not self._events.empty() and self.num_flows_active != 0:

            # Get the event and time
            (time, current_event) = self._events.get()

            # Don't run the event if it source has been deleted
            if current_event.src_id in self.deleted:
                continue

            print ("{0} at time {1} with {2}"
                   "flows active".format(str(current_event),
                                         time,
                                         self.num_flows_active))

            # Update the current time
            self._time = time

            # Run the event
            current_event.run()

        # Return end time.
        self.bw.write()
        return self._time
