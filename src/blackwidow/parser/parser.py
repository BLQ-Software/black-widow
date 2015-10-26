from blackwidow.network import Network
import json

def config_network(filename, bw):
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
        network.add_link(link['network_id'], link['devices'][0], 
                         link['devices'][1], link['delay'], 
                         link['rate'], link['buffer'], bw)

    for flow in config['Flows']:
        network.add_flow(flow['network_id'], flow['src'],
                         flow['dest'], flow['amount'],
                         flow['start'])

    return network
