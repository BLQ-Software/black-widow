from blackwidow.parser import config_network

def test_host():
    network = config_network('cases/case0.json')
    network.dump()
    assert network.devices['H1'].host_id == 'H1'
