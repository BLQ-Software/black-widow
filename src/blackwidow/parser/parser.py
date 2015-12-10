from blackwidow.network import Network
import json

def config_network(filename, bw):
    """Returns Network object after parsing a .json file.
    
    Parameters
    ----------
    filename : string 
        name of .json file to configure off of.
    bw : `BlackWidow`
        BlackWidow simulation object containing simulation settings.
    """

    f = open(filename)
    config = json.load(f)
    f.close()
    network = Network(bw)

    for host_id in config['Hosts']:
        network.add_host(host_id)

    for router_id in config['Routers']:
        network.add_router(router_id)

    for link in config['Links']:
        network.add_link(link['network_id'], link['devices'][0],
                         link['devices'][1], link['delay'],
                         link['rate'], link['buffer'])

    for flow in config['Flows']:

        network.add_flow(flow['network_id'], flow['src'],
                         flow['dest'], flow['amount'],
                         flow['start'])

    return network
