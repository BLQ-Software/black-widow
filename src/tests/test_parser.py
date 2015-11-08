from blackwidow.parser import config_network

def test_host():
    network = config_network('cases/case0.json', None)
    network.dump()
    assert network.devices['H1'].network_id == 'H1'
