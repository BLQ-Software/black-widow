from blackwidow.network.device import Device
from blackwidow.network.host import Host

def test_construct():
    d = Device('H1')
    assert d.network_id == 'H1'

def test_host():
    h1 = Host('H1')
    h2 = Host('H2')
    h1.add_link('L1')
    assert h1.links[0] == 'L1'
    assert h2.links == []
