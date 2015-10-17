from blackwidow.network.host import Host
from blackwidow.network.router import Router
# from blackwidow.network.link import Link
from blackwidow.network.flow import Flow

class Network():
    """Python representation of the network."""
    def __init__(self):
        self.hosts = []
        self.routers = []
        self.links = []
        self.flows = []

    def dump(self):
        """Prints out network"""
        print self.hosts 
        print self.routers
        print self.links
        print self.flows

    def add_host(self, host_id):
        """Construct host and add to list of hosts."""
        self.hosts.append(Host(host_id))

    def add_router(self, router_id):
        pass

    def add_link(self, link):
        pass

    def add_flow(self, flow):
        pass
    



