from host import Host
from router import Router
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
        self.hosts = {}
        self.routers = {}
        self.links = {}
        self.flows = {}

    def check_id(self, obj_id):
        """Raise an exception if object id is not unique."""
        if ((obj_id in self.hosts) or (obj_id in self.routers) or
                (obj_id in self.links) or (obj_id in self.flows)):
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

    def add_router(self, router_id):
        """Construct router and add to dictionary of routers"""
        self.check_id(router_id)
        self.routers[router_id] = Router(router_id)

    def add_link(self, link):
        pass

    def add_flow(self, flow):
        pass
