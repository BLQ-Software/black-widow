from blackwidow.parser import config

def test_host():
    network = config('case0.json')
    network.dump()
    assert network.hosts[0].host_id == 'H1'
