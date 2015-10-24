from blackwidow.network import Network
import json

def config_network(filename):
    """Returns config object."""
    f = open(filename)
    config = json.load(f)
    f.close()
    network = Network()
    
    for host_id in config['Hosts']:
        network.add_host(host_id)
    
    for router_id in config['Routers']:
        network.add_router(router_id)

    for link in config['Links']:
        network.add_link(link)
    
    for flow in config['Flows']:
        network.add_flow(flow)

    return network

    
