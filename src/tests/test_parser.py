from blackwidow.parser import config_network

def test_host():
    network = config_network('case0.json')
    network.dump()
    assert network.hosts['H1'].host_id == 'H1'
